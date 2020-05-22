from typing import List, Dict, Tuple
import requests


class Base:
    def __init__(self, url: str, required_data: List[Dict]):
        self.url, self.required_data = url, required_data
        self.response_code, self.response_content = self.get_page(self.url)

    @staticmethod
    def get_page(url: str) -> Tuple:
        """
        Perform an http request, returns content of the response
        :param url: url to get content for
        :type url: str
        :return: Content of the response from the url
        :rtype: bytes
        """
        # response = requests.get("http://splash:8050/render.json?url={}&html=1")
        response = requests.get(url=url)
        return response.status_code, response.content
