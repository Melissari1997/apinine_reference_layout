class StatusCodes:
    CONFLICTING_INPUTS = (
        422,
        "Either 'address' or both 'lat' and 'long' parameters must be supplied",
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
