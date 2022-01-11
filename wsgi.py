from app.main import app, db, User

db.create_all()

user1 = User(email='email1')
user2 = User(email='email2')
db.session.add(user1)
db.session.add(user2)
db.session.commit()


if __name__ == "__main__":
    app.run()