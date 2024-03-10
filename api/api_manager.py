from api.auth_api import AuthAPI
from api.build_api import BuildAPI
from api.project_api import ProjectAPI
from api.user_api import UserAPI


class APIManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.project_api = ProjectAPI(session)
        self.build_api = BuildAPI(session)
        self.user_api = UserAPI(session)

    def close_session(self):
        self.session.close()