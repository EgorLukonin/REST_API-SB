from flask import jsonify
from flask_restful import Resource, abort, reqparse
from sqlalchemy import exc

from data.db_session import create_session
from data.models.organizations import Organizations

from .utilits.check_void import check_void


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
            abort(404, error="Insufficient or incorrectly passed arguments (expected 5)")


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
            abort(404, error=f"No organization with id = {organization_id}")
        else:
            return jsonify({"organization": organization.to_dict()})

    def delete(self, organization_id):
        session = create_session()
        organization = session.query(Organizations).get(organization_id)
        if not organization:
            abort(404, error=f"No organization with id = {organization_id}")
        else:
            session.delete(organization)
            session.commit()
            resp = {"status_code": 200}
            return jsonify(resp)

    def put(self, organization_id):
        session = create_session()
        organization = session.query(Organizations).get(organization_id)
        if not organization:
            abort(404, error=f"No organization with id = {organization_id}")
        else:
            args = self.parser.parse_args()
            values = list(args.values())
            if len(set(values)) == 1:
                abort(404, error="Insufficient arguments (expected 5)")
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
