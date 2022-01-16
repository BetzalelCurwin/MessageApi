from flask_sqlalchemy import SQLAlchemy
from app.main import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.DateTime)
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
