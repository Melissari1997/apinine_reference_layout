class StatusCodes:
    QUERYSTRING_ERROR = (
        400,
        "Either 'address' or both 'lat' and 'lon' parameters must be supplied. 'lon' must be between -22 and 45, 'lat' must be between 27 and 72",
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
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")
