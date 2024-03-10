import allure
import time

from data.build_data import BuildResponseModel, RunBuildResponseModel
import pytest


class TestBuildConfig:

    @allure.feature('Builds management')
    @allure.story('Build creation')
    @allure.testcase('https:testcase.manager/testcase/13', name='Test case')
    @allure.title('Checking if a build was created')
    @allure.description('Checks if a build was created')
    def test_create_build(self, super_admin, build_data):
        project_data_1, build_data_1 = build_data()
        with allure.step('Sending a request to create a project for build configuration'):
            create_response = super_admin.api_object.project_api.create_project(project_data_1.model_dump())

        with allure.step('Sending a request to create a build config'):
            create_response = super_admin.api_object.build_api.create_build(build_data_1.model_dump()).text
            build_response = BuildResponseModel.model_validate_json(create_response)
        with pytest.assume:
            assert build_response.id == build_data_1.id, \
                f"expected build id = {build_data_1.id}, but '{build_response.id}' given"
        with pytest.assume:
            assert build_response.projectId == build_data_1.project["id"]

        with allure.step('Sending a request to get info about the created build'):
            get_response = super_admin.api_object.build_api.get_build_by_id(build_data_1.id).text
            created_build = BuildResponseModel.model_validate_json(get_response)
        with pytest.assume:
            assert created_build.id == build_data_1.id, \
                f"expected build id = {build_data_1.id}, but '{created_build.id}' given"
