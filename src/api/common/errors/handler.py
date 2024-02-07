from api.common.errors.errors import ConflictingInputsError, FailedGeocodeError


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            # TODO: exit with 200 OK response
            return result

        # TODO: exit with appropriate HTTP status code
        except ConflictingInputsError as cie:
            print(str(cie))
        except FailedGeocodeError as fge:
            print(str(fge))
        except Exception:
            raise

    return wrapper
