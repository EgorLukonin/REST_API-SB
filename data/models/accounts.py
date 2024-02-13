import sqlalchemy
from ..db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Accounts(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'accounts'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    full_name = sqlalchemy.Column(sqlalchemy.Text(60), nullable=True)
    account_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    contract_number = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    INN = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    BIK = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    balance = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    company = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

