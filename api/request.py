from flask import jsonify
from flask_restful import Resource, abort

from data.db_session import create_session
from data.models.requests import Requests


class RequestsListResource(Resource):

    def get(self):
        session = create_session()
        requests = session.query(Requests).all()
        return jsonify({"requests": list(map(Requests.to_dict, requests))})


class RequestsResource(Resource):

    def get(self, request_id):
        session = create_session()
        request = session.query(Requests).get(request_id)
        if not request:
            abort(404, error=f"No request with id = {request_id}")
        else:
            return jsonify({"request": request.to_dict()})
