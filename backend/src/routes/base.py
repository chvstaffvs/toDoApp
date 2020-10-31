from typing import Any, Dict, List, Optional, Type
from fastapi import APIRouter


class CustomRouter(APIRouter):
    def create(self, path: str, *, response_model: Optional[Type[Any]]):
        return self.post(path, response_model=response_model, status_code=201)


def filter_generator(locals_: Dict[str, Any], exclude: List[str] = []):
    return {
        key: value
        for key, value in locals_.items()
        if value is not None and key not in exclude
    }
