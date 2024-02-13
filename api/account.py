from flask import jsonify
from flask_restful import Resource, abort

from data.db_session import create_session
from data.models.accounts import Accounts


class AccountsListResource(Resource):

    def get(self):
        session = create_session()
        accounts = session.query(Accounts).all()
        return jsonify({"accounts": list(map(Accounts.to_dict, accounts))})


class AccountsResource(Resource):

    def get(self, account_id):
        session = create_session()
        account = session.query(Accounts).get(account_id)
        if not account:
            abort(404, error=f"No account with id = {account_id}")
        else:
            return jsonify({"account": account.to_dict()})
