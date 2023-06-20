from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(150))
    is_client = db.Column(db.Boolean, default=False)
    is_artisan = db.Column(db.Boolean, default=False)
    notes = db.relationship('Note', backref='user', cascade='all, delete')
    artisans = db.relationship('Artisan', backref='user', cascade='all, delete')

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    is_client = db.Column(db.Boolean, default=True)  # Add the is_client column

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_client = db.Column(db.Boolean, default=True)  # Add the is_client column

class Artisan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    services = db.Column(db.String(120), nullable=False)
    profile_picture = db.Column(db.String(120), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    sample_works = db.relationship('SampleWork', backref='artisan', cascade='all, delete')
    is_client = db.Column(db.Boolean, default=False)  # Add the is_client column

class SampleWork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artisan_id = db.Column(db.Integer, db.ForeignKey('artisan.id'))
    file_path = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='sample_work', cascade='all, delete')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sample_work_id = db.Column(db.Integer, db.ForeignKey('sample_work.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
