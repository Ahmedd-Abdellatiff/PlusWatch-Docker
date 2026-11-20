from datetime import datetime
from pydantic import BaseModel, ConfigDict, HttpUrl


class WebsiteCreate(BaseModel):
    name: str
    url: HttpUrl


class WebsiteResponse(BaseModel):
    id: int
    name: str
    url: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WebsiteCheckResponse(BaseModel):
    id: int
    website_id: int
    status_code: int | None
    response_time: int | None
    is_up: bool
    checked_at: datetime

    model_config = ConfigDict(from_attributes=True)