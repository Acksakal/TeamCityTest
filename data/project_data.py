from utils.data_generator import DataGenerator
from pydantic import BaseModel


class ProjectDataModel(BaseModel):
    parentProject: dict
    name: str
    id: str
    copyAllAssociatedSettings: bool


class ProjectData:

    @staticmethod
    def create_project_data() -> ProjectDataModel:
        return ProjectDataModel(parentProject={"locator": "_Root"},
                                name=DataGenerator.fake_name(),
                                id=DataGenerator.fake_project_id(),
                                copyAllAssociatedSettings=True)


class ParentProjectModel(BaseModel):
    id: str
    name: str
    description: str
    href: str
    webUrl: str


class ProjectResponseModel(BaseModel):
    id: str
    name: str
    parentProjectId: str
    parentProject: ParentProjectModel

    class ConfigDict:
        extra = "allow"
