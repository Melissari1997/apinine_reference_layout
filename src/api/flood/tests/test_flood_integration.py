from geocoder.gmaps_geocoder import GMapsGeocoder
from main import handler, main
from readgeodata.rasterioreader import RasterIOReader
from schema import OutputSchema


# Real calls to gmaps and aws
class TestFloodIntegration:
    def test_integ_main(self, geotiff_path_s3):
        lon, lat = 12.215283630441727, 44.88393348245498
        gmaps = GMapsGeocoder()
        rioreader = RasterIOReader()
        got = main(
            filename=geotiff_path_s3["GEOTIFF_PATH"],
            address=None,
            lon=lon,
            lat=lat,
            geocoder=gmaps,
            geodatareader=rioreader,
        )

        # Checking only format and types, not the values
        OutputSchema(**got)

    def test_integ_handler_address(self, geotiff_path_s3, event_address):
        got = handler(event=event_address, context=None)

        want_status_code = 200
        OutputSchema(**got["body"])

        assert want_status_code == got["statusCode"]

    def test_integ_handler_filename(self, event_address):
        got = handler(event=event_address, context=None)

        want_status_code = 500
        wanted_body = "Internal Server Error"

        assert want_status_code == got["statusCode"]
        assert wanted_body == got["body"]

    def test_integ_handler_lat_lon(self, geotiff_path_s3, event_lat_lon):
        # got = handler(event=event_lat_lon, context=None)

        assert 1 == 2

    def test_integ_handler_conflicting(self, geotiff_path_s3):
        assert 1 == 2

    def test_integ_invalid_address(self, geotiff_path_s3):
        assert 1 == 2
