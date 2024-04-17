from typing import Literal

from pydantic import BaseModel, HttpUrl


class EnvSchema(BaseModel):
    POWERTOOLS_LOG_LEVEL: Literal["INFO", "DEBUG", "ERROR"]
    POWERTOOLS_SERVICE_NAME: str
    URL_USERINFO: HttpUrl
    USER_DB_PARAMETER_NAME: str
