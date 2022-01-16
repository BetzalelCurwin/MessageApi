from flask import jsonify, request
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError
from app.main import app
import database.database as db
from schemas.schemas import MessageSchema
from models.models import Message

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)


@app.route('/messages/unread')
@jwt_required()
def get_unread_messages():
    """
    returns list of all unread messages for current user
    """

    messages = messages_schema.dump(db.get_unread_messages(current_user))
    return jsonify(messages)


@app.route('/messages/<int:message_id>', methods=['GET', 'DELETE'])
@jwt_required()
def update_message(message_id):
    """
    read or delete a specific message by its id
    :param message_id:
    """

    message_entry = db.get_message_entry(message_id, current_user.id)

    if not message_entry:
        return jsonify("could not find message"), 404

    if request.method == 'GET':
        return message_schema.dump(db.read_message(message_entry))

    if request.method == 'DELETE':
        db.delete_message(message_entry)
        return jsonify("deleted successfully")


@app.route('/messages')
@jwt_required()
def get_messages():
    """
    returns a list of all messages for current user
    """

    messages = messages_schema.dump(db.get_all_messages(current_user))
    return jsonify(messages)


@app.route('/message', methods=['POST'])
@jwt_required()
def send_message():
    """
    creates message and returns it
    """

    data = request.form
    print(data)
    email = data.get('to_email', None)
    if not email:
        return jsonify("to email not included"), 400

    to_user = db.get_user_by_email(email)
    if not to_user:
        return jsonify("user not found"), 400

    try:
        result = message_schema.load({**data, 'sender_id': current_user.id, 'receiver_id': to_user.id})
    except ValidationError as e:
        return e.messages, 400

    message = db.add_message(Message(**result))
    return message_schema.dump(message)
