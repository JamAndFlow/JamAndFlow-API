from typing import Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str
    code: str
    status_code: int
    context: Optional[dict] = None
