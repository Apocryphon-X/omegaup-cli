
from . import models
from .utils import *


class User:
    endpoint = ENTRYPOINT + "/api/user"
    def  __init__(self, target_session):
        self.session = target_session

    # Log into account.
    def login(self, username_or_email, password):
        login_data = get_dict("api-user-login")

        login_data["password"] = password
        login_data["usernameOrEmail"] = username_or_email

        return self.session.post(url = self.endpoint + "/login",
             params = login_data)

