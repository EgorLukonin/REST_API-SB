from flask import jsonify
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from data.db_session import create_session
from data.models.accounts import Accounts

from utilits.check_condition import check_void, check_len_str, check_len_number


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
            check_args = [check_len_str("full_name", args["full_name"], 3),
                          check_len_number("account_number", args["account_number"], 20),
                          check_len_number("contract_number", args["contract_number"], 10),
                          check_len_number("INN", args["INN"], 10),
                          check_len_number("BIK", args["BIK"], 9)
                          ]
            for value in check_args:
                if isinstance(value, bool) is False:
                    return jsonify({"error": value})
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
           return jsonify({"error": "Insufficient or incorrectly passed arguments (expected 6)"})


class AccountsResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        interface = ["full_name", "account_number", "contract_number", "INN", "BIK", "balance"]
        for key in interface:
            self.parser.add_argument(f"{key}")

    def get(self, account_id):
        session = create_session()
        account = session.query(Accounts).get(account_id)
        if not account:
            return jsonify({"error": f"No account with id = {account_id}"})
        else:
            return jsonify({"account": account.to_dict()})

    def delete(self, account_id):
        session = create_session()
        account = session.query(Accounts).get(account_id)
        if not account:
            return jsonify({"error": f"No account with id = {account_id}"})
        else:
            session.delete(account_id)
            session.commit()
            resp = {"status_code": 200}
            return jsonify(resp)

    def put(self, account_id):
        session = create_session()
        account = session.query(Accounts).get(account_id)
        if not account:
            return jsonify({"error": f"No account with id = {account_id}"})
        else:
            args = self.parser.parse_args()
            values = list(args.values())
            if len(set(values)) == 1:
                return jsonify({"error": "Insufficient arguments (expected 6)"})
            else:
                args = check_void(args)
                account.full_name = args["full_name"] if "full_name" in args else account.full_name
                account.account_number = args["account_number"] if "account_number" in args else account.account_number
                account.contract_number = args["contract_number"] if "contract_number" in args else account.contract_number
                account.INN = args["INN"] if "INN" in args else account.INN
                account.BIK = args["BIK"] if "BIK" in args else account.BIK
                account.balance = args["balance"] if "balance" in args else account.balance
                session.commit()
                resp = {"status_code": 200}
                return jsonify(resp)