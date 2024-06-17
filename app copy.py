from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
import psycopg2
import logging
import os
# from flask_sqlalchemy import SQLAlchemy   
import subprocess


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/myDB'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class TravelPackage(db.Model):
#     __tablename__ = 'packages'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     country = db.Column(db.String, nullable=False)
#     city = db.Column(db.String, nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     start_date = db.Column(db.String, nullable=False)
#     end_date = db.Column(db.String, nullable=False)
#     guide = db.Column(db.String, nullable=False)
#     people = db.Column(db.Integer, nullable=False)
#     theme = db.Column(db.String, nullable=False)
    
    
app.secret_key = 'your_secret_key'

DB_HOST = 'database-tour.cluster-ro-crln8mpfedqu.ap-northeast-2.rds.amazonaws.com'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWD = 'lightening123$'
DB_PORT = 5432

LOG_DIR = '/opt/web/travel_curator/log'
if not os.path.isdir(LOG_DIR):
  os.mkdir(LOG_DIR)
  
logging.getLogger('werkzeug').disabled = True

# json_formatter = JsonFormatter({"level": "levelname", 
#                                     "message": "message", 
#                                     "loggerName": "name", 
#                                     "processName": "processName",
#                                     "processID": "process", 
#                                     "threadName": "threadName", 
#                                     "threadID": "thread",
#                                     "timestamp": "asctime"})
# json_handler.setFormatter(json_formatter)
    
    
logging.basicConfig(filename = f"{LOG_DIR}/server.log", level = logging.DEBUG
                  # , datefmt = '%Y/%m/%d %H:%M:%S %p'  # 년/월/일 시(12시간단위)/분/초 PM/AM
                  , datefmt = '%Y-%m-%d %H:%M:%S'  # 년/월/일 시(24시간단위)/분/초
                  , format = '{\'timestamp\' : \'%(asctime)s\', \'level\' : \'%(levelname)s\', \'message\' : %(message)s}')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWD, port=DB_PORT)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = get_db()
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.autocommit = True
        cursor = db.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            full_name TEXT NOT NULL
        )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS coupons (
            id SERIAL PRIMARY KEY,
            code TEXT NOT NULL,
            expiration_date TEXT NOT NULL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_coupons (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL,
            coupon_code TEXT NOT NULL,
            expiration_date TEXT NOT NULL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS travel_packages (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            city TEXT NOT NULL,
            price REAL NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            guide TEXT NOT NULL,
            people INTEGER NOT NULL,
            theme TEXT NOT NULL
        )
        ''')
        db.commit()
        #cursor.execute('DELETE FROM coupons')
        #cursor.execute('DELETE FROM user_coupons')
        #cursor.execute('DELETE FROM travel_packages')
        #cursor.execute('DELETE FROM users')

        #cursor.execute('''INSERT INTO users (username, password, email, full_name) VALUES ('user1', 'password1', 'user1@example.com', 'User One'), ('user2', 'password2', 'user2@example.com', 'User Two');''')

        #cursor.execute('''INSERT INTO coupons (code, expiration_date) VALUES ('ABC123', '2024-12-31'),('XYZ789', '2024-12-31'),('LMN456', '2024-12-31');''')

        cursor.execute('''INSERT INTO travel_packages (name, country, city, price, start_date, end_date, guide, people, theme) VALUES
            ('Fishing Adventure', 'Canada', 'Vancouver', 1200.0, '2024-06-01', '2024-06-10', 'Y', 4, 'Fishing'),
            ('Golf Retreat', 'Scotland', 'Edinburgh', 1500.0, '2024-07-01', '2024-07-10', 'N', 2, 'Golf'),
            ('Elderly Care Tour', 'Japan', 'Kyoto', 1800.0, '2024-08-01', '2024-08-10', 'Y', 5, 'Care'),
            ('Activity Expedition', 'Australia', 'Sydney', 2000.0, '2024-09-01', '2024-09-10', 'Y', 3, 'Activity'),
            ('Relaxing Getaway', 'Maldives', 'Male', 2500.0, '2024-10-01', '2024-10-10', 'N', 2, 'Relaxation'),
            ('City Tour', 'France', 'Paris', 1700.0, '2024-11-01', '2024-11-10', 'N', 4, 'Tourism'),
            ('Cultural Experience', 'India', 'Delhi', 1600.0, '2024-12-01', '2024-12-10', 'Y', 3, 'Cultural'),
            ('Adventure Safari', 'Kenya', 'Nairobi', 2200.0, '2024-01-01', '2024-01-10', 'Y', 6, 'Safari'),
            ('Hiking Trip', 'Nepal', 'Kathmandu', 1400.0, '2024-02-01', '2024-02-10', 'N', 3, 'Hiking'),
            ('Cruise Voyage', 'Italy', 'Rome', 3000.0, '2024-03-01', '2024-03-10', 'Y', 8, 'Cruise');'''
                           )

        db.commit()

init_db()

@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/')
# def sindex():
#     return render_template('s_index.html')

@app.route('/login', methods=['GET', 'POST'])
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
            app.logger.info(f'Login Success {username}')
            return redirect(url_for('home'))
        else:
            app.logger.error(f'Login Failed {username}')
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    app.logger.info(f'Logout {username}')
    return redirect(url_for('home'))

@app.route('/issue_coupon', methods=['GET', 'POST'])
def issue_coupon():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = session['username']
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM coupons ORDER BY id LIMIT 1')
        coupon = cursor.fetchone()
        
        if coupon:
            coupon_id, coupon_code, expiration_date = coupon
            cursor.execute("INSERT INTO user_coupons (user_id, coupon_code, expiration_date) VALUES (user_id, coupon_code, expiration_date);")
            db.commit()
            cursor.execute('DELETE FROM coupons WHERE id = %s', (coupon_id,))
            db.commit()
            app.logger.info(f'Coupon {username} got coupon {coupon_id}')
            message = f"쿠폰이 발급되었습니다: {coupon_code}"
        else:
            app.logger.info(f'Coupon sold out')
            message = "발급 가능한 쿠폰이 없습니다."
        
        return render_template('issue_coupon.html', message=message)
    
    return render_template('issue_coupon.html')

@app.route('/coupons')
def my_coupons():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = session['username']
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT coupon_code, expiration_date FROM user_coupons WHERE user_id = %s', (user_id,))
    coupons = cursor.fetchall()
    return render_template('coupons.html', user_id=user_id, coupons=coupons)

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
    
    db = get_db()
    cursor = db.cursor()
    
    query = 'SELECT name, country, city, price, start_date, end_date, guide, people, theme FROM travel_packages WHERE 1=1'
    count_query = 'SELECT COUNT(*) FROM travel_packages WHERE 1=1'
    log_params = {}
    params = []
    
    if start_date:
        query += ' AND start_date >= %s'
        count_query += ' AND start_date >= %s'
        params.append(start_date)
        log_params['start_date'] = start_date
    
    if end_date:
        query += ' AND end_date <= %s'
        count_query += ' AND end_date <= %s'
        params.append(end_date)
        log_params['end_date'] = end_date
    
    if country:
        query += ' AND country = %s'
        count_query += ' AND country = %s'
        params.append(country)
        log_params['country'] = country
    
    if city:
        query += ' AND city = %s'
        count_query += ' AND city = %s'
        params.append(city)
        log_params['city'] = city
    
    if price_range:
        query += ' AND price <= %s'
        count_query += ' AND price <= %s'
        params.append(price_range)
        log_params['price_range'] = price_range
    
    if guide:
        query += ' AND guide = %s'
        count_query += ' AND guide = %s'
        params.append(guide)
        log_params['guide'] = guide
    
    if people:
        query += ' AND people = %s'
        count_query += ' AND people = %s'
        params.append(people)
        log_params['people'] = people
    
    query += ' LIMIT %s OFFSET %s'
    
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = session['username']

    
    params.extend([PER_PAGE, (page - 1) * PER_PAGE])

    cursor.execute(query, params)
    
    app.logger.info(f'{{\'user\' : \'{user_id}\', \'params\' : {log_params}}}')

    packages = cursor.fetchall()
    packages = [{'name': p[0], 'country': p[1], 'city': p[2], 'price': p[3], 'start_date': p[4], 'end_date': p[5], 'guide': p[6], 'people': p[7], 'theme': p[8]} for p in packages]

    
    cursor.execute(count_query, params[:-2])
    total_packages = cursor.fetchone()[0]
    total_pages = (total_packages + PER_PAGE - 1) // PER_PAGE
    if total_packages > 5:
        total_packages = 5

    page_numbers = list(range(1, total_pages + 1))
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    query_string = request.query_string.decode().replace(f'page={page}', '').replace('&&', '&').strip('&')
    
    return render_template('travel_packages.html', packages=packages, page=page, page_numbers=page_numbers, prev_page=prev_page, next_page=next_page, query_string=query_string)


@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_id = session['username']
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        email = request.form['email']
        full_name = request.form['full_name']
        cursor.execute('UPDATE users SET email = %s, full_name = %s WHERE username = %s', (email, full_name, user_id))
        db.commit()

    cursor.execute('SELECT username, email, full_name FROM users WHERE username = %s', (user_id,))
    user = cursor.fetchone()
    return render_template('mypage.html', user=user)

@app.route('/execute_script', methods=['POST'])
def execute_script():
    result = subprocess.run(['python', 'script.py'], capture_output=True, text=True)
    output = result.stdout.strip()
    return jsonify({"message": output})

@app.route('/recommend', methods=['POST'])
def recommend():
    result = subprocess.run(['python', 'recommend.py'], capture_output=True, text=True)
    recommendations = result.stdout.strip().split('\n')
    return jsonify({"recommendations": recommendations})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
