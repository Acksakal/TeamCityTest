import allure
import time

from data.build_data import BuildResponseModel, RunBuildResponseModel
from data.project_data import ProjectResponseModel
import pytest


class TestProjectCreate:

    @allure.feature('Projects management')
    @allure.story('Project creation')
    @allure.testcase('https:testcase.manager/testcase/13', name='Test case')
    @allure.title('Checking if a project was created')
    @allure.description('Checks if a project was created and added to the common project list')
    def test_create_project_with_role(self, super_admin, project_data):
        project_data_1, build_data_1, run_build_data_1 = project_data()
        # CREATE A PROJECT
        with allure.step('Sending a request to create a project'):
            create_response = super_admin.api_object.project_api.create_project(project_data_1.model_dump()).text
            project_response = ProjectResponseModel.model_validate_json(create_response)
        with pytest.assume:
            assert project_response.id == project_data_1.id, \
                f"expected project id = {project_data_1.id}, but '{project_response.id}' given"
        with pytest.assume:
            assert project_response.parentProjectId == project_data_1.parentProject["locator"]
        with allure.step('Sending a request to get info about the created project'):
            get_response = super_admin.api_object.project_api.get_project_by_locator(project_data_1.id).text
            created_project = ProjectResponseModel.model_validate_json(get_response)
        with pytest.assume:
            assert created_project.id == project_data_1.id, \
                f"expected project id = {project_data_1.id}, but '{created_project.id}' given"

        # CREATE A BUILD WITHIN THE CREATED PROJECT
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

        # RUNNING THE CREATED BUILD AND FINAL CLEAN-UP
        with allure.step('Running the created build'):
            create_response = super_admin.api_object.build_api.run_build(run_build_data_1.model_dump()).text
            run_build_response = RunBuildResponseModel.model_validate_json(create_response)
        with pytest.assume:
            assert run_build_response.buildTypeId == run_build_data_1.buildType['id'], \
                (f"expected run_build type id = {run_build_data_1.buildType['id']}, "
                 f"but {run_build_response.buildTypeId} given")
        with pytest.assume:
            assert run_build_response.buildTypeId == run_build_data_1.buildType["id"]
        with allure.step('Checking if the build queue is empty'):
            # Without the delay the "count" key == 1 cuz there is a discrepancy between API and UI representations
            time.sleep(1)
            get_response = super_admin.api_object.build_api.check_if_queue_is_empty().json()
        with pytest.assume:
            assert get_response["count"] == 0, "The build failed to run and still queued"
