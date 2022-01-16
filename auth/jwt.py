from flask import request, jsonify
from flask_jwt_extended import create_access_token, JWTManager
from app.main import app
import database.database as db


jwt = JWTManager(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data):
    identity = jwt_data['sub']
    return db.get_user_by_id(identity)


@app.route('/login', methods=['POST'])
def login():
    """
    send email of user in order to get access token
    :return:
    access token
    """

    email = request.form.get('email', None)
    user = db.get_user_by_email(email)
    if not user:
        return jsonify("no user with that email"), 401

    access_token = create_access_token(user)
    return jsonify(access_token=access_token)


