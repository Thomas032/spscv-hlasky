from flask import Blueprint, render_template,request, jsonify
from flask_login import  login_required, current_user


views  = Blueprint('views', __name__)



@views.route('/', methods=['GET', 'POST']) 
def home():
    return render_template("home.html", user=current_user, profile="Home", school=False)  

@views.route('/admin')
@login_required
def admin():
    test = current_user
    better = str(test)[1:-1]
    return render_template("home.html", author=better, user=current_user, profile="Home", hsh="admin")

