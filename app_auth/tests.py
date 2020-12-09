from application import create_app as create_base_settings
from mongoengine.connection import _get_db
import unittest
import json
from datetime import datetime, timedelta


from app_auth.models import AppAuth, Tokens
from settings import MONGODB_HOST

class AppAuthTest(unittest.TestCase):
    def create_app(self):
        self.db_name = 'appts-api-test'
        db_settings = {
            'DB': self.db_name,
            'HOST': MONGODB_HOST
        }
        settings = create_base_settings(
            MONGODB_SETTINGS=db_settings,
            TESTING=True, # needed to test for assertions or exceptions
            WTF_CSRF_ENABLED=False,
            SECRET_KEY = 'heyThere'

        )
        return settings

    def setUp(self):
        # appauth is now the test client so we can send requests using appauth
        self.appauth = self.create_app().test_client()


    def tearDown(self):
        # get the connection object from mongoengine
        db = _get_db()
        db.client.drop_database(db)

    def appauth_dict(self):
        user_info = {
            'appauth_id':"appts_client",
            'appauth_secret':"appts_secret"
        }
        return json.dumps(user_info)


    def test_create_app(self):
        # registration
        rcode = self.appauth.post('/appsauth/',
                               data=self.appauth_dict(),
                               content_type='application/json')
        assert rcode.status_code == 200

        # missing appauth_secret
        user_id_only = {'appauth_id':"appts_client"}
        missing_sec_info = json.dumps(user_id_only)
        rcode = self.appauth.post('/appsauth/',
                                  data=missing_sec_info,
                                  content_type='application/json')
        assert "MISSING_APPAUTH_ID_OR_SECRET" in str(rcode.data)

        # duplicate entry
        rcode = self.appauth.post('/appsauth/',
                                  data=self.appauth_dict(),
                                  content_type='application/json')
        assert "APPAUTH_ID_EXISTS" in str(rcode.data)


    def test_token_gen(self):
        rcode = self.appauth.post('/appsauth/',
            data=self.appauth_dict(),
            content_type='application/json')
        assert rcode.status_code == 200


        # generate access token
        rcode = self.appauth.post('/appsauth/tokens/',
            data=self.appauth_dict(),
            content_type='application/json')
        token = json.loads(rcode.data.decode('utf-8')).get('token')
        assert token is not None


        # missing secret
        user_id_only = {'appauth_id':"appts_client"}
        missing_sec = json.dumps(user_id_only)
        rcode = self.appauth.post('/appsauth/tokens/',
                                  data=missing_sec,
                                  content_type='application/json')
        assert "MISSING_APPAUTH_ID_OR_SECRET" in str(rcode.data)

        # incorrect secret
        user_info = {
            'appauth_id':"appts_client",
            'appauth_secret':"blas" # bad secret
        }
        incorrect_sec = json.dumps(user_info)

        rcode = self.appauth.post('/appsauth/tokens/',
                                  data=incorrect_sec,
                                  content_type='application/json')

        assert "INCORRECT_CREDENTIALS" in str(rcode.data)


        # valid token
        header_info_valid = {
            'x-access-id':'appts_client',
            'x-access-token': token
        }
        rcode = self.appauth.get('/appts/',
                                  headers=header_info_valid,
                                  content_type='application/json')

        assert "NO_RECORDS" in str(rcode.data)

        # bad token
        header_info_wrong = {
            'x-access-id':"appts_client",
            'x-access-token': "wrong"
        }
        rcode = self.appauth.get('/appts/',
                                  headers=header_info_wrong)
        assert rcode.status_code == 403


        # expired token
        now = datetime.utcnow().replace(second=0, microsecond=0)
        expires = now + timedelta(days=-31)
        access = Tokens.objects.first()
        access.expires = expires
        access.save()
        rcode = self.appauth.get('/appts/',
            headers=header_info_valid,
            content_type='application/json')

        assert "TOKEN_EXPIRED" in str(rcode.data)
