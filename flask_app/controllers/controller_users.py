from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.model_user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    session['user_id'] = ""
    session['first_name'] = ""
    session['last_name'] = ""
    session['email'] = ""
    session['login_email'] = ""
    return render_template('index.html')

@app.route("/register", methods=["POST"])
def register():
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    user = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['password_confirmation']
    }
    valid = User.validate_user(user)
    if valid:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        user['pw_hash'] = pw_hash
        user_id = User.add_user(user)
        session['user_id'] = user_id
        return redirect("/marketplace")
    return render_template("index.html", user = user)


@app.route("/login", methods=["POST"])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid email or Password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['login_password']):
        flash("Invalid email or Password", "login")
        return redirect('/')
    session['login_email'] = user.email
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    if 'user_id' not in session:
        return redirect('/')
    return redirect("/marketplace")


@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")