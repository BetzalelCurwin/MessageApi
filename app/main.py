from flask import Flask

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'temporary-Secret-key-will-change-later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messageapi.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


