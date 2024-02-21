from os import environ

from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from data import db_session
from api.request import RequestsListResource, RequestsResource
from api.organization import OrganizationsListResource, OrganizationsResource
from api.account import AccountsListResource, AccountsResource


load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
api = Api(app)


db_session.global_init("db/database.db")


if __name__ == '__main__':
    api.add_resource(RequestsListResource, "/api/requests/")
    api.add_resource(RequestsResource, "/api/requests/<int:request_id>")
    api.add_resource(OrganizationsListResource, "/api/organizations/")
    api.add_resource(OrganizationsResource, "/api/organizations/<int:organization_id>")
    api.add_resource(AccountsListResource, "/api/accounts/")
    api.add_resource(AccountsResource, "/api/accounts/<int:account_id>")
    app.run(debug=False, port=3000, host="127.0.0.1")
