from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,FileField
from wtforms.validators import DataRequired,Email,EqualTo



class loginform(FlaskForm):
    email=StringField('email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('submit')

class signupform(FlaskForm):
    username=StringField('username',validators=[DataRequired()])
    username=StringField('username',validators=[DataRequired()])
    email=StringField('email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    nome=StringField('nome',validators=[DataRequired()])
    cognome=StringField('cognome',validators=[DataRequired()])
    submit=SubmitField('submit')

class AddVerificaform(FlaskForm):
    testo = StringField('testo')
    griglia = StringField('griglia',validators=[DataRequired()])
    argomento = StringField('argomento',validators=[DataRequired()])
    materia = StringField('materia',validators=[DataRequired()])
    testo_pdf = FileField('testo_pdf')
    submit=SubmitField('submit')
