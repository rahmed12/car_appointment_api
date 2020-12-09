from application import db

class Appts(db.Document):
    external_id = db.StringField()
    first_name = db.StringField()
    last_name = db.StringField()
    service = db.StringField()
    status = db.StringField()
    street_address = db.StringField()
    city = db.StringField()
    state = db.StringField()
    zip = db.StringField()
    phone = db.StringField()
    date = db.DateTimeField()
    price = db.DecimalField(precision=2, rounding='ROUND_HALF_UP')
    live = db.BooleanField(default=True)

    meta = {
        'indexes': [('external_id', 'live'), ('date')]
    }
