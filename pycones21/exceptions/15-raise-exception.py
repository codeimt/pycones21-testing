import pytest


def raise_exception():
    raise Exception("error")


def test_raises_exception():
    with pytest.raises(Exception) as error:
        raise_exception()
        assert str(error.value) == "Some other string"
