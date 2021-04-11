from flask import Blueprint, render_template,request, jsonify
from flask_login import  login_required, current_user
from .models import Note
from . import db
from flask import flash
import json
import random
from .auth import login

views  = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST']) 
def home():
    return render_template("home.html", user=current_user, profile="Home" )  

secret = random.randint(1,4582545)
@views.route('/admin')
@login_required
def admin():
    test = current_user
    better = str(test)[1:-1]
    return render_template("home.html", author=better, user=current_user, profile="Home", hsh="admin")

