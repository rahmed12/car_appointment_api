'''
Instead of using function routes we are going to use objects
For better maintenance
'''
from flask.views import MethodView
from flask import jsonify, request, abort
from jsonschema import Draft7Validator
from jsonschema.exceptions import best_match
import uuid
import json
import datetime

from mongoengine import Q

from app_auth.decorators import app_required
from appt.schema_validate import schema, schema_put
from appt.dbfields_to_json import appts_obj, appt_obj
from appt.models import Appts


class ApptsApi(MethodView):

    # plugable view allows you to pass decorators as a list
    # we cant use the @app_required above the class since it's a class
    # and not a function
    decorators = [app_required]

    def __init__(self):
        self.APPTS_PER_PAGE = 10 # for pagination functionality
        if (request.method != 'GET' and request.method != 'DELETE') and not request.json:
            abort(400)



    def get(self, appt_id):
        '''
        :param appt_id: None or rec id
        :return:
        All recs if None in appt_id
        All recs in date range sort by prices if startdate and enddate on url
        Specific rec if app_id has valid id
        Error if bad request
        '''
        if appt_id:
            appt = Appts.objects.filter(external_id=appt_id, live=True).first()
            if appt:
                reply = {'result':"ok", 'appt': appt_obj(appt)}
                return jsonify(reply), 200
            else:
                return jsonify({}), 404
        else:
            # appt url baseline
            appts_href = "/appts/?page=%s"

            # get all appointments
            appts_recs = Appts.objects.filter(live=True)
            if not appts_recs:
                reply = {"error": "NO_RECORDS"}
                return jsonify(reply), 404

            # filter appointment rec if startdate and endate set
            if "startdate" in request.args and "enddate" in request.args:

                try:
                    datetime.datetime.strptime(request.args.get('startdate'), '%Y-%m-%d')
                    datetime.datetime.strptime(request.args.get('enddate'), '%Y-%m-%d')
                except:
                    return jsonify({"error": "INVALID_START_OR_END_DATE"}), 400

                appts_recs = appts_recs.order_by('+price')
                appts_recs = appts_recs.filter(Q(date__gte=request.args.get('startdate')) &
                                               Q(date__lte=request.args.get('enddate')))
                appts_href += "&startdate=" + request.args.get('startdate') + "&enddate=" + request.args.get('enddate')
            page = int(request.args.get('page', 1))

            appts_recs = appts_recs.paginate(page=page, per_page=self.APPTS_PER_PAGE)

            # adding some HATEOAS (hypertext used to find your way through the API)
            reply = {
                'result': "ok",
                'links': [
                    {
                        'href': appts_href % page,
                        'rel': "self"
                    }
                ],
                "appts" : appts_obj(appts_recs)
            }
            if appts_recs.has_prev:
                reply['links'].append(
                    {
                        'href': appts_href % (appts_recs.prev_num),
                        'rel': "previous"
                    }
                )
            if appts_recs.has_next:
                reply['links'].append(
                    {
                        'href': appts_href % (appts_recs.next_num),
                        'rel': "next"
                    }
                )
            return jsonify(reply), 200

    def post(self):
        '''
        Takes in an json obj and creats a record from it
        Using jsonscheme to validate the json obj

        :return:
        Ok with status code 201 if added record
        Error if inbound json obj bad
        '''
        appt_json = request.json
        error = best_match(Draft7Validator(schema).iter_errors(appt_json))
        if error:
            return jsonify({"error": error.message}), 400

        try:
            date = datetime.datetime.strptime(
                appt_json.get('date'), "%Y-%m-%dT%H:%M:%SZ")
        except:
            return jsonify({"error": "INVALID_DATE"}), 400

        appt = Appts(
            external_id=str(uuid.uuid4()),
            first_name=appt_json.get('first_name'),
            last_name=appt_json.get('last_name'),
            service=appt_json.get('service'),
            status=appt_json.get('status'),
            street_address=appt_json.get('street_address'),
            city=appt_json.get('city'),
            state=appt_json.get('state'),
            zip=appt_json.get('zip'),
            phone=appt_json.get('phone'),
            date=date,
            price=appt_json.get('price')
        ).save()
        reply = {
            "result": "ok",
            "appt": appt_obj(appt)
        }
        return jsonify(reply), 201




    # not going to use patch because it doesn't work too well on all devices
    # using put to do update
    def put(self, appt_id):
        '''
        Updates the status of a recod
        :param appt_id:
        rec id to update
        :return:
        Error if fail json schema validation
        If updated send back ok with status code 200
        '''
        if appt_id:
            appt = Appts.objects.filter(external_id=appt_id, live=True).first()
            if not appt:
                return jsonify({}), 404
            appt_json = request.json
            error = best_match(Draft7Validator(schema_put).iter_errors(appt_json))

            if error:
                return jsonify({'error': error.message}), 400


            appt.status=appt_json.get('status')
            appt.save()

            reply = {
                "result": "ok",
                "appt": appt_obj(appt)
            }
            return jsonify(reply), 200


    def delete(self, appt_id):
        '''
        Delete a specific record
        :param appt_id:
        Rec id to delete
        :return:
        Error code 404 returend if can't find rec
        Status code of 204 returned when deleted
        '''
        if appt_id:
            appt = Appts.objects.filter(external_id=appt_id, live=True).first()
            if not appt:
                return jsonify({}), 404

            appt.live=False
            appt.save()

            return jsonify({}), 204
