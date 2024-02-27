import pytest


@pytest.fixture(scope="function")
def querystring_table():
    yield {}
