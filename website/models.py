from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import re
from time import time
  
def slugify(s):
    patters = r'[^\w+]'
    return re.sub(pattern, '-', s)

class Note(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    slug = db.Column(db.String(150), unique=True)  
    body = db.column(db.Text)  
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()
        
    def generate_slug():
        if self.title:
            self.slug= slugify(self.title)
        else:
            self.slug = str(int(time()))
    def __repr__(self):
        return f"<Post Id: {self.id}, Title: {self.title}>"        
    
    