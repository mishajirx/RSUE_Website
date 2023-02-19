import sqlalchemy
from data.db_session import SqlAlchemyBase


class Subject(SqlAlchemyBase):
    __tablename__ = 'subjects'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    courier_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('couriers.id'))
    sqlalchemy.orm.relation('Courier')
