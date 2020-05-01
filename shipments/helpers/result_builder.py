from rest_framework import status
from rest_framework.response import Response


class ResultBuilder:
    def __init__(self):
        self.results = {}
        self.status_code = 1
        self.status_message = ""
        self.status = status.HTTP_200_OK

    def fail(self):
        self.status_code = -1
        return self

    def message(self, status_message):
        self.status_message = status_message
        return self

    def success(self):
        self.status_code = 1
        return self

    def ok_200(self):
        self.status = status.HTTP_200_OK
        return self

    def bad_request_400(self):
        self.status = status.HTTP_400_BAD_REQUEST
        return self

    def user_unauthorized_401(self):
        self.status = status.HTTP_401_UNAUTHORIZED
        self.status_message = "User Unauthorized"
        return self

    def result_object(self, result):
        self.results = result
        return self

    def get_response(self):
        content = self.get_json()
        return Response(content, status=self.status)

    def get_json(self):
        return {
            'status-code': self.status_code,
            'status-message': self.status_message,
            'data': self.results
        }
