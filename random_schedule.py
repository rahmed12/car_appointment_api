
# Schedule Library imported
import uuid
from datetime import datetime, timedelta
import schedule
import time
import random

from application import create_app as create_base_settings
from settings import MONGODB_HOST, MONGODB_DB
from appt.models import Appts


def create_app():

    db_settings = {
        'DB': MONGODB_DB,
        'HOST': MONGODB_HOST
    }
    return create_base_settings(
        MONGODB_SETTINGS=db_settings,
        TESTING=True,
        WTF_CSRF_ENABLED=False, # we don't need csrf protection in unit testing
        SECRET_KEY = 'hushy', # used to encrypt sessions objects
    )



def job(app):

    now = datetime.utcnow().replace(second=0, microsecond=0)
    future_date = now + timedelta(days=random.randrange(5, 10), hours=(random.randrange(1, 24)))
    appt = Appts(
        external_id=str(uuid.uuid4()),
        first_name='Random',
        last_name='appointment',
        service='random service',
        status='open',
        street_address='random street',
        city='random city',
        state='random state',
        zip='random zip',
        phone='random phone',
        date=future_date,
        price='1.0'
    ).save()





if __name__ == "__main__":
    app = create_app()
    schedule.every(1).seconds.do(job, app)
    
    while True:
        schedule.run_pending()
        time.sleep(random.randrange(1, 30))
