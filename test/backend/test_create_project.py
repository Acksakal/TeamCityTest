import allure
import pytest

from data.project_data import ProjectResponseModel


class TestProjectCreate:

    @allure.feature('Projects management')
    @allure.story('Project creation')
    @allure.testcase('https:testcase.manager/testcase/13', name='Test case')
    @allure.title('Checking if a project was created')
    @allure.description('Checks if a project was created and added to the common project list')
    def test_create_project(self, super_admin, project_data):
        project_data_1 = project_data()
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
