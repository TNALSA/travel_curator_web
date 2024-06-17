
import requests
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import subprocess
import sys
# import models

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:lightening123$@database-tour.cluster-ro-crln8mpfedqu.ap-northeast-2.rds.amazonaws.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# models.db.init_app(app)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)

class TravelPackage(db.Model):
    __tablename__ = 'packages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
    guide = db.Column(db.String, nullable=False)
    people = db.Column(db.Integer, nullable=False)
    theme = db.Column(db.String, nullable=False)

def get_recommendations():
    result = subprocess.run([sys.executable, 'recommend.py'], capture_output=True, text=True)
    recommendations = result.stdout.strip().split('\n')
    return recommendations

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/travel_packages', methods=['GET'])
def travel_packages():
    PER_PAGE = 3
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    country = request.args.get('country')
    city = request.args.get('city')
    price_range = request.args.get('price_range')
    guide = request.args.get('guide')
    people = request.args.get('people')
    
    query = TravelPackage.query
    
    if start_date:
        query = query.filter(TravelPackage.start_date >= start_date)
    
    if end_date:
        query = query.filter(TravelPackage.end_date <= end_date)
    
    if country:
        query = query.filter(TravelPackage.country == country)
    
    if city:
        query = query.filter(TravelPackage.city == city)
    
    if price_range:
        query = query.filter(TravelPackage.price <= price_range)
    
    if guide:
        query = query.filter(TravelPackage.guide == guide)
    
    if people:
        query = query.filter(TravelPackage.people == people)
    
    total_packages = query.count()
    packages = query.offset((page - 1) * PER_PAGE).limit(PER_PAGE).all()
    
    total_pages = (total_packages + PER_PAGE - 1) // PER_PAGE
    page_numbers = list(range(1, total_pages + 1))
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    query_string = request.query_string.decode().replace(f'page={page}', '').replace('&&', '&').strip('&')

    recommendations = get_recommendations()
    
    return render_template('travel_packages.html', packages=packages, page=page, page_numbers=page_numbers, prev_page=prev_page, next_page=next_page, query_string=query_string, recommendations=recommendations)

@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = session['username']
    user = User.query.filter_by(username=user_id).first()

    if request.method == 'POST':
        user.email = request.form['email']
        user.full_name = request.form['full_name']
        db.session.commit()

    return render_template('mypage.html', user=user)

@app.route('/my_coupons')
def my_coupons():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = session['username']
    coupons = []  # Fetch user's coupons from the database
    return render_template('my_coupons.html', user_id=user_id, coupons=coupons)

# @app.route('/issue_coupon', methods=['POST'])
# def issue_coupon():
#     if 'username' not in session:
#         return redirect(url_for('login'))
#     if request.method == 'POST':
#         user_id = session['username']
#         db = get_db()
#         cursor = db.cursor()
#
#         cursor.execute('SELECT * FROM coupons ORDER BY id LIMIT 1')
#         coupon = cursor.fetchone()
#
#         if coupon:
#             coupon_id, coupon_code, expiration_date = coupon
#             cursor.execute("INSERT INTO user_coupons (user_id, coupon_code, expiration_date) VALUES (user_id, coupon_code, expiration_date);")
#             db.commit()
#             cursor.execute('DELETE FROM coupons WHERE id = %s', (coupon_id,))
#             db.commit()
#             app.logger.info(f'Coupon {username} got coupon {coupon_id}')
#             message = "쿠폰이 발급되었습니다: {coupon_code}"
#         else:
#             app.logger.info(f'Coupon sold out')
#             message = "발급 가능한 쿠폰이 없습니다."
#
#         return render_template('issue_coupon.html', message=message)
#
#     return render_template('issue_coupon.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
