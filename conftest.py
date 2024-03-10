import pytest
import requests

from api.api_manager import APIManager
from data.build_data import BuildData
from data.project_data import ProjectData
from data.user_data import UserData
from entities.user import User, Role
from resources.user_creds import SuperAdminCreds


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = APIManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()
    super_admin = User(SuperAdminCreds.USERNAME,
                       SuperAdminCreds.PASSWORD,
                       new_session,
                       ["SUPER_ADMIN", "g"])
    super_admin.api_object.auth_api.auth_and_get_csrf(super_admin.creds)
    return super_admin


@pytest.fixture
def user_create(user_session, super_admin):
    created_user_pool = []

    def _user_create(role):
        user_data = UserData.create_user_data(role, scope="g")
        super_admin.api_object.user_api.create_user(user_data)
        new_session = user_session()
        created_user_pool.append(user_data["username"])
        return User(user_data["username"],
                    user_data["password"],
                    new_session,
                    [Role(role)],
                    user_data["email"])

    yield _user_create

    for username in created_user_pool:
        super_admin.api_object.user_api.delete_user(username)


@pytest.fixture
def project_data(super_admin):
    project_id_pool = []

    def _project_data():
        project = ProjectData.create_project_data()
        project_id_pool.append(project.id)
        return project

    yield _project_data

    for project_id in project_id_pool:
        super_admin.api_object.project_api.clean_up_project(project_id)


@pytest.fixture
def build_data(super_admin):
    project_id_pool = []

    def _build_data():
        project = ProjectData.create_project_data()
        project_id_pool.append(project.id)
        build = BuildData.create_build_data(project.id)
        return project, build

    yield _build_data

    for project_id in project_id_pool:
        super_admin.api_object.project_api.clean_up_project(project_id)


@pytest.fixture
def run_build(super_admin):
    project_id_pool = []

    def _run_build():
        project = ProjectData.create_project_data()
        project_id_pool.append(project.id)
        build = BuildData.create_build_data(project.id)
        run_build = BuildData.create_run_build_data(build.id)
        return project, build, run_build

    yield _run_build

    for project_id in project_id_pool:
        super_admin.api_object.project_api.clean_up_project(project_id)
