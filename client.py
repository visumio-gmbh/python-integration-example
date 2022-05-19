from urllib.parse import urljoin

import requests


class VisumIOClientError(Exception):
    def __init__(self, error_code: int, message: any = None):
        self.error_code: int = error_code
        self.message = message
        super().__init__((error_code, message))


class Client:
    API_HOST = "https://demo.visum.io/api/v2/"
    API_TOKEN = "9db1b1560149b819e472f87e0465191e69854e77c64122e167b5676fe1fce2bc"

    def _request(self, url: str, method: str = "GET", query: dict = None, data: dict = None, headers=None):
        headers = {
            "Accept": "application/json",
            "Authorization": self.API_TOKEN,
            "Content-Type": "application/json",
        }
        url = urljoin(self.API_HOST, url)
        response = requests.request(method, url, params=query, json=data, headers=headers)
        if 200 <= response.status_code < 300:
            return response
        raise VisumIOClientError(error_code=response.status_code, message=response.json())


class VisumAPI(Client):
    def get_me(self):
        response = self._request("account/")
        return response.json()

    def create_empty_questionnaire(self, document_type: str):
        response = self._request("questionnaires/", "POST", data=dict(
            document_type=document_type,
            answers=None,
        ))
        return response.json()

    def create_questionnaire(self, document_type: str, answers: dict):
        response = self._request("questionnaires/", "POST", data=dict(
            document_type=document_type,
            answers=answers,
        ))
        return response.json()

    def get_list(self):
        response = self._request("questionnaires/")
        return response.json()

    def get_by_id(self, questionnaire_id: int):
        response = self._request(f"questionnaires/{questionnaire_id}")
        return response.json()

    def generate_document(self, questionnaire_id: int):
        self._request(f"questionnaires/{questionnaire_id}/document/", method="PATCH")
        return True
