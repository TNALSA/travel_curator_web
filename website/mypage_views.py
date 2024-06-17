from datetime import datetime

from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
import psycopg2

from .auth import get_db
from psycopg2.extras import RealDictCursor

from .models import User
from . import db

mypage_views = Blueprint('mypage_views', __name__)

@mypage_views.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    username = session['username']
    user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        user.email = request.form['email']
        user.full_name = request.form['full_name']
        db.session.commit()

    return render_template('mypage.html', user=user)

@mypage_views.route('/my_coupons')
def my_coupons():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']

    conn = get_db()

    # conn = psycopg2.connect(
    #     host='database-tour.cluster-ro-crln8mpfedqu.ap-northeast-2.rds.amazonaws.com',
    #     dbname='postgres',
    #     user='postgres',
    #     password='lightening123$',
    #     port=5432
    # )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        print("Executing query...")
        cursor.execute('SELECT * FROM coupons c INNER JOIN coupon_issues ci ON c.id = ci.coupon_id WHERE user_id = \''+username+'\'')
        my_coupon = cursor.fetchall()

        print("Query executed successfully, my_coupon: " + str(my_coupon))

        my_coupon_list = []
        for c in my_coupon:
            date_issue_end = datetime.strptime(str(c['date_issue_end']), '%Y-%m-%d %H:%M:%S')
            formatted_date_issue_end = date_issue_end.strftime('%Y년 %m월 %d일')

            my_coupon_list.append({
                'id': c['id'],
                'title': c['title'],
                'coupon_id': c['coupon_id'],
                'user_id': c['user_id'],
                # 'date_issue_start':c['date_issue_start'],
                'date_issue_end': formatted_date_issue_end,
                'date_issued': c['date_issued'],
                'date_used': c['date_used'],
                'date_created': c['date_created'],
                'date_updated': c['date_updated']
            })

    except Exception as e:
        conn.rollback()
        print("Error occurred:", str(e))
        result = {"error": str(e)}

    finally:
        cursor.close()
        conn.close()

    return render_template('my_coupons.html', my_coupon_list = my_coupon_list)





