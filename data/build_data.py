from utils.data_generator import DataGenerator
from pydantic import BaseModel


class BuildDataModel(BaseModel):
    id: str
    name: str
    project: dict
    steps: dict


class RunBuildDataModel(BaseModel):
    buildType: dict


class BuildData:

    @staticmethod
    def create_build_data(project_id) -> BuildDataModel:
        return BuildDataModel(id=DataGenerator.fake_build_id(),
                              name=DataGenerator.fake_name(),
                              project={"id": project_id},
                              steps={
                                  "step": [
                                      {
                                          "name": "myCommandLineStep",
                                          "type": "simpleRunner",
                                          "properties": {
                                              "property": [
                                                  {
                                                      "name": "script.content",
                                                      "value": "echo 'Hello World!'"
                                                  },
                                                  {
                                                      "name": "teamcity.step.mode",
                                                      "value": "default"
                                                  },
                                                  {
                                                      "name": "use.custom.script",
                                                      "value": "true"
                                                  }
                                              ]
                                          }
                                      }
                                  ]
                              })

    @staticmethod
    def create_run_build_data(build_id) -> RunBuildDataModel:
        return RunBuildDataModel(buildType={"id": build_id})


class BuildResponseModel(BaseModel):
    id: str
    name: str
    projectId: str
    project: dict
    steps: dict

    class ConfigDict:
        extra = "allow"


class RunBuildResponseModel(BaseModel):
    buildTypeId: str
    buildType: dict
