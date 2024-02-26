import os

from jsonschema import validate

from .input_schema import querystring_schema


def parse_aws_event(event: dict) -> tuple[str, str, float, float]:
    """Parse AWS Lambda event and extract data.

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
    filename = os.environ.get("GEOTIFF_PATH")

    if filename is None:
        raise ValueError("Missing env var GEOTIFF_PATH")

    query_params = event.get("queryStringParameters")

    validate(instance=query_params, schema=querystring_schema)

    address = query_params.get("address")

    lat = query_params.get("lat")
    if lat is not None:
        lat = float(lat)

    lon = query_params.get("lon")
    if lon is not None:
        lon = float(lon)

    return filename, address, lat, lon
