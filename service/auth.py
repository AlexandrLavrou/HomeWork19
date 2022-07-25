import datetime
import calendar

import jwt

from constants import JWT_SECRET, JWT_ALGORITHM
from service.user import UserService
from flask import abort


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):

        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(404)
        if not is_refresh:
            if not self.user_service.compare_password(user.password, password):
                abort(400)
        data = {"username": user.username, "role": user.role}

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        days90 = datetime.datetime.utcnow() + datetime.timedelta(days=90)
        data["exp"] = calendar.timegm(days90.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {"access_token": access_token, "refresh_token": refresh_token}

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(refresh_token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        username = data['username']
        user = self.user_service.get_by_username(username)

        if not user:
            raise Exception("bad token")
        return self.generate_tokens(username, user.password, is_refresh=True)
