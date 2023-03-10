import datetime

import sqlalchemy
from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_type = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    grade = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    subject = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # subject_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('subjects.id'), nullable=True)
    # sqlalchemy.orm.relation('Subject')
    c_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('couriers.id'), nullable=True)
    sqlalchemy.orm.relation('Courier')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
