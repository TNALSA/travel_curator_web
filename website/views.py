from datetime import datetime

import requests
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from flask_login import login_required, current_user
import psycopg2

from psycopg2.extras import RealDictCursor
from .auth import get_db
from .models import TravelPackage
from . import db

views = Blueprint('views', __name__)



@views.route('/')
def home():
    return render_template('index.html')

# @views.route('/issue-coupon', methods=['Get', 'POST'])
# def issue_coupon():
#     if 'username' not in session:
#         return redirect(url_for('auth.login'))
#     username = session['username']
#
#     conn = get_db_connection()
#     cursor = conn.cursor(cursor_factory=RealDictCursor)
#
#     try:
#         cursor.execute('SELECT COUNT(*) FROM user_coupons')
#         coupon_count = cursor.fetchone()['count']
#
#         if coupon_count < 50:
#             cursor.execute('INSERT INTO user_coupons (username, coupon_code, description) VALUES (%s, %s, %s)',
#                            (username, 'COUPON' + str(coupon_count + 1).zfill(4), 'Discount Coupon'))
#             conn.commit()
#             result = {"success": True, "couponCode": 'COUPON' + str(coupon_count + 1).zfill(4)}
#         else:
#             result = {"success": False, "message": "No more coupons available."}
#     except Exception as e:
#         conn.rollback()
#         result = {"error": str(e)}
#     finally:
#         cursor.close()
#         conn.close()
#
#     result = jsonify(result)
#     # result = 'test'
#     return render_template('issue_coupon.html',message=result )
#
# -----

@views.route('/issue-coupon', methods=['GET','POST'])
def issue_coupon():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    username = session['username']

    message = request.args.get('message')

    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        # 쿠폰 유효 기간에 해당하는 쿠폰 목록을 조회
        cursor.execute('SELECT * FROM coupons WHERE date_issue_start <= (SELECT now()) AND (SELECT now()) <= date_issue_end')
        coupons = cursor.fetchall()

        coupon_list = []
        for c in coupons:
            date_issue_start = datetime.strptime(str(c['date_issue_start']), '%Y-%m-%d %H:%M:%S')
            date_issue_end = datetime.strptime(str(c['date_issue_end']), '%Y-%m-%d %H:%M:%S')
            formatted_date_issue_start = date_issue_start.strftime('%Y년 %m월 %d일')
            formatted_date_issue_end = date_issue_end.strftime('%Y년 %m월 %d일')

            coupon_list.append({
                'id': c['id'],
                'title': c['title'],
                'coupon_type': c['coupon_type'],
                'total_quantity': c['total_quantity'],
                'issued_quantity': c['issued_quantity'],
                'date_issue_start': formatted_date_issue_start,
                'date_issue_end': formatted_date_issue_end
            })

    except Exception as e:
        conn.rollback()
        result = {"error": str(e)}

    finally:
        cursor.close()
        conn.close()

    if message :
        return render_template('issue_coupon.html', coupon_list=coupon_list, message = message)
    else:
        return render_template('issue_coupon.html', coupon_list=coupon_list)


@views.route('/issues', methods=['GET','POST'])
def issues():
    print("Request received at /issue") # 디버깅 출력
    if 'username' not in session:
        print("Username not in session, redirecting to login")
        return redirect(url_for('login'))

    if request.method == 'POST':
        print("POST request received")
        user_id = session['username']
        coupon_id = request.form.get('coupon_id')
        print(f"Form data received - userId: {user_id}, couponId: {coupon_id}")

        print("userId : {0} , couponId : {1}".format(user_id, coupon_id))
        data = {
            "userId": str(user_id),
            "couponId": int(coupon_id)
        }

        response = requests.post('http://172.18.0.3:7070/v2/issue-async', json=data)

        isSuccess = response.json().get('isSuccess')
        comment = response.json().get('comment')

        print("isSuccess: "+ str(isSuccess))
        print("comment: "+str(comment))

        return redirect(url_for('views.issue_coupon', message = str(comment)))


@views.route('/travel_packages', methods=['GET'])
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

    # recommendations = get_recommendations()
    recommendations = [['PACKAGE1', 'Canada', '2024-06-10'],['PACKAGE2', 'Germany', '2024-07-10']]
    return render_template('travel_packages.html', packages=packages, page=page, page_numbers=page_numbers, prev_page=prev_page, next_page=next_page, query_string=query_string, recommendations=recommendations)
