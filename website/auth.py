from flask import Blueprint, render_template, request , flash, redirect, url_for, send_file
from .models import User
import datetime
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Schedule
from .models import Note
import os
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
 
@auths.route('/náš_rozvrh')
@login_required
def nase(): 
    return render_template("nase_rozvrhy.html", user=current_user, profile="r_nas", rozvrh='rozvrh.png' ) 
@auths.route('/učitelské_rozvrhy')
@login_required
def jejich(): 
    
    rozvrhy = Schedule.query.all() 
    return render_template("ucitelske_rozvrhy.html", user=current_user, profile="r_ost", rozvrhy=rozvrhy)
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
                    return redirect(url_for('auths.admin'))
                
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
        elif email == "tomas.bartos.cv@gmail.com" and first_name== "Tomáš":
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'), role="Admin")
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auths.admin')) #Needs to be change if admin is in auth !!
              
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'), role="Pleb")
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
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit() 

@auths.route('/delete-sched', methods=['POST', 'GET'])
@login_required
def delete_sched():
    if current_user.role == "Admin" or current_user.role == "Admin 2.0":
        sched = json.loads(request.data)
        schedId = sched['schedId']
        sched = Schedule.query.get(schedId)
        if sched:
            os.remove(os.path.join(r"website\static\rozvrhy", sched.file_name))
            db.session.delete(sched)
            db.session.commit() 
            flash(f"Schedule '{sched.file_name}' was successfully deleted!", category="success")
            return redirect(url_for('auths.admin'))
    else:
        return render_template("error.html", user=current_user)


    
@auths.route('/change-color', methods=['POST', 'GET'])
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
<<<<<<< HEAD

@auths.route("/admin", methods=['POST', 'GET'])
@login_required
def admin():
    if current_user.role == "Admin" or current_user.role== "Admin 2.0":
        print("Admin logged in!")
        if request.method == "POST":
            name = request.form.get('t_name')
            file = request.files['file']
            if 'file' not in request.files:
                flash('No file part', category="error")
                print("NO file")
                return redirect(url_for('auths.admin'))

            if file.filename == '':
                flash('No selected file', category="error")
                return redirect(url_for('auths.admin'))
            
            existing_file = Schedule.query.filter_by(file_name=file.filename).first() 
            if existing_file:
                flash("File already exists!",category="error") 
            else:
                new_schedule= Schedule(teacher_name=name, file_name=file.filename, author=current_user.id)
                db.session.add(new_schedule)
                db.session.commit()
                file.save(os.path.join(r"website\static\rozvrhy", file.filename))
                flash("Rozvrh byl úspěžně přidán")
                print(f"file : {file.filename} by {name} added successfully")
            
            
            
         
        first = current_user.first_name
        final = ""
        if first[-1] == 'š':
            final = first + "i"
        elif first[-1] == "d" or first[-1]=="b":
            final = first + "e"
        elif first[-1] == "a":
            final = final[len(final)-2]+"o"
            
        else:
            final = first
        
        rozvrhy = Schedule.query.all()  
        return render_template("admin.html", user = current_user,rozvrhy = rozvrhy, num=len(rozvrhy), oslovení=final)
    else:
        print("noob")
        return render_template("error.html", user =current_user)
    
@auths.route('/make_admin/<email>')
@login_required
def adminify(email):
    
    if current_user.role == "Admin":
        profile = User.query.filter_by(email=email).first()
        if profile and profile.role!="Admin 2.0":
            
            profile.role = "Admin 2.0"
            db.session.commit()
            flash(f"User {email} is now Admin 2.0!", category="success")
            return redirect(url_for('auths.admin'))
        else:
            flash(f"User {email} can not be found or he is already admin 2.0.", category="error")
            return redirect(url_for('auths.admin'))
    else:
        return render_template("error.html", user=current_user)
    
@auths.route('/make_pleb/<email>')
@login_required
def plebify(email):
    
    if current_user.role == "Admin":
        profile = User.query.filter_by(email=email).first()
        if profile:
            print(profile.role)
            profile.role = "pleb"
            db.session.commit()
            flash(f"User {email} is now pleb!", category="success")
            return redirect(url_for('auths.admin'))
        else:
            flash(f"User {email} can not be found.", category="error")
            return redirect(url_for('auths.admin'))
    else:
        return render_template("error.html", user=current_user)
    
=======
>>>>>>> 13bdd04e7990c465c3ae359e84b07ca33782d6bf
