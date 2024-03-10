from http import HTTPStatus

from custom_requester.custom_requester import CustomRequester


class BuildAPI(CustomRequester):

    def create_build(self, build_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST",
                                 "/app/rest/buildTypes",
                                 data=build_data,
                                 expected_status=expected_status)

    def get_build_by_id(self, build_id):
        return self.send_request("GET", f"/app/rest/buildTypes/id:{build_id}")

    def run_build(self, run_build_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST",
                                 "/app/rest/buildQueue",
                                 data=run_build_data,
                                 expected_status=expected_status)

    def check_if_queue_is_empty(self):
        return self.send_request("GET",
                                 "/app/rest/buildQueue")
