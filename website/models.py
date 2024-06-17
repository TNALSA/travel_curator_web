# models.py
# coding: utf-8
from . import db  # from website import db

# define User Model
class User(db.Model):
    __tablename__ = 'users'
    # username password email full_name
    username = db.Column(db.String(200), primary_key=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(200))
    full_name = db.Column(db.String(200))
    pass


class TravelPackage(db.Model):
    __tablename__ = 'travel_packages'
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

class UserCoupon(db.Model):
    __tablename__ = 'user_coupons'
    #  id | user_id | coupon_code | expiration_date
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    coupon_code = db.Column(db.String, nullable=False)
    expiration_date = db.Column(db.String, nullable=False)

class Coupons(db.Model):
    __tablename__ = 'coupons'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True )
    title = db.Column(db.String, nullable=False)
    coupon_type = db.Column(db.String, nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)
    issued_quantity = db.Column(db.Integer, nullable=False)
    discount_amount = db.Column(db.Integer, nullable=False)
    min_available_amount = db.Column(db.Integer, nullable=False)
    date_issue_start = db.Column(db.DateTime, nullable=False)
    date_issue_end = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    date_updated = db.Column(db.DateTime, nullable=False)

class CouponIssues(db.Model):
    __tablename__ = 'coupon_issues'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    coupon_id = db.Column(db.BigInteger, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    date_issued = db.Column(db.DateTime, nullable=False)
    date_used = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    date_updated = db.Column(db.DateTime, nullable=False)


# from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, Table, Text
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql.sqltypes import NullType
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class AuthGroup(db.Model):
#     __tablename__ = 'auth_group'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)


# class AuthGroupPermission(db.Model):
#     __tablename__ = 'auth_group_permissions'
#     __table_args__ = (
#         db.Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id'),
#     )

#     id = db.Column(db.Integer, primary_key=True)
#     group_id = db.Column(db.ForeignKey('auth_group.id'), nullable=False, index=True)
#     permission_id = db.Column(db.ForeignKey('auth_permission.id'), nullable=False, index=True)

#     group = db.relationship('AuthGroup', primaryjoin='AuthGroupPermission.group_id == AuthGroup.id', backref='auth_group_permissions')
#     permission = db.relationship('AuthPermission', primaryjoin='AuthGroupPermission.permission_id == AuthPermission.id', backref='auth_group_permissions')


# class AuthPermission(db.Model):
#     __tablename__ = 'auth_permission'
#     __table_args__ = (
#         db.Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename'),
#     )

#     id = db.Column(db.Integer, primary_key=True)
#     content_type_id = db.Column(db.ForeignKey('django_content_type.id'), nullable=False, index=True)
#     codename = db.Column(db.String(100), nullable=False)
#     name = db.Column(db.String(255), nullable=False)

#     content_type = db.relationship('DjangoContentType', primaryjoin='AuthPermission.content_type_id == DjangoContentType.id', backref='auth_permissions')


# class AuthUser(db.Model):
#     __tablename__ = 'auth_user'

#     id = db.Column(db.Integer, primary_key=True)
#     password = db.Column(db.String(128), nullable=False)
#     last_login = db.Column(db.DateTime)
#     is_superuser = db.Column(db.Boolean, nullable=False)
#     first_name = db.Column(db.String(30), nullable=False)
#     last_name = db.Column(db.String(30), nullable=False)
#     email = db.Column(db.String(254), nullable=False)
#     is_staff = db.Column(db.Boolean, nullable=False)
#     is_active = db.Column(db.Boolean, nullable=False)
#     date_joined = db.Column(db.DateTime, nullable=False)
#     username = db.Column(db.String(150), nullable=False)


# class AuthUserGroup(db.Model):
#     __tablename__ = 'auth_user_groups'
#     __table_args__ = (
#         db.Index('auth_user_groups_user_id_group_id_94350c0c_uniq', 'user_id', 'group_id'),
#     )

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.ForeignKey('auth_user.id'), nullable=False, index=True)
#     group_id = db.Column(db.ForeignKey('auth_group.id'), nullable=False, index=True)

#     group = db.relationship('AuthGroup', primaryjoin='AuthUserGroup.group_id == AuthGroup.id', backref='auth_user_groups')
#     user = db.relationship('AuthUser', primaryjoin='AuthUserGroup.user_id == AuthUser.id', backref='auth_user_groups')


# class AuthUserUserPermission(db.Model):
#     __tablename__ = 'auth_user_user_permissions'
#     __table_args__ = (
#         db.Index('auth_user_user_permissions_user_id_permission_id_14a6b632_uniq', 'user_id', 'permission_id'),
#     )

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.ForeignKey('auth_user.id'), nullable=False, index=True)
#     permission_id = db.Column(db.ForeignKey('auth_permission.id'), nullable=False, index=True)

#     permission = db.relationship('AuthPermission', primaryjoin='AuthUserUserPermission.permission_id == AuthPermission.id', backref='auth_user_user_permissions')
#     user = db.relationship('AuthUser', primaryjoin='AuthUserUserPermission.user_id == AuthUser.id', backref='auth_user_user_permissions')


# class DjangoAdminLog(db.Model):
#     __tablename__ = 'django_admin_log'

#     id = db.Column(db.Integer, primary_key=True)
#     object_id = db.Column(db.Text)
#     object_repr = db.Column(db.String(200), nullable=False)
#     action_flag = db.Column(db.Integer, nullable=False)
#     change_message = db.Column(db.Text, nullable=False)
#     content_type_id = db.Column(db.ForeignKey('django_content_type.id'), index=True)
#     user_id = db.Column(db.ForeignKey('auth_user.id'), nullable=False, index=True)
#     action_time = db.Column(db.DateTime, nullable=False)

#     content_type = db.relationship('DjangoContentType', primaryjoin='DjangoAdminLog.content_type_id == DjangoContentType.id', backref='django_admin_logs')
#     user = db.relationship('AuthUser', primaryjoin='DjangoAdminLog.user_id == AuthUser.id', backref='django_admin_logs')


# class DjangoContentType(db.Model):
#     __tablename__ = 'django_content_type'
#     __table_args__ = (
#         db.Index('django_content_type_app_label_model_76bd3d3b_uniq', 'app_label', 'model'),
#     )

#     id = db.Column(db.Integer, primary_key=True)
#     app_label = db.Column(db.String(100), nullable=False)
#     model = db.Column(db.String(100), nullable=False)


# class DjangoMigration(db.Model):
#     __tablename__ = 'django_migrations'

#     id = db.Column(db.Integer, primary_key=True)
#     app = db.Column(db.String(255), nullable=False)
#     name = db.Column(db.String(255), nullable=False)
#     applied = db.Column(db.DateTime, nullable=False)


# class DjangoSession(db.Model):
#     __tablename__ = 'django_session'

#     session_key = db.Column(db.String(40), primary_key=True)
#     session_data = db.Column(db.Text, nullable=False)
#     expire_date = db.Column(db.DateTime, nullable=False, index=True)


# t_sqlite_sequence = db.Table(
#     'sqlite_sequence',
#     db.Column('name', db.NullType),
#     db.Column('seq', db.NullType)
# )