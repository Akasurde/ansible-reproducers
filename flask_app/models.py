from app import db
from flask_login import UserMixin
from sqlalchemy import event


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwd = db.Column(db.String(300), nullable=False, unique=True)
    ansible_vault = db.Column(db.String(300), nullable=False, unique=True)

    def __repr__(self):
        return "<User %r>" % self.username


class Hosts(db.Model):
    __tablename__ = "hosts"
    id = db.Column(db.Integer, primary_key=True)
    os = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


@event.listens_for(Hosts.__table__, "after_create")
def create_hosts(*args, **kwargs):
    with open("linux.pwd", "r") as f:
        password = f.read()
    db.session.add(Hosts(os="linux", password=password))
    db.session.add(Hosts(os="windows", password=password))
    db.session.commit()
