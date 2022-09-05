from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, request, session, current_app
from . import auth
from .forms import LoginForm, RegisterForm
from .. import db
from ..models import User, Role
import bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from app.email import send_email


'''
The auth.login route is accessed,it initiate an instance of the LoginForm() class, if no form validation is passed
meaning a GET request then it simply sends across the form data and renders the login page to the view. If form
validation is successful, a POST request then;
- it checks to see if the user is exists and if the associated password is valid if YES then;
- it passes this to the flask-login.login_user
- it checks the url to confirm if the request came with a redirect url
- if there was a redirect url it redirects to this url and flashes a successful message.
'''


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if user is already authenticated prevent them from accessing the login route
    if current_user.is_authenticated:
        flash('You already have an account, log out to sign into a different account', 'info')
        return render_template('home.html')

    # if user is not authenticated the below takes effect
    form = LoginForm()
    if form.validate_on_submit():  # this will validated to true for a POST request only
        attempted_user = User.query.filter_by(username=form.username.data.lower()).first()
        if attempted_user is not None and attempted_user.verify_password(form.password.data):
            login_user(attempted_user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.home')
            flash('Login Successful', 'success')
            return redirect(next)
        flash('Incorrect username/password', 'danger')
    return render_template('auth/login.html', form=form)


# use a get and post request, the later to handle form submissions
@auth.route('/register', methods=['GET', 'POST'])
def register():
    # if user is already authenticated prevent them from accessing the register route
    if current_user.is_authenticated:
        flash('You already have an account, log out to register a new account', 'info')
        return render_template('home.html')

    form = RegisterForm()
    # the below will return true only for a POST request and if the form inputs are validated
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(),
                    email=form.email.data.lower(),
                    password=form.password.data)
        # pass data to password not password_hash to ensure encryption
        # user.role = admin_role
        try:
            db.session.add(user)
            print(current_app.config['APP_ADMIN'])
            db.session.commit()
        except:
            db.session.rollback()
            flash('Registration Unsuccessful', 'danger')
            return redirect(url_for('auth.register'))
        token = user.generate_confirmation_token()
        send_email(user.email, 'New User', 'auth/email/account_confirmation', user=user, token=token)
        flash(f"Hi {user.username.capitalize()} your registration was successful. A confirmation mail has been sent to your registered email address {user.email.upper()}, please confirm your email address before proceeding to log in below", 'success')
        return redirect(url_for('auth.login'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error encountered: {err_msg}', 'danger')
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out', 'success')
    return redirect(url_for('main.home'))


# view function to confirm new accounts
@auth.route('/confirm/<token>')
@login_required
def confirm_account(token):
    if current_user.confirmed:
        return redirect(url_for('main.home'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Your account has been confirmed!', 'success')
    else:
        flash('The link is invalid or has expired.', 'danger')
    return redirect(url_for('main.home'))


# this view intercepts a request when the below conditions are true:
# a user logged in(current_user.is_authenticated is True
# the user account is not confirmed
# the request URL is outside of the auth blue print and is not a static file
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.blueprint != 'auth' \
            and request.endpoint != 'static' \
            and request.endpoint != 'main.home':
        return redirect(url_for('auth.unconfirmed'))


# the before_request routes users to the below endpoint
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.home'))
    return render_template('auth/unconfirmed.html')


# the below endpoint is handles token regeneration for unconfirmed users
@auth.route('/resend_confirmation')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/account_confirmation',
               user=current_user, token=token)
    flash('A new confirmation email has been sent to your registered email', 'info')
    return redirect(url_for('main.home'))

