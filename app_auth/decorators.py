'''
Making sure inbound request has valid header
'''
from functools import wraps
from flask import request, jsonify
import datetime

from app_auth.models import AppAuth, Tokens

def app_required(f):
    @wraps(f) # preserve your functions metadata
    def dec_func(*args, **kwargs):
        '''
        Checking if creds and token are good
        :return:
        Error if creds or token are bad
        '''

        appauth_id = request.headers.get('x-access-id')
        appauth_token = request.headers.get('x-access-token')

        # checking if access values are set on inbound header
        if not appauth_id or not appauth_token:
            error = {'error': "NO_ACCESS_ID_OR_TOKEN_SENT"}
            return jsonify(error), 403

        app_auth_rec = AppAuth.objects.filter(appauth_id=appauth_id).first()
        # error if user id does not exist
        if not app_auth_rec:
            error = {'error': "NO_RECORD_FOR_ACCESS_ID"}
            return jsonify(error), 403


        token_rec = Tokens.objects.filter(appauth=app_auth_rec).first()
        # error if not user token
        if not token_rec:
            error = {'error': "NO_RECORD_FOR_TOKEN"}
            return jsonify(error), 403

        # if user db token does not match in bound token, error
        if token_rec.token != appauth_token:
            error = {'error': "TOKEN_DOES_NOT_MATCH"}
            return jsonify(error), 403

        # if token expired, error
        if token_rec.expires < datetime.datetime.utcnow():
            error = {'error': "TOKEN_EXPIRED"}
            return jsonify(error), 403

        return f(*args, **kwargs)
    return dec_func
