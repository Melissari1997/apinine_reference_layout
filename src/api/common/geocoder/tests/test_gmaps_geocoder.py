import pytest
from geocoder.geocoder import FailedGeocodeError
from geocoder.gmaps_geocoder import GMapsGeocoder


class TestGMapsGeocoder:
    def test_geocode_success(self):
        geocoder = GMapsGeocoder()
        valid_address = "via verruca 1 trento"
        coords, formatted_address = geocoder.geocode(valid_address)

        assert isinstance(coords, tuple)
        assert len(coords) == 2
        assert isinstance(coords[0], float)
        assert isinstance(coords[1], float)
        assert isinstance(formatted_address, str)

    def test_geocode_fails(self):
        geocoder = GMapsGeocoder()
        invalid_address = "huasidb12983db210o3gdb120od39gh198732dg"

        with pytest.raises(FailedGeocodeError):
            coords, formatted_address = geocoder.geocode(invalid_address)
