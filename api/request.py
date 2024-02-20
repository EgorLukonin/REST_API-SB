from flask import jsonify
from flask_restful import Resource, abort, reqparse
from sqlalchemy import exc

from data.db_session import create_session
from data.models.requests import Requests

from .utilits.check_void import check_void


class RequestsListResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        interface = ["type", "status", "account"]
        for key in interface:
            self.parser.add_argument(f"{key}")

    def get(self):
        session = create_session()
        requests = session.query(Requests).all()
        return jsonify({"requests": list(map(Requests.to_dict, requests))})

    def post(self):
        args = self.parser.parse_args()
        session = create_session()
        try:
            request = Requests(
                type=args["type"],
                status=args["status"],
                account=args["account"]
            )
            session.add(request)
            session.commit()
            resp = {"status_code": 200}
            return jsonify(resp)
        except exc.IntegrityError:
            abort(404, error="Insufficient or incorrectly passed arguments (expected 3)")


class RequestsResource(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        interface = ["type", "status", "account"]
        for key in interface:
            self.parser.add_argument(f"{key}")

    def get(self, request_id):
        session = create_session()
        request = session.query(Requests).get(request_id)
        if not request:
            abort(404, error=f"No request with id = {request_id}")
        else:
            return jsonify({"request": request.to_dict()})

    def delete(self, request_id):
        session = create_session()
        request = session.query(Requests).get(request_id)
        if not request:
            abort(404, error=f"No request with id = {request_id}")
        else:
            session.delete(request)
            session.commit()
            resp = {"status_code": 200}
            return jsonify(resp)

    def put(self, request_id):
        session = create_session()
        request = session.query(Requests).get(request_id)
        if not request:
            abort(404, error=f"No request with id = {request_id}")
        else:
            args = self.parser.parse_args()
            values = list(args.values())
            if len(set(values)) == 1:
                abort(404, error="Insufficient arguments (expected 3)")
            else:
                args = check_void(args)
                request.type = args["type"] if "type" in args else request.type
                request.status = args["status"] if "status" in args else request.status
                request.account = args["account"] if "account" in args else request.account
                session.commit()
                resp = {"status_code": 200}
                return jsonify(resp)

