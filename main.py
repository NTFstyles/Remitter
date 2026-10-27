from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
app=Flask(__name__)
Bootstrap(app)
app.secret_key='ajrncccgccbcvsatcasyuc'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dashboard.db"
db=SQLAlchemy(app)
class Login(FlaskForm):
    # username=StringField('Username', validators=[DataRequired(message='Username is Required'), Length(min=3, max=15, message='Username must be between 3 to 15 characters long')])
    email=EmailField('Email', validators=[DataRequired(message='Email is Required'), Email(message='Email address must include @')])
    password=PasswordField('Password', validators=[DataRequired(message='Password is required'), Length(min=5, max=15, message='Password must be between 5 to 15 characters long')])
    # confirm_password=PasswordField('Confirm your Password', validators=[EqualTo('password', message='Password do not match')])
    submit=SubmitField('Submit')

class Dashboard(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(30), unique=True, nullable=False)
    email=db.Column(db.String(30), unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)

class Signin(FlaskForm):
    username=StringField('Username', validators=[DataRequired(message='Username is required'), Length(min=3, max=15, message='Username must be between 3 to 15 characters long')])
    email=EmailField('Email', validators=[DataRequired(message='Email is Required'), Email(message='Email address must include @')])
    password=PasswordField('Password', validators=[DataRequired(message='Password is required'), Length(min=5, max=15, message='Password must be between 5 to 15 characters long')])
    confirm_password=PasswordField('Confirm your password', validators=[EqualTo('password', message='Password do not match')])
    submit=SubmitField('Create your new account')




@app.route('/login', methods=['POST', 'GET'])
def login():
    form=Login()
    all_email=[]
    all=db.session.query(Dashboard).all()
    for a in all:
        all_email.append(a.email)
    if form.validate_on_submit():
        if form.email.data in all_email:
            
            record=Dashboard.query.filter_by(email=form.email.data)
            for i in record:
                if i.email==form.email.data and i.password==form.password.data:
                    return "<h2>Login successful</h2>"
                else:
                    return "<h2>Incorrect email or password</h3>"
    
        else:     
            return "<p>please consider creating an account with us</p>"

    return render_template('login.html', form=form)


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    all_email=[]
    all=db.session.query(Dashboard).all()
    for a in all:
        all_email.append(a.email)
    form=Signin()
    if form.email.data in all_email:
        return "<h2>This Account already exist, Login in instead</h2>"
    elif form.validate_on_submit():
        new_user=Dashboard(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('signin.html', form=form)


@app.route('/')
def home():
    return render_template('home.html')

if __name__=="__main__":
    with app.app_context():
        db.create_all()
        all_email=[]
        all=db.session.query(Dashboard).all()
        for a in all:
            all_email.append(a.email)

        
    app.run(debug=True)