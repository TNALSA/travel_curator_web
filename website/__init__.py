from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'postgres'

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:lightening123$@database-tour.cluster-ro-crln8mpfedqu.ap-northeast-2.rds.amazonaws.com:5432/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    # get Blueprint object
    from .views import views
    from .mypage_views import mypage_views
    from .auth import auth

    # register on flask app
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(mypage_views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    
    # Get models
    from .models import User  # from .models import *
    # create_database(app)

   # flask-login 적용
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)  # primary_key
    
    
    return app

# # 데이터 베이스 생성 함수
# def create_database(app):
#     # db파일이 확인안될 때만 생성
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('>>> Create DB')