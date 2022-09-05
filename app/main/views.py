from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, request, session, abort
from . import main
from flask_login import login_required, current_user
from app.models import Permission


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')


@main.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')


@main.route('/info')
@login_required
def info():
    return render_template('info.html')


@main.route('/admin_hub')
@login_required
def admin_hub():
    # checks if the user has the right permissions before granting access to the page or aborting with a 403 error
    if current_user.can(Permission.ADMIN):
        return render_template('admin_hub.html')
    else:
        abort(403)
