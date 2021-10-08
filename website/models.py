from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import re
from time import time
import os
  


class Note(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    
    role = db.Column(db.String(50))
    notes = db.relationship('Note',  backref="author", lazy=True)
    schedule = db.relationship('Schedule', backref="user")
    
class Schedule(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(50))
    file_name = db.Column(db.String(50), unique=True)
    author = db.Column(db.String, db.ForeignKey('user.first_name'), nullable=False)
    
    
    


    