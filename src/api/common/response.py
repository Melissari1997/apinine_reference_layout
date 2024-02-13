import traceback

from aws_lambda_powertools import Logger
from geocoder.geocoder import (
    FailedGeocodeError,
    MultipleMatchesForAddressError,
    OutOfBoundsError,
)

from .errors import ConflictingInputsError, MissingDataError
from .status_codes import StatusCodes

logger = Logger()


def handle_response(validate_schema):
    def function_wrapper(func):
        def response_wrapper(*args, **kwargs):
            def exception_wrapper(*args, **kwargs):
                body, status_code, err_message = {}, 200, None
                try:
                    raw_body = func(*args, **kwargs)
                    body = validate_schema(**raw_body).model_dump()
                except ConflictingInputsError:
                    status_code, err_message = StatusCodes.CONFLICTING_INPUTS
                except FailedGeocodeError:
                    status_code, err_message = StatusCodes.UNKNOWN_ADDRESS
                except OutOfBoundsError:
                    status_code, err_message = StatusCodes.OUT_OF_BOUNDS
                except MultipleMatchesForAddressError:
                    status_code, err_message = StatusCodes.UNKNOWN_ADDRESS
                except MissingDataError:
                    status_code, err_message = StatusCodes.MISSING_DATA
                except Exception:
                    status_code, err_message = StatusCodes.INTERNAL_SERVER_ERROR
                    logger.error(traceback.format_exc())

                return body, (status_code, err_message)

            body, (status_code, err_message) = exception_wrapper(*args, **kwargs)

            response = {"body": body or err_message, "statusCode": status_code}
            return response

        return response_wrapper

    return function_wrapper
