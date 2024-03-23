from flask import jsonify
from flask_restful import Resource, reqparse
from sqlalchemy import exc

from data.db_session import create_session
from data.models.organizations import Organizations

from .check_condition import check_void, check_len_str, check_len_number


class OrganizationsListResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        interface = ["abbreviated_name", "full_name", "address", "OKATO", "OGRN"]
        for key in interface:
            self.parser.add_argument(f"{key}")

    def get(self):
        session = create_session()
        organizations = session.query(Organizations).all()
        return jsonify({"organizations": list(map(Organizations.to_dict, organizations))})

    def post(self):
        args = self.parser.parse_args()
        session = create_session()
        try:
            check_args = [check_len_str("abbreviated_name", args["abbreviated_name"]),
                          check_len_str("full_name", args["full_name"]),
                          check_len_str("address", args["address"]),
                          check_len_number("OKATO", args["OKATO"], 11),
                          check_len_number("OGRN", args["OGRN"], 13)
                          ]
            for value in check_args:
                if isinstance(value, bool) is False:
                    return jsonify({"error": value})

            organization = Organizations(
                abbreviated_name=args["abbreviated_name"],
                full_name=args["full_name"],
                address=args["address"],
                OKATO=args["OKATO"],
                OGRN=args["OGRN"],
            )
            session.add(organization)
            session.commit()
            resp = {"status_code": 200}
            return jsonify(resp)
        except exc.IntegrityError:
            return jsonify({"error": "Insufficient or incorrectly passed arguments (expected 5)"})


class OrganizationsResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        interface = ["abbreviated_name", "full_name", "address", "OKATO", "OGRN"]
        for key in interface:
            self.parser.add_argument(f"{key}")

    def get(self, organization_id):
        session = create_session()
        organization = session.query(Organizations).get(organization_id)
        if not organization:
            return jsonify({"error": f"No organization with id = {organization_id}"})
        else:
            return jsonify({"organization": organization.to_dict()})

    def delete(self, organization_id):
        session = create_session()
        organization = session.query(Organizations).get(organization_id)
        if not organization:
            return jsonify({"error": f"No organization with id = {organization_id}"})
        else:
            session.delete(organization)
            session.commit()
            resp = {"status_code": 200}
            return jsonify(resp)

    def put(self, organization_id):
        session = create_session()
        organization = session.query(Organizations).get(organization_id)
        if not organization:
            return jsonify({"error": f"No organization with id = {organization_id}"})
        else:
            args = self.parser.parse_args()
            values = list(args.values())
            if len(set(values)) == 1:
                return jsonify({"error": "Insufficient arguments (expected 5)"})
            else:
                args = check_void(args)
                organization.abbreviated_name = args["abbreviated_name"] if "abbreviated_name" in args else organization.abbreviated_name
                organization.full_name = args["full_name"] if "full_name" in args else organization.full_name
                organization.address = args["address"] if "address" in args else organization.address
                organization.OKATO = args["OKATO"] if "OKATO" in args else organization.OKATO
                organization.OGRN = args["OGRN"] if "OGRN" in args else organization.OGRN
                session.commit()
                resp = {"status_code": 200}
                return jsonify(resp)
