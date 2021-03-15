
from .utils import *
from . import models

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


#addGroup = "https://omegaup.com/api/user/addGroup/"
#associateIdentity = "https://omegaup.com/api/user/associateIdentity/"
#changePassword = "https://omegaup.com/api/user/changePassword/"
#coderOfTheMonth = "https://omegaup.com/api/user/coderOfTheMonth/"
#coderOfTheMonthList = "https://omegaup.com/api/user/coderOfTheMonthList/"
#contestStats = "https://omegaup.com/api/user/contestStats/"
#
## Interesting stuff
#create = "https://omegaup.com/api/user/create/"
#generateOmiUsers = "https://omegaup.com/api/user/generateOmiUsers/"
#
#listAssociatedIdentities = "https://omegaup.com/api/user/listAssociatedIdentities/"
#listUnsolvedProblems = "https://omegaup.com/api/user/listUnsolvedProblems/"
#login = "https://omegaup.com/api/user/login/"

#login = "https://omegaup.com"
#login = "https://omegaup.com"
#login = "https://omegaup.com"
#login = "https://omegaup.com"
#login = "https://omegaup.com"
#login = "https://omegaup.com"
#login = "https://omegaup.com"
#login = "https://omegaup.com"
#login = "https://omegaup.com"
#login = "https://omegaup.com"
#login = "https://omegaup.com"
#login = "https://omegaup.com"
#login = "https://omegaup.com"
#login = "https://omegaup.com"
#login = "https://omegaup.com"
