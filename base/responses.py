from typing import Any, Optional

class RepositoryResponse:
    def __init__(self, success: bool, message: str, data: Optional[Any] = None):
        self.success = success
        self.message = message
        self.data = data

class APIResponse:
    def __init__(self, success: bool, message: str, data: Optional[Any] = None, status: int = 200):
        self.success = success
        self.message = message
        self.data = data
        self.status = status