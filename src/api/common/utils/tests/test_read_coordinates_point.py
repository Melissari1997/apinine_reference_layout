from utils import read_coordinates_point


class TestReadCoordinatesPoint:
    def test_primo(self):
        want = 2
        got = read_coordinates_point()
        assert want == got
