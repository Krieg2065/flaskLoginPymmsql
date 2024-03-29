
# all imports
from flask import render_template,redirect,url_for,request,flash,session
# app is flask object mag in init.py
# bcrypt is used for hashing passwords
# login manager package is used for loging functions
from hello import app,bcrypt,login_manager
# forms made by flask_forms in form.py module
from .form import loginform,signupform,AddVerificaform
# db helper class deals with databse connections and queries
from .db import DBHelper
# 
from flask_login import  login_required, login_user, logout_user ,current_user
# User is basically model for logi funtions
from .models import User
import io


# route for '/' page which requires log in
@login_required
@app.route('/')
def hello():
    if current_user.is_authenticated:
        db=DBHelper()
        sql='SELECT * FROM scuola.verifica2'
        row=db.fetch(sql, data=None)
        return render_template('index.html',data=row,title='Home')
    else:
        return redirect(url_for('login'))

# login method
@app.route('/login',methods=['GET','POST'])
def login():
    # check if user loged in then go to home page which is "/"
    if current_user.is_authenticated:
        return redirect((url_for("hello")))
    else:
        # first  send form from "form class" to login.html
        form=loginform()
        # checks from is using POST method
        if form.validate_on_submit():
            # object of DBHelper class
            db=DBHelper()
            # statement for sql cmnd
            sql="SELECT * FROM docente where useremail like %s"
            # fetch function is called which returns query data
            row=db.fetch(sql, form.email.data,1)
            # passed data to User model and created instance 
            user=User(row[0], row[1], row[2], row[3])
            # checks if any user n "user" and also checks password check which is hashed
            if user and bcrypt.check_password_hash(user.password, form.password.data) :
                # pass that user instance to login user object
                login_user(user)
                return redirect(url_for('hello'))
            else:
                flash("invalid credentials")        
        return render_template('login.html',form=form,title='login')
# route for register
@login_required
@app.route('/aggiungiVerifica',methods=['GET','POST'])
def AggiungiVerifica():
    if current_user.is_authenticated:
        form=AddVerificaform()
        if form.validate_on_submit():
            testo =form.testo.data
            griglia=form.griglia.data
            argomento=form.argomento.data
            materia=form.materia.data
            print(form.testo_pdf.data)
            testo_pdf= form.testo_pdf.read()
            #testo_pdf= io.BytesIO(form.testo_pdf.data)
            stmt = "SELECT * FROM docente where useremail like %s"
            db=DBHelper()
            qedit="insert into scuola.verifica2(testo,griglia,argomento,materia,testo_pdf) values (%s, %s, %s, %s, %s)"
            data=(testo,griglia,argomento,materia,testo_pdf)
            db=DBHelper()
            row=db.adddata(qedit,data )
            flash("Verifica aggiunta")
            return redirect(url_for('hello'))
        return render_template('aggiungiVerifica.html',form=form,title="aggiungiVerifica")

@login_required
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect((url_for("hello")))
    else:
        form=signupform()
        if form.validate_on_submit():
            username =form.username.data
            email=form.email.data
            nome=form.nome.data
            cognome=form.cognome.data
            hashedpassword=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            stmt = "SELECT * FROM docente where useremail like %s"
            db=DBHelper()
            row=db.fetch(stmt,form.email.data,True )
            if row:
                flash("email already registered")
                return redirect(url_for('register'))
            else:
                qedit="insert into docente(userName,userEmail,userPass,nome,cognome) values (%s, %s, %s, %s, %s)"
                data=(username,email,hashedpassword,nome,cognome)
                db=DBHelper()
                row=db.adddata(qedit,data )
                flash("registeration succesful")
            return redirect(url_for('login'))
    return render_template('reg.html',form=form,title="register")

# route for logout
@login_required
@app.route('/logout')
def logout():
    logout_user()
    flash("logged out")
    return redirect(url_for('login'))

@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')
     
@login_manager.user_loader
def load_user(userid):
    sql='SELECT * from docente where ID = %d'
    db=DBHelper()
    row=db.fetch(sql, userid,True)
    users=User(row[0], row[1], row[2], row[3]) 
    return users