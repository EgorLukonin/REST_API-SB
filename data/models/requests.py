import sqlalchemy
from ..db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Requests(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'requests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    account = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

