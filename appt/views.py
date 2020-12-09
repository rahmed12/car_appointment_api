'''
This is where we bind our url routes to our method classes using Pluggable Views
'''
from flask import Blueprint

from appt.api import ApptsApi

appts_app = Blueprint('appts_app', __name__)



# our GET endpoint needs a rec id but to get all recs we don't need the id
# set it to None to get all values
appts_app.add_url_rule('/appts/', defaults={'appt_id': None}, view_func=ApptsApi.as_view('appts_get'), methods=['GET'])
appts_app.add_url_rule('/appts/', view_func=ApptsApi.as_view('appts_post'), methods=['POST'])
appts_app.add_url_rule('/appts/<appt_id>', view_func=ApptsApi.as_view('appts_crud'), methods=['PUT','GET','DELETE'])
