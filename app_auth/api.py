'''
Token generator
'''
from flask.views import MethodView
from flask import request, abort, jsonify
import bcrypt
# uuid will be used to create our tokens
import uuid
from datetime import datetime, timedelta

from app_auth.models import AppAuth, Tokens

class AppAuthApi(MethodView):

    def __init__(self):
        if not request.json:
            abort(400)

    def post(self):
        '''
        Creating user creds to be used later on for generating token
        :return:
        Error if appauth_id and appauth_secret not in json header
        '''
        if not 'appauth_id' in request.json or not 'appauth_secret' in request.json:
            error = {'code': "MISSING_APPAUTH_ID_OR_SECRET"}
            return jsonify({'error': error}), 400

        # check to see if credentials rec exist, if it does throw an error
        app_auth_rec = AppAuth.objects.filter(appauth_id=request.json.get('appauth_id')).first()
        if app_auth_rec:
            error = {'code': "APPAUTH_ID_EXISTS"}
            return jsonify({'error': error}), 400
        else:
            # create the credentials
            # encrypt it
            salt = bcrypt.gensalt()
            encryp_pass = bcrypt.hashpw(request.json.get('appauth_secret'), salt)
            app_auth = AppAuth(
                appauth_id=request.json.get('appauth_id'),
                appauth_sec = encryp_pass
            ).save()
            return jsonify({'result': 'ok'}), 200


class TokensApi(MethodView):
    def __init__(self):
        if not request.json:
            abort(400)


    def post(self):
        '''
        Token generation
        :return:
        Error if appauth_id and appauth_secret does not exit in json header
                no creds create
                incorrects creds
        '''

        if not 'appauth_id' in request.json or not 'appauth_secret' in request.json:
            error = {'code': "MISSING_APPAUTH_ID_OR_SECRET"}
            return jsonify({'error': error}), 400

        # check to see if credentials exist, if it does not that means never had access to make token
        # or did not create their credentials, return error
        app_auth_rec = AppAuth.objects.filter(appauth_id=request.json.get('appauth_id')).first()
        if not app_auth_rec:
            error = {'code': "INVALID_CREDENTIALS_OR_CREDENTIALS_DOES_NOT_EXIST"}
            return jsonify({'error': error}), 400
        else:
            # create the token
            # if encypted inbound password is same as db recod then delete all existing tokens and make
            # this one the newest one
            if bcrypt.hashpw(request.json.get('appauth_secret'), app_auth_rec.appauth_sec) == app_auth_rec.appauth_sec:
                # getting all tokens based on incoming credentials and delete them
                existing_tokens = Tokens.objects.filter(appauth=app_auth_rec).delete()

                token = str(uuid.uuid4()) # random number of new token
                now = datetime.utcnow().replace(second=0, microsecond=0)
                expires = now + timedelta(days=30)
                tokens = Tokens(
                    appauth=app_auth_rec,
                    token=token,
                    expires=expires
                ).save()
                # 3339 is a standard time format
                expires3339_format = expires.isoformat("T") + "Z"
                return jsonify({'token': token, 'expires': expires3339_format}), 200
            else:
                error = {'code': "INCORRECT_CREDENTIALS"}
                return jsonify({'error': error}), 400
