from flask import Blueprint, render_template, request , flash, redirect, url_for, send_file
from .models import User
import datetime

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Note

import json
from flask_login import login_user, login_required, logout_user, current_user


auths  = Blueprint('auths', __name__)


@auths.route('/macháček') 
@login_required 
def macháček(): 
    return render_template("macháček.html", user=current_user, profile="Mach" ) 

@auths.route('/kubánková') 
@login_required 
def kubánková(): 
    return render_template("kubankova.html", user=current_user, profile="Kub" ) 

@auths.route('/ostatní') 
@login_required 
def other(): 
    return render_template("other.html", user=current_user, profile="Oth")

@auths.route('/učebnice') 
@login_required
def books(): 
    return render_template("books.html", user=current_user, profile="Book")  
 
@auths.route('/login',  methods=['GET', 'POST']) 
def login():
    if request.method == 'POST': 
        email = request.form.get('email') 
        password = request.form.get('password') 
        mem = request.form.get('memes')
        user = User.query.filter_by(email=email).first() 
        
        if user:      
            
            if check_password_hash(user.password, password): 
                flash('Přihlášeno úspěšně.', category='success') 
                login_user(user, remember=True) 
                
                if email == "tomas.bartos.cv@gmail.com" and mem!="on":
                    return redirect(url_for('views.admin'))
                
                if email == "tomas.bartos.cv@gmail.com" and mem == "on":
                    return redirect(url_for('auths.school'))
                
                if mem!= "on": 
                    return redirect(url_for('views.home')) 
                
                else: 
                    return redirect(url_for('auths.school'))  
                              
            else:
                flash('Špatně zadané heslo, zkuste znovu', category='error') 
                
        else:
            flash('Email neexistuje', category='error') 
            
    return render_template("login.html", user=current_user, profile="log") 

@auths.route('/logout') 
@login_required 
def logout(): 
    logout_user() 
    return redirect(url_for('auths.login')) 

@auths.route('/sign-up',  methods=['GET', 'POST']) 
def sign_up():
    if request.method == 'POST' : 
        email = request.form.get('email')
        first_name = request.form.get('firstName') 
        password1 = request.form.get('password1') 
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first() 
        col = request.form.get('color')
        
        if user:
            flash('Email již existuje', category='error') 
            #color code is 60, 222, 16
            # color code to hex is #3cde10

        elif len(email) < 4:
            flash(f'Délka vašeho emailu je {len(email)} charaktery dlouhé, ale musí být větší než 4', category='error')
            
        elif len(first_name) <2:
            flash('Email musí být větší než 4 charaktery', category='error')

        elif password1 != password2:
            flash("Vaše hesla se neshodují.", category='error')
            
        elif len(password1) < 7:
            flash(f'Sorry vaše heslo má{len(password1)} charaktery/ú dlouhé ale musí být větší než 8', category='error')
            
        elif col != "#3cde10":
            flash(f"Sorry váš autentikační kód je {col}, což není správně!", category="error")
            
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'), background="#fffff")
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
                                 
    return render_template("sign_up.html", user=current_user, profile="sign") 


@auths.route('/úkoly', methods=['GET', 'POST'])
@login_required
def work():
    if request.method == 'POST':
        note = request.form.get('note')
        dat = request.form.get('datum')
        
        if len(note) <=1:
            flash('Note is too short', category='error')
            
        else: 
            new_note = Note(data=note,date=dat,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Úkol přidán úspěšně', category='success')
    
    return render_template('homework.html', user=current_user, profile="Work")
    
@auths.route('/PohlDrive', methods=['GET', 'POST'])
@login_required
def PohlDrive():
    return render_template("PohlDrive.html", user=current_user, profile="Pohl")

@auths.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    

    
    
@auths.route('/change-color', methods=['POST'])
def change_color():
    data = json.loads(request.data)
    color = data['color']
    print(color)
    if color:
        user = current_user
        user.background = color
        db.session.commit()
        
        
@auths.route("/school")
@login_required
def school():
    return render_template('home.html', user = current_user, profile="Home", school=True)