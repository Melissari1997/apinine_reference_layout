# The proposed response structure is suggested here:
# https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-create-api-as-simple-proxy-for-lambda.html

import traceback

from geocoder.geocoder import FailedGeocodeError

from .errors import ConflictingInputsError
from .status_codes import StatusCodes


def handle_response(func):
    def response_wrapper(*args, **kwargs):
        def exception_wrapper(*args, **kwargs):
            body, status_code, err_message = {}, 200, None
            try:
                body = func(*args, **kwargs)
            except ConflictingInputsError:
                status_code, err_message = StatusCodes.CONFLICTING_INPUTS
            except FailedGeocodeError:
                status_code, err_message = StatusCodes.UNKNOWN_ADDRESS
            except Exception:
                status_code, err_message = StatusCodes.INTERNAL_SERVER_ERROR
                print(traceback.format_exc())

            return body, (status_code, err_message)

        body, (status_code, err_message) = exception_wrapper(*args, **kwargs)

        response = {"body": body or err_message, "statusCode": status_code}

        return response

    return response_wrapper
