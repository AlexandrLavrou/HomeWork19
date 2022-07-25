from flask import request, abort
from flask_restx import Namespace, Resource

from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route("/")
class AuthView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get("username", None)
        password = req_json.get("password", None)
        if None is [username, password]:
            return abort(400)

        tokens = auth_service.generate_tokens(username, password)
        if tokens:
            return tokens, 201

        return "horror", 400

    def put(self):
        data = request.json
        ref_token = data.get("refresh_token")
        if ref_token is None:
            return abort(400)
        tokens = auth_service.approve_refresh_token(ref_token)
        if tokens:
            return tokens, 201
        else:
            return "horror", 400
