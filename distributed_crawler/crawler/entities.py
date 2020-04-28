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
    def __init__(self, url: str, data):
        self.url = url
        self.data = data

    @property
    def object(self):
        return dict(url=self.url, data=self.data)
