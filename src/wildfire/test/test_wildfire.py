from main import handler


class TestWildfire:
    def test_wildfire_out(self):
        want = 0
        got = handler()

        assert got == want
