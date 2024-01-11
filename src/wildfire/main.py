from common.errors.errors import error
from common.utils.utils import common_func


def handler():
    common_func()
    print("I am wildfire")
    error("Calling error")
    return 0


if __name__ == "__main__":
    handler()
