from enum import Enum
from typing import Dict
import urllib.parse

class OperationMethod(Enum):
    GET = 'GET'
    POST = 'POST'
        
class MonitorEntry:
    def __init__(self, method: OperationMethod, operation_id:str, base_urls:Dict[str, str], path:str, request_body=None):
        self.base_urls = base_urls
        self.path = path
        self.method = method
        self.operation_id = operation_id
        self.request_body = request_body

    def get_urls(self) -> Dict[str, str]:
        urls = {}
        for key, base_url in self.base_urls.items():
            urls[f'{key}-{self.operation_id}'] = urllib.parse.urljoin(base_url, self.path)
        return urls
