# The proposed response structure is suggested here:
# https://google.github.io/styleguide/jsoncstyleguide.xml

# TODO: Verify whether we need to add some metadata fields to our output, such as:
#     "apiVersion": "1.0"
#     "id": "9a728uH5PM"

# example valid response:
# {
#     "data": {
#         "address": "Via Milazzo, 193, 27100 Pavia PV, Italy",
#         "flood_risk_assessment": {
#             "return_period_20y": {
#                 "intensity": {"water_height": 2.6},
#                 "vulnerability": 0.81,
#             },
#             "return_period_100y": {
#                 "intensity": {"water_height": 2.7},
#                 "vulnerability": 0.82,
#             },
#             "return_period_200y": {
#                 "intensity": {"water_height": 2.7},
#                 "vulnerability": 0.82,
#             },
#         },
#         "risk_index": 5,
#         "average_annual_loss": 0.0408,
#     },
# }
# example error response:
# {
#     "data": {}, "error": {"code": 404, "message": "Unable to identify provided address"}
# }

import traceback

from errors import ConflictingInputsError
from geocoder.geocoder import FailedGeocodeError
from status_codes import StatusCodes


# TODO: structure the code better? Move logic of response format elsewhere?
def handle_response(func):
    def response_wrapper(*args, **kwargs):
        def exception_wrapper(*args, **kwargs):
            data, err_code, err_message = {}, None, None
            try:
                data = func(*args, **kwargs)
            except ConflictingInputsError:
                err_code, err_message = StatusCodes.CONFLICTING_INPUTS
            except FailedGeocodeError:
                err_code, err_message = StatusCodes.UNKNOWN_ADDRESS
            except Exception:
                err_code, err_message = StatusCodes.INTERNAL_SERVER_ERROR
                print(traceback.format_exc())

            return data, (err_code, err_message)

        data, (err_code, err_message) = exception_wrapper(*args, **kwargs)

        response = {"data": data}
        if err_code and err_message:
            response["error"] = {"code": err_code, "message": err_message}

        return response

    return response_wrapper
