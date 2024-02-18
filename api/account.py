from flask import jsonify
from flask_restful import Resource, abort, reqparse
from sqlalchemy import exc

from data.db_session import create_session
from data.models.accounts import Accounts


class AccountsListResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        interface = ["full_name", "account_number", "contract_number", "INN", "BIK", "balance"]
        for key in interface:
            self.parser.add_argument(f"{key}")

    def get(self):
        session = create_session()
        accounts = session.query(Accounts).all()
        return jsonify({"accounts": list(map(Accounts.to_dict, accounts))})

    def post(self):
        args = self.parser.parse_args()
        session = create_session()
        try:
            account = Accounts(
                full_name=args["full_name"],
                account_number=args["account_number"],
                contract_number=args["contract_number"],
                INN=args["INN"],
                BIK=args["BIK"],
                balance=args["balance"]
            )
            session.add(account)
            session.commit()
            resp = {"status_code": 200}
            return jsonify(resp)
        except exc.IntegrityError:
            abort(404, error="Insufficient or incorrectly passed arguments (expected 5)")


class AccountsResource(Resource):

    def get(self, account_id):
        session = create_session()
        account = session.query(Accounts).get(account_id)
        if not account:
            abort(404, error=f"No account with id = {account_id}")
        else:
            return jsonify({"account": account.to_dict()})

    def delete(self, account_id):
        session = create_session()
        account = session.query(Accounts).get(account_id)
        if not account:
            abort(404, error=f"No account with id = {account_id}")
        else:
            session.delete(account_id)
            session.commit()
            resp = {"status_code": 200}
            return jsonify(resp)
