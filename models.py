from . import db

class users(db.Model):
    email = db.Column(db.String(255), primary_key=True)
    user = db.Column(db.String(255))
    password = db.Column(db.String(255))

class sms(db.Model):
    email = db.Column(db.String(255), primary_key=True)
    dateTime = db.Column(db.DateTime, primary_key=True)
    number = db.Column(db.String(50))
    message = db.Column(db.Text)
