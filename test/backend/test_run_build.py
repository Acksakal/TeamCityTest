import allure
import time

from data.build_data import BuildResponseModel, RunBuildResponseModel
import pytest


class TestBuildConfig:

    @allure.feature('Builds management')
    @allure.story('Creating and running a build')
    @allure.testcase('https:testcase.manager/testcase/13', name='Test case')
    @allure.title('Checking if we can create and run the build successfully')
    def test_run_build(self, super_admin, run_build):
        project_data_1, build_data_1, run_build_data_1 = run_build()
        with allure.step('Sending a request to create a project'):
            create_response = super_admin.api_object.project_api.create_project(project_data_1.model_dump())

        with allure.step('Sending a request to create a build config'):
            create_response = super_admin.api_object.build_api.create_build(build_data_1.model_dump())

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
