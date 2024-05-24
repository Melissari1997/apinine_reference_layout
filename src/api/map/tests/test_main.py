# - testare che un layer inesistente sollevi errore correttamente
# - testare comportamento quando ho NaN
# - testare compostamento quando sono out of bounds
import numpy as np
import pytest
import rasterio
from common.errors import BandNotFoundError
from main import main


class MockRasterIODataSet:
    def __init__(self, descriptions):
        self._descriptions = descriptions

    def __getattr__(self, name):
        if name == "descriptions":
            return self._descriptions
        return self

    def __call__(self, *args, **kwargs):
        raise ValueError()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def mock_rasterio_open(*args, **kwargs):
    descriptions = ["band1", "band2", "band3"]
    return MockRasterIODataSet(descriptions=descriptions)


class MockMapReader:
    def read(self, *args, **kwargs):
        return np.ones((10, 10, 3)), {}


class MockMapConverter:
    def convert(self, data, *args, **kwargs):
        return str(data.sum())


@pytest.mark.unit
class TestMapMainUnit:

    # This merely tests whether other objects can be injected changing the function behaviour
    def test_success(self, box_3035_verruca, monkeypatch):
        layer = "band1"
        monkeypatch.setattr(rasterio, "open", mock_rasterio_open)
        mock_map_reader = MockMapReader()
        mock_map_converter = MockMapConverter()
        got = main(
            filename="myfile",
            box_3035=box_3035_verruca,
            layer=layer,
            map_reader=mock_map_reader,
            map_converter=mock_map_converter,
            layer_to_range={layer: (0, 1)},
        )
        want = "100.0"
        assert got == want

    def test_band_not_found_error(self, box_3035_verruca, monkeypatch):
        monkeypatch.setattr(rasterio, "open", mock_rasterio_open)
        with pytest.raises(BandNotFoundError):
            main(
                filename="myfile",
                box_3035=box_3035_verruca,
                layer="wronglayer",
                map_reader={},
                map_converter={},
                layer_to_range={},
            )
