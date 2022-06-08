from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TelField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import smtplib
import os
# from dotenv import load_dotenv

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRETKEY')
gmail = os.getenv('EMAIL')
pw = os.getenv('PW')

class InfoForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    phone = TelField('Phone:', validators=[DataRequired()])
    email = EmailField('Email:', validators=[DataRequired()])
    comments = TextAreaField('Comments:')
    submit = SubmitField('Submit')

class ClientPortal(FlaskForm):
    username = StringField('User Name:', validators=[DataRequired()])
    password = StringField('Password:', validators=[DataRequired()])
    login = SubmitField('Log In')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/contact-us', methods=['GET', 'POST'])
def contact():
    name = False
    phone = False
    email = False
    comments = False

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(gmail, pw)
    form = InfoForm()

    if form.validate_on_submit():
        session['name'] = form.name.data
        session['phone'] = form.phone.data
        session['email'] = form.email.data
        session['comments'] = form.comments.data
        server.sendmail(gmail, gmail, f"{form.name.data}, {form.phone.data}, {form.email.data}, {form.comments.data}")

        return redirect(url_for('thank_you'))
    return render_template('contact-us.html', form=form)

@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')

@app.route('/client-portal', methods=['GET', 'POST'])
def client_portal():
    username = False
    password = False
    form = ClientPortal()

    if form.validate_on_submit():
        session['username'] = form.username.data
        session['password'] = form.password.data

        return redirect(url_for('login_failure'))
    return render_template('client-portal.html', form=form)

@app.route('/login-failure')
def login_failure():
    return render_template('login-failure.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))