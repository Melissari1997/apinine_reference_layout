# TODO: define only generic errors. Then, each API endpoint (or group of endpoints) should define their own
# list of specific errors. This way I do not retrigger the build of wildfire if I define a new catchable Exception
# for each new endpoint I implement.
class StatusCodes:
    QUERYSTRING_ERROR = (
        400,
        "Either 'address' or both 'lat' and 'lon' parameters must be supplied. 'lon' must be between -22 and 45, 'lat' must be between 27 and 72",
    )
    # Returned when client provides an invalid input year
    QUERYSTRING_ERROR_RCP = (
        400,
        "Either 'address' or both 'lat' and 'lon' parameters must be supplied. 'lon' must be between -22 and 45, 'lat' must be between 27 and 72. Year must be a positive integer",
    )
    # Returned when GMaps api fails to geocode provided address
    UNKNOWN_ADDRESS = (
        404,
        "Unable to identify provided address",
    )
    # Returned when the value inside the .tif is nodata
    MISSING_DATA = (
        404,
        "Data not available for the selected point",
    )
    # Returned when the query refers to an address the user can not access
    OUT_OF_BOUNDS = (
        400,
        "The provided address is out of bounds",
    )
    LAYER_NOT_FOUND = (400, "The provided layer does not exist")
    BATCH_REQUEST_INVALID_BODY = (
        400,
        "Invalid input. Align body format to the specification provided in the API documentation and try again.",
    )
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")
