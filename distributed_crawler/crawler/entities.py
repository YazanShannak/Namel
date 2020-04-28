class Domain:
    def __init__(self, domain_info):
        self.domain_info = domain_info

    @property
    def url(self):
        return self.domain_info.get("url")

    @property
    def data(self):
        return self.domain_info.get("data")


class Url:
    def __init__(self, url: str, data, response=None):
        self._url = url
        self._data = data
        self._response = response

    @property
    def object(self):
        main_dict = dict(url=self._url, data=self.data)
        if self.response:
            main_dict["response"] = self.response
            return main_dict
        else:
            return main_dict

    @property
    def data(self):
        return self._data

    @property
    def url(self):
        return self._url

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, code):
        self._response = code
