import allure
import pytest


class TestBuildConfigNegative:

    @allure.feature('Builds management_negative')
    @allure.story('Build creation_negative')
    @allure.testcase('https:testcase.manager/testcase/13', name='Test case')
    @allure.title('Checking if we can create two builds holding the same ID. Negative scenario')
    @allure.description('Checks if two builds with the same ID\'s can be created')
    def test_create_two_builds_with_the_same_id(self, super_admin, build_data):
        project_data_1, build_data_1 = build_data()
        with allure.step('Sending a request to create a project for build configuration'):
            create_response = super_admin.api_object.project_api.create_project(project_data_1.model_dump())

        with allure.step('Sending a request to create the first build config'):
            create_response_1 = super_admin.api_object.build_api.create_build(build_data_1.model_dump()).text

        project_data_2, build_data_2 = build_data()
        with allure.step('Sending a request to create a project for build configuration'):
            create_response = super_admin.api_object.project_api.create_project(project_data_2.model_dump())

        with allure.step('Sending a request to create the second build config with the same ID as the first one'):
            build_data_2.id = build_data_1.id
            try:
                create_response_2 = super_admin.api_object.build_api.create_build(build_data_2.model_dump()).text
                pytest.fail("Creating two builds with the same ID succeeded unexpectedly.")
            except ValueError as e:
                if "Unexpected status code: 400" in str(e):
                    # Log a custom message if a 400 status code is encountered
                    allure.attach("Custom Log", "Builds with the same ID are not allowed!", allure.attachment_type.TEXT)
                    print("Custom Log: Builds with the same ID are not allowed!")
                    pytest.fail("Creating two builds with the same ID is not allowed.")
                else:
                    # If it's not a 400 status code, fail the test with the original error
                    raise e

