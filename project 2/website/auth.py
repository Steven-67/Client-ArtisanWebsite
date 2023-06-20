from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                if user.is_client:
                    return redirect(url_for('views.client_page'))
                elif user.is_artisan:
                    return redirect(url_for('views.artisan_page'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html')

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        is_client = role == 'client'
        is_artisan = role == 'artisan'

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password), is_client=is_client, is_artisan=is_artisan)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please login.', category='success')
            return redirect(url_for('auth.login'))

    return render_template('sign_up.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', category='success')
    return redirect(url_for('views.home'))
