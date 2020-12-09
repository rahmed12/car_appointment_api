'''
This is where we bind our url routes to our method classes using Pluggable Views
'''

from flask import Blueprint
from app_auth.api import AppAuthApi, TokensApi

app_appauth = Blueprint('app_appauth', __name__)


app_appauth.add_url_rule('/appsauth/', view_func=AppAuthApi.as_view('appauth_api'), methods=['POST'])
app_appauth.add_url_rule('/appsauth/tokens/', view_func=TokensApi.as_view('token_api'), methods=['POST'])
