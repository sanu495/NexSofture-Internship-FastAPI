from pydantic import BaseModel
from typing import Optional, TypeVar, Generic

T = TypeVar("T")

class ResponseTo(BaseModel, Generic[T]):
    message:str
    status: str | int
    response: Optional[T] = None