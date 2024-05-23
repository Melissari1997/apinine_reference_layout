import pytest
from cache import LambdaCache


class TestLambdaCache:
    def test_cache_miss(self):
        cache = LambdaCache(max_size=10)
        with pytest.raises(KeyError):
            cache.get("somethingwrong")

    def test_cache_hit(self):
        cache = LambdaCache(max_size=10)
        want_key, want_value = "mykey", "myvalue"
        cache.set(want_key, want_value)
        got_value = cache.get(want_key)

        assert want_value == got_value

    def test_cache_size(self):
        cache = LambdaCache(max_size=2)
        # add one entry
        want_key, want_value = "mykey", "myvalue"
        cache.set(want_key, want_value)
        # I find it
        _ = cache.get(want_key)

        # add a second entry
        want_key2, want_value2 = "mykey2", "myvalue2"
        cache.set(want_key2, want_value2)
        # I find it
        _ = cache.get(want_key2)

        # add a third entry
        want_key3, want_value3 = "mykey3", "myvalue3"
        cache.set(want_key3, want_value3)
        # I find it
        _ = cache.get(want_key3)

        # I expect the second value to still be present
        _ = cache.get(want_key2)

        # I expect the first value has been discarded
        with pytest.raises(KeyError):
            cache.get(want_key)
