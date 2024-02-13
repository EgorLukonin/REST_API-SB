import sqlalchemy
from ..db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Organizations(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'organizations'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    abbreviated_name = sqlalchemy.Column(sqlalchemy.String(20), nullable=True)
    full_name = sqlalchemy.Column(sqlalchemy.Text(40), nullable=True)
    address = sqlalchemy.Column(sqlalchemy.Text(40), nullable=True)
    OKATO = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    OGRN = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

