import csv
from io import StringIO
from typing import Dict, List

import pytest
from functions import hexdigest, list_to_csv


@pytest.mark.unit
class TestHexdigest:
    def test_hexdigest_equal_strings_and_tags(self):
        string = "mylongstring"
        tags = "filename=s3://my/tiff/file".encode()
        bdata1 = string.encode()
        bdata2 = string.encode()

        digest1 = hexdigest(bdata=bdata1, tags=tags)
        digest2 = hexdigest(bdata=bdata2, tags=tags)

        assert isinstance(digest1, str)
        assert isinstance(digest2, str)
        assert digest1 == digest2

    def test_hexdigest_different_strings_equal_tags(self):
        bdata1 = "string1".encode()
        bdata2 = "string2".encode()
        tags = "filename=s3://my/tiff/file".encode()

        digest1 = hexdigest(bdata=bdata1, tags=tags)
        digest2 = hexdigest(bdata=bdata2, tags=tags)

        assert isinstance(digest1, str)
        assert isinstance(digest2, str)
        assert digest1 != digest2

    def test_hexdigest_different_tags_same_string(self):
        string = "mylongstring"
        tags1 = "filename=s3://my/tiff/file1".encode()
        tags2 = "filename=s3://my/tiff/file2".encode()
        bdata1 = string.encode()
        bdata2 = string.encode()

        digest1 = hexdigest(bdata=bdata1, tags=tags1)
        digest2 = hexdigest(bdata=bdata2, tags=tags2)

        assert isinstance(digest1, str)
        assert isinstance(digest2, str)
        assert digest1 != digest2


def compare_list_to_csv(
    dictionary: Dict, fieldnames: List, csv_data: str, delimiter: str = "|"
):
    reader = csv.DictReader(
        StringIO(csv_data),
        fieldnames=fieldnames,
        delimiter=delimiter,
        quoting=csv.QUOTE_NONNUMERIC,
    )

    # Remove headers
    _ = next(reader)

    assert list(reader) == dictionary


@pytest.mark.unit
class TestListToCSV:
    def test_list_to_csv_success(self):
        data = [
            {"lon": 14.23, "lat": 11.03, "address": "a1"},
            {"lon": 43.52, "lat": 12.32, "address": "a2"},
            {"lon": 23.21, "lat": 9.23, "address": "a3"},
        ]
        fieldnames = ["lon", "lat", "address"]
        csv_data = list_to_csv(data=data, fieldnames=fieldnames, delimiter="|")
        assert isinstance(csv_data, str)
        compare_list_to_csv(dictionary=data, fieldnames=fieldnames, csv_data=csv_data)

    def test_dict_to_csv_strange_chars(self):
        data = [
            {"lon": 14.23, "lat": 11.03, "address": '   my ""  strange|a||ddres|||ss '},
            {"lon": 43.52, "lat": 12.32, "address": ""},
            {"lon": 23.21, "lat": 9.23, "address": " ''''''  "},
        ]
        fieldnames = ["lon", "lat", "address"]
        csv_data = list_to_csv(data=data, fieldnames=fieldnames, delimiter="|")
        assert isinstance(csv_data, str)
        compare_list_to_csv(dictionary=data, fieldnames=fieldnames, csv_data=csv_data)
