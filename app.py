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

# Create new user
@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    existing_user = SupaUser.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 200

    new_user = SupaUser(email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'}), 201

#Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = SupaUser.query.all()
    users_list = [{'id': user.id, 'email': user.email} for user in users]
    return jsonify(users_list)

#Get user_id by email
@app.route('/get_user_id', methods=['GET'])
def get_user_id():
    email = request.args.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = SupaUser.query.filter_by(email=email).first()

    if user:
        return jsonify({'id': user.id}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

####################################################################

# Create new event
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    print(data) 
    
    organizer = SupaUser.query.get_or_404(data['organizer_id'])

    start_time_str = data['start_time'].replace('Z', '')
    end_time_str = data['end_time'].replace('Z', '')

    new_event = Event(
        title=data['title'],
        description=data.get('description', ''),
        start_time=datetime.fromisoformat(start_time_str),
        end_time=datetime.fromisoformat(end_time_str),
        organizer_id=organizer.id,
        google_event_id=data.get('google_event_id')
    )

    attendee_emails = data.get('attendees', [])
    for email in attendee_emails:
        user = SupaUser.query.filter_by(email=email).first()
        if user:
            new_event.attendees.append(user)

    db.session.add(new_event)
    db.session.commit()
    
    return jsonify({'message': 'Event created successfully!', 'event_id': new_event.id}), 201

# Get events by user_id
@app.route('/events/<int:user_id>', methods=['GET'])
def get_events(user_id):
    events = Event.query.filter(
        (Event.organizer_id == user_id) | (Event.attendees.any(id=user_id))
    ).all()

    events_list = [{
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'start_time': event.start_time.isoformat(),
        'end_time': event.end_time.isoformat(),
        'organizer_id': event.organizer_id,
        'attendees': [user.id for user in event.attendees],
        'google_event_id' : event.google_event_id
    } for event in events]
    return jsonify(events_list)

#Edit event / Update Event
@app.route('/events/<int:event_id>', methods=['PUT'])
def edit_event(event_id):
    data = request.get_json()
    event = Event.query.get_or_404(event_id)

    organizer_id = data.get('organizer_id')
    if not organizer_id:
        return jsonify({'error': 'Organizer ID is required'}), 400

    if event.organizer_id != organizer_id:
        return jsonify({'error': 'Only the organizer can edit this event'}), 403

    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    
    if 'start_time' in data:
        event.start_time = datetime.fromisoformat(data['start_time'].replace('Z', ''))
    if 'end_time' in data:
        event.end_time = datetime.fromisoformat(data['end_time'].replace('Z', ''))
    if 'attendees' in data:
        new_attendees = []
        for email in data['attendees']:
            user = SupaUser.query.filter_by(email=email).first()
            if user:
                new_attendees.append(user)
        event.attendees = new_attendees

    db.session.commit()
    return jsonify({'message': 'Event updated successfully!'}), 200

# Delete event
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    organizer_id = request.args.get('organizer_id', type=int)
    
    if organizer_id is None:
        return jsonify({'error': 'Organizer ID is required as query parameter'}), 400

    event = Event.query.get_or_404(event_id)

    if event.organizer_id != organizer_id:
        return jsonify({'error': 'Only the organizer can delete this event'}), 403

    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)