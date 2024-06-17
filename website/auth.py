from flask import Blueprint, redirect, render_template, request, flash, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

''''''
from flask import Flask, session, g
import psycopg2
DB_HOST = 'database-tour.cluster-ro-crln8mpfedqu.ap-northeast-2.rds.amazonaws.com'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWD = 'lightening123$'
DB_PORT = 5432

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWD, port=DB_PORT)
    return db
''''''
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            return redirect(url_for('views.home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))
