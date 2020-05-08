from typing import List, Dict
from .base import Base

class Hybrid(Base):
    def __init__(self, url:str, required_data: List[Dict]):
        super(Hybrid, self).__init__(url=url, required_data=required_data)
        self.response_code, self.response_content = self.get_page(self.url)

    


