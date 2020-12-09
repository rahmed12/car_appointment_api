from application import db

class AppAuth(db.Document):
    appauth_id = db.StringField( unique=True)
    appauth_sec = db.StringField()

    meta = {'indexes': [('appauth_id')]}


class Tokens(db.Document):
    appauth = db.ReferenceField(AppAuth) # foreign key
    token = db.StringField()
    expires = db.DateTimeField()
