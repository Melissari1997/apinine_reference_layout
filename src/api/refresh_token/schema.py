from typing import Literal

from pydantic import BaseModel, HttpUrl


class EnvSchema(BaseModel):
    POWERTOOLS_LOG_LEVEL: Literal["INFO", "DEBUG", "ERROR"]
    URL: HttpUrl
    APP_CLIENT_ID: str
    POWERTOOLS_SERVICE_NAME: str
