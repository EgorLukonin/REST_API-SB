from flask import jsonify
from flask_restful import Resource, abort

from data.db_session import create_session
from data.models.organizations import Organizations


class OrganizationsListResource(Resource):

    def get(self):
        session = create_session()
        organizations = session.query(Organizations).all()
        return jsonify({"organizations": list(map(Organizations.to_dict, organizations))})


class OrganizationsResource(Resource):

    def get(self, organization_id):
        session = create_session()
        organization = session.query(Organizations).get(organization_id)
        if not organization:
            abort(404, error=f"No organization with id = {organization_id}")
        else:
            return jsonify({"organization": organization.to_dict()})
