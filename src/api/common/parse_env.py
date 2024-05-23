import abc
import json
from typing import Dict

from .errors import InvalidYearError


class EnvParser(abc.ABC):
    def __init__(self, environ: Dict[str, str]):
        geotiff_json = environ.get("GEOTIFF_JSON")

        if geotiff_json is None:
            raise ValueError("Missing env var GEOTIFF_JSON")

        try:
            self.geotiff_list = json.loads(geotiff_json)
        except json.JSONDecodeError:
            raise ValueError(f"Variable is not a valid JSON: {geotiff_json}") from None

    @abc.abstractmethod
    def get_filename(self) -> str: ...


class BaselineEnvParser(EnvParser):
    def __init__(self, environ: Dict[str, str]):
        super().__init__(environ)

    def get_filename(self, *args, **kwargs) -> str:
        return self.geotiff_list[0]["path"]


class RCPEnvParser(EnvParser):
    def __init__(self, environ: Dict[str, str]) -> str:
        super().__init__(environ)

    def get_filename(self, **kwargs) -> str:
        try:
            return next(
                entry["path"]
                for entry in self.geotiff_list
                if str(entry["year"]) == str(kwargs.get("year"))
            )
        except StopIteration:
            years = [str(entry["year"]) for entry in self.geotiff_list]
            raise InvalidYearError(years) from None
