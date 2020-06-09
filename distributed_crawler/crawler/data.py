from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class RequiredData:
    key: str
    xpath: str


@dataclass
class Domain:
    url: str
    required_data: List[RequiredData]
    created_at: datetime = datetime.now()


