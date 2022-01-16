from datetime import datetime
from models.models import User, MessageList, Message, db


def get_user_by_email(email) -> User:
    return User.query.filter_by(email=email).one_or_none()


def get_user_by_id(identity) -> User:
    return User.query.filter_by(id=identity).one_or_none()


def get_all_messages(user: User):
    return [entry.message for entry in user.message_list]


def get_unread_messages(user: User):
    return [entry.message for entry in user.message_list if not entry.read]


def add_message(message: Message) -> Message:
    message.created_at=datetime.now()
    to_entry = MessageList(user_id=message.receiver_id, message=message, read=False)
    from_entry = MessageList(user_id=message.sender_id, message=message, read=True)
    db.session.add(message)
    db.session.add(to_entry)
    db.session.add(from_entry)
    db.session.commit()
    return message


def delete_message(message_entry: MessageList) -> None:
    db.session.delete(message_entry)
    db.session.commit()


def read_message(message_entry: MessageList) -> Message:
    message_entry.read = True
    db.session.commit()
    return message_entry.message


def get_message_entry(message_id, user_id) -> MessageList:
    return MessageList.query.filter_by(message_id=message_id, user_id=user_id).one_or_none()





