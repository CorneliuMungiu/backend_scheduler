from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

db = SQLAlchemy()
app = Flask(__name__)

CORS(app)  


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres.gckjglzhldumgqqvhnao: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@aws-0-us-east-2.pooler.supabase.com:5432/postgres"
db.init_app(app)

event_attendees = db.Table('event_attendees',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('supa_user.id'), primary_key=True)
)

class SupaUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey('supa_user.id'), nullable=False)
    attendees = db.relationship('SupaUser', secondary=event_attendees, backref='events_attending', lazy='subquery')
    google_event_id = db.Column(db.String)


with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/')
def hello_world():
    return 'Scheduler API is running!'