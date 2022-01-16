from app.main import app
import models.models
import schemas.schemas
import auth.jwt
import database.database
import routes.routes
from models.models import db, User

try:
    print('starting')
    db.create_all()
    user1 = User(email='email1')
    user2 = User(email='email2')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
except Exception:
    pass


if __name__ == "__main__":
    app.run()