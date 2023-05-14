import logging
import curlify
import allure

from allure import step
from allure_commons.types import AttachmentType
from requests import Session


class BaseSession(Session):
    def __init__(self, **kwargs):
        self.base_url = kwargs.pop('base_url')
        super().__init__()

    def request(self, method, url, **kwargs):
        with step(f'Вызов метода:{method} end-point: {url}'):
            response = super().request(method=method, url=f'{self.base_url}{url}', **kwargs)
            content_type = response.headers.get("content-type", None)

            logging.info(f"/n Status code: {response.status_code}")
            logging.info(curlify.to_curl(response.request))
            curl_log = f'STATUS CODE: {response.status_code} {curlify.to_curl(response.request)}'

            if not content_type:
                logging.warning(f"\n Was not received the content-type, check the response: '{response.text}'")
            elif "text" in content_type:
                logging.info(f"\n Response is text: {response.text}")
            elif "json" in content_type:
                logging.info(f"\n Response is json : {response.text}")

        allure.attach(curl_log, 'curl_logs', AttachmentType.TEXT, '.log')
        allure.attach(response.text, 'response_log', AttachmentType.TEXT, '.log')

        return response
