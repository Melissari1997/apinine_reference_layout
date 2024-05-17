import json
import os

from aws_lambda_powertools import Logger
from pydantic import ValidationError

from .errors import QuerystringInputError
from .input_schema import QueryStringRCPSchema, QueryStringSchema, validate_query_params
from .status_codes import StatusCodes

logger = Logger()


def is_baseline_scenario(geotiff_list: list) -> bool:
    # In baseline scenario my json must be made of a single entry, without the "year" key
    if len(geotiff_list) == 1 and "year" not in geotiff_list[0]:
        return True
    # In RCP scenario my json must:
    # - be made of one or more entries
    # - have a "year" key for each entry, each with a different value
    # - have a "climate_scenario" key for each entry, all with the same value
    if (
        len(geotiff_list) >= 1
        and all("year" in entry for entry in geotiff_list)
        and len([entry["year"] for entry in geotiff_list])
        == len({entry["year"] for entry in geotiff_list})
        and all("climate_scenario" in entry for entry in geotiff_list)
        and len({entry["climate_scenario"] for entry in geotiff_list}) == 1
    ):
        return False
    raise ValueError(f"Unexpected value of GEOTIFF_JSON: {geotiff_list}")


class BaselineParser:
    def __init__(self, geotiff_list: list):
        self.geotiff = geotiff_list[0]

    def parse(self, event: dict) -> tuple[str, str, float, float]:
        logger.info("Parsing event for baseline scenario")
        query_params = event.get("queryStringParameters")
        # AWS sets the value to None when no parameter is passed
        if query_params is None:
            query_params = {}

        filename = self.geotiff["path"]
        try:
            validate_query_params(model=QueryStringSchema, params=query_params)
        except ValidationError as ve:
            code, msg = StatusCodes.QUERYSTRING_ERROR
            raise QuerystringInputError(code=code, msg=msg) from ve

        address = query_params.get("address")

        lat = query_params.get("lat")
        if lat is not None:
            lat = float(lat)

        lon = query_params.get("lon")
        if lon is not None:
            lon = float(lon)

        return filename, address, lat, lon


class RCPParser:
    def __init__(self, geotiff_list: list):
        self.geotiff_list = geotiff_list
        self.years = self.parse_years(geotiff_list)

    def parse_years(self, geotiff_list: list) -> list:
        return [tiff["year"] for tiff in geotiff_list]

    def get_tiff_path_from_year(self, year: str) -> str:
        return next(
            (entry["path"] for entry in self.geotiff_list if entry["year"] == str(year))
        )

    def parse(self, event: dict) -> tuple[str, str, float, float]:
        logger.info("Parsing event for rcp scenario")

        query_params = event.get("queryStringParameters")
        # AWS sets the value to None when no parameter is passed
        if query_params is None:
            query_params = {}
        query_params["valid_years"] = self.years
        try:
            validated_params = validate_query_params(
                model=QueryStringRCPSchema, params=query_params
            )
        except ValidationError as ve:
            code, msg = StatusCodes.QUERYSTRING_ERROR_RCP
            raise QuerystringInputError(code=code, msg=msg.format(self.years)) from ve

        year = validated_params["year"]
        filename = self.get_tiff_path_from_year(year)

        address = query_params.get("address")

        lat = query_params.get("lat")
        if lat is not None:
            lat = float(lat)

        lon = query_params.get("lon")
        if lon is not None:
            lon = float(lon)

        return filename, address, lat, lon


def parse_aws_event(event: dict) -> tuple[str, str, float, float]:
    """Parse AWS Lambda event and extract data.

    Depending on the environment, it processes the event associated either with the baseline scenario,
    or with a RCP scenario. In the second case, the query parameter "year" is expected to be found
    in the event query parameters.

    Parameters
    ----------
    event : dict
        Lambda event.

    Returns
    -------
    tuple[str, str, float, float]
        Tuple of filename, address, lat and lon

    Raises
    ------
    ValueError
        Raised in case of missing GEOTIFF_PATH env variable
    """
    geotiff_json = os.environ.get("GEOTIFF_JSON")

    if not geotiff_json:
        raise ValueError("Missing env var GEOTIFF_JSON")

    try:
        geotiff_list = json.loads(geotiff_json)
    except json.JSONDecodeError:
        raise ValueError(f"Variable is not a valid JSON: {geotiff_json}") from None

    if is_baseline_scenario(geotiff_list):
        return BaselineParser(geotiff_list).parse(event)
    return RCPParser(geotiff_list).parse(event)
