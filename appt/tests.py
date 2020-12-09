from application import create_app as create_base_settings
from mongoengine.connection import _get_db
import unittest
import json

from settings import MONGODB_HOST
from appt.models import Appts
from application import fixtures

class ApptsTest(unittest.TestCase):

    def create_app(self):
        self.db_name = 'appts-api-test'
        db_settings = {
            'DB': self.db_name,
            'HOST': MONGODB_HOST
        }
        return create_base_settings(
            MONGODB_SETTINGS=db_settings,
            TESTING=True,
            WTF_CSRF_ENABLED=False, # we don't need csrf protection in unit testing
            SECRET_KEY = 'hushy', # used to encrypt sessions objects
        )

    def setUp(self):
        # appauth is now the test client so we can send requests using appauth
        self.app = self.create_app().test_client()

    def tearDown(self):
        db = _get_db()
        db.client.drop_database(db)

    def appts_cred_dict(self):
        user_info = {
            'appauth_id':"appts_client",
            'appauth_secret':"appts_secret"
        }
        return json.dumps(user_info)

    def appts_info_dict(self):
        rec_info = {'first_name': 'Brown',
                    'last_name': 'Cheese',
                    'service': 'Tire rotation',
                    'status': 'open',
                    'street_address': '4335 82th Street',
                    'city': 'Broland',
                    'state': 'NA',
                    'zip': '44413',
                    'phone': '123-456-7890',
                    'date': '2020-11-11T12:12:01Z',
                    'price': '38233.22'}
        return json.dumps(rec_info)

    def create_api_app(self):
        # create our app credentials
        rcode = self.app.post('/appsauth/',
            data=self.appts_cred_dict(),
            content_type='application/json')

        assert rcode.status_code == 200


    def generate_access_token(self):
        # generate an access token
        rcode = self.app.post('/appsauth/tokens/',
            data=self.appts_cred_dict(),
            content_type='application/json')

        self.token = json.loads(rcode.data.decode('utf-8')).get('token')

    def headers(self):
        header_info = {
            'x-access-id': 'appts_client',
            'x-access-token': self.token
        }
        return header_info

    def test_appts(self):
        # get app up and running
        self.create_api_app()
        self.generate_access_token()

        # create an appointment
        rcode = self.app.post('/appts/',
            headers=self.headers(),
            data=self.appts_info_dict(),
            content_type='application/json')
        appt_id = json.loads(rcode.data.decode('utf-8')).get('appt')['id']
        assert rcode.status_code == 201




        # get an appointment
        rcode = self.app.get('/appts/' + appt_id,
            headers=self.headers(),
            content_type='application/json')
        assert rcode.status_code == 200


        # get an appointment on date range
        rcode = self.app.get('/appts/?startdate=2020-11-02&enddate=2020-12-5',
            headers=self.headers(),
            content_type='application/json')


        # get no appointment on date range
        rcode = self.app.get('/appts/?startdate=2025-11-02&enddate=2025-12-5',
            headers=self.headers(),
            content_type='application/json')

        assert "first_name" not in str(rcode.data)

        # update an apointment
        update_fields = {
            'status':"closed"
        }
        update_appt = json.dumps(update_fields)
        rcode = self.app.put('/appts/' + appt_id,
            headers=self.headers(),
            data=update_appt,
            content_type='application/json')

        assert rcode.status_code == 200
        assert json.loads(rcode.data.decode('utf-8')).get('appt')['status'] == "closed"

        # delete an appointment
        rcode = self.app.delete('/appts/' + appt_id,
            headers=self.headers(),
            content_type='application/json')
        assert rcode.status_code == 204
        assert Appts.objects.filter(live=False).count() == 1

    def test_pagination(self):
        # get app up and running
        self.create_api_app()
        self.generate_access_token()

        # import fixtures
        # uploaded test recs to db
        fixtures(self.db_name, "appts", "appt/fixtures/appts.json")

        # get all appts
        rcode = self.app.get('/appts/',
            headers=self.headers(),
            content_type='application/json')
        assert "next" in str(rcode.data)

        # get second page of appts
        rcode = self.app.get('/appts/?page=2',
            headers=self.headers(),
            content_type='application/json')
        assert "previous" in str(rcode.data)
        assert "next" in str(rcode.data)
