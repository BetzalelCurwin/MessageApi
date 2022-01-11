from datetime import datetime
from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, current_user, create_access_token, JWTManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'temporary-Secret-key-will-change-later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

jwt = JWTManager(app)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(40))
    created_at = db.Column(db.DateTime, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sender = db.relationship('User', backref='sent_messages', foreign_keys=[sender_id])
    receiver = db.relationship('User', backref='received_messages', foreign_keys=[receiver_id])

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class MessageList(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), primary_key=True)
    message = db.relationship('Message', backref='message_lists', foreign_keys=[message_id])
    sender = db.relationship('User', backref='message_list', foreign_keys=[user_id])
    read = db.Column(db.Boolean, nullable=False)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data):
    identity = jwt_data['sub']
    return User.query.filter_by(id=identity).one_or_none()


@app.route('/')
def hi():
    return "hello world!"


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    user = User.query.filter_by(email=email).one_or_none()
    if not user:
        return jsonify("no user with that email"), 401

    access_token = create_access_token(user)
    return jsonify(access_token=access_token)


@app.route('/messages/unread')
@jwt_required()
def get_unread_messages():
    messages = [entry.message.as_dict() for entry in current_user.message_list if not entry.read]
    return jsonify(messages)


@app.route('/messages/<int:message_id>', methods=['GET', 'DELETE'])
@jwt_required()
def update_message(message_id):
    message_entry = MessageList.query.filter_by(message_id=message_id, user_id=current_user.id).one_or_none()

    if not message_entry:
        return jsonify("could not find message"), 404

    if request.method == 'GET':
        message_entry.read = True
        db.session.commit()
        return message_entry.message.as_dict()

    if request.method == 'DELETE':
        db.session.delete(message_entry)
        return jsonify("deleted successfully")


@app.route('/messages')
@jwt_required()
def get_messages():
    messages = [entry.message.as_dict() for entry in current_user.message_list]
    return jsonify(messages)


@app.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    data = request.form
    message = Message()

    message.message = data.get('message', None)
    if not message.message:
        return jsonify("message not included"), 400

    message.subject = data.get('subject', None)
    if not message.subject:
        return jsonify("subject not included"), 400

    to_user = User.query.filter_by(email=data.get('to_email', None)).one_or_none()
    if not to_user:
        return jsonify("user to send to not included"), 400

    message.receiver_id = to_user.id
    message.created_at = datetime.now()
    message.sender_id = current_user.id
    to_entry = MessageList(user_id=to_user.id, message=message)
    from_entry = MessageList(user_id=current_user.id, message=message)
    db.session.add(message)
    db.session.add(to_entry)
    db.session.add(from_entry)
    db.session.commit()
    return jsonify(message.as_dict())
