# - testare che un layer inesistente sollevi errore correttamente
# - testare comportamento quando ho NaN
# - testare compostamento quando sono out of bounds
import pytest
import rasterio
from common.errors import BandNotFoundError
from main import main


class MockRasterIODataSetValueError:
    def __getattr__(self, name):
        # Return self to allow chaining
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __call__(self, *args, **kwargs):
        # Raise the specified error when the object is called
        raise ValueError


@pytest.mark.unit
class TestMapMainUnit:
    def test_band_not_found_error(self, box_3035_verruca, monkeypatch):

        def mock_open(*args, **kwargs):
            return MockRasterIODataSetValueError()

        monkeypatch.setattr(rasterio, "open", mock_open)
        with pytest.raises(BandNotFoundError):
            main(
                filename="myfile",
                box_3035=box_3035_verruca,
                layer="wronglayer",
                map_reader={},
                map_converter={},
                layer_to_range={},
            )
