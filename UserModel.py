from flask_sqlalchemy import SQLAlchemy
from settings import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    password = db.Column(db.String(80), nullable=False)


    def username_password_match(_username, _password):
        user = db.session.query(User).filter_by(username=_username, password=_password).first()

        return bool(user)


    def get_all_users():
        return db.session.query(User).all()


    def create_user(_username, _password):
        new_user = User(username=_username, password=_password)
        db.session.add(new_user)
        db.session.commit()


    def __repr__(self):
        return str({
            'username': self.username,
            'password': self.password
        })
