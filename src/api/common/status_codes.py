class StatusCodes:
    # TODO: complete list of errors
    CONFLICTING_INPUTS = (
        422,
        "Either 'address' or both 'lat' and 'long' parameters must be supplied",
    )
    UNKNOWN_ADDRESS = (
        404,
        "Unable to identify provided address",
    )
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error")
