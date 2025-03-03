import json
from typing import Callable

from aws_lambda_powertools import Logger, Tracer
from geocoder.geocoder import (
    FailedGeocodeError,
    MultipleMatchesForAddressError,
    OutOfBoundsError,
)
from pydantic import BaseModel, ValidationError

from .errors import BandNotFoundError, InvalidYearError, MissingDataError
from .http_headers import response_headers
from .status_codes import StatusCodes

logger = Logger(serialize_stacktrace=True)
tracer = Tracer()


@tracer.capture_method
def handle_response(validate_schema: BaseModel) -> Callable:
    """Decorator handling common exceptions and formatting.

    This does the following:
    - Calls the decorated function with the provided parameters
    - Catches any exceptions and generate HTTP status code and error message accordingly
    - Validate the decorated function's output with 'validate_schema' Pydantic model
    - Format the output according to AWS Proxy Integration between Lambda and API Gateway

    Parameters
    ----------
    validate_schema : BaseModel
        Pydantic model the decorated function's output has to be validated against.

    Returns
    -------
    Callable
        The decorated function.
    """

    def function_wrapper(func: Callable) -> Callable:
        def response_wrapper(*args, **kwargs) -> Callable:
            """Wrapper for 'exception_wrapper'. Format the response object.

            This calls the privately-defined 'exception_wrapper' and returns a
            dictionary whose keys are recognized by AWS Lambda Proxy Integration
            with AWS API Gateway.
            """

            def exception_wrapper(*args, **kwargs) -> tuple[dict, tuple[int, str]]:
                """Wraps an external-scoped 'func' function and handles exceptions.

                Invoke the 'func' function, catches any exceptions and associate them
                with the proper HTTP status code and error message to be included
                in the body. If an unexpected exception is thrown, a '500 Internal Server
                Error' is returned.

                Returns
                -------
                tuple
                    The three returned objects are: the dictionary to be json-encoded into
                    the 'body' response field, the HTTP response status code and the error
                    message, if any.
                """
                body, status_code, err_message = {}, 200, None
                try:
                    raw_body = func(*args, **kwargs)
                # Static errors
                except FailedGeocodeError:
                    status_code, err_message = StatusCodes.UNKNOWN_ADDRESS
                except OutOfBoundsError:
                    status_code, err_message = StatusCodes.OUT_OF_BOUNDS
                except MultipleMatchesForAddressError:
                    status_code, err_message = StatusCodes.UNKNOWN_ADDRESS
                except BandNotFoundError:
                    status_code, err_message = StatusCodes.LAYER_NOT_FOUND
                # Errors raising dynamic error message
                except InvalidYearError as ye:
                    status_code, _ = StatusCodes.QUERYSTRING_ERROR
                    err_message = ye.msg
                # Validation errors with custom error message
                except ValidationError as ve:
                    status_code, _ = StatusCodes.QUERYSTRING_ERROR
                    err_message = ve.title
                # Unexpected errors
                except Exception as e:
                    logger.exception(e)
                    status_code, err_message = StatusCodes.INTERNAL_SERVER_ERROR
                # When there is no error, validate output
                else:
                    try:
                        body = validate_schema(**raw_body).model_dump()
                    except MissingDataError:
                        status_code, err_message = StatusCodes.MISSING_DATA
                    # Raise error if schema is not what I expect
                    except Exception as ve:
                        logger.exception(ve)
                        status_code, err_message = StatusCodes.INTERNAL_SERVER_ERROR

                return body, (status_code, err_message)

            body, (status_code, err_message) = exception_wrapper(*args, **kwargs)

            response = {
                "body": err_message or json.dumps(body),
                "statusCode": status_code,
                "headers": response_headers,
            }
            return response

        return response_wrapper

    return function_wrapper
