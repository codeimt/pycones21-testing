from unittest import mock
from pycones21.fake_store import FakeStore


# Patch hell
def test_nested_mocks():
    with mock.patch.object(FakeStore, "namespace_exists") as m1:
        with mock.patch.object(FakeStore, "get") as m2:
            with mock.patch.object(FakeStore, "set_namespace") as m3:
                with mock.patch.object(FakeStore, "count") as m4:
                    assert isinstance(m1, mock.MagicMock)
                    assert isinstance(m2, mock.MagicMock)
                    assert isinstance(m3, mock.MagicMock)
                    assert isinstance(m4, mock.MagicMock)


@mock.patch.multiple(
    FakeStore,
    namespace_exists=mock.DEFAULT,
    get=mock.DEFAULT,
    set_namespace=mock.DEFAULT,
    count=mock.DEFAULT,
)
def test_multimock(**mocks):
    namespace_exists, get, set_namespace, count = mocks.values()
    assert isinstance(namespace_exists, mock.MagicMock)
    assert isinstance(get, mock.MagicMock)
    assert isinstance(set_namespace, mock.MagicMock)
    assert isinstance(count, mock.MagicMock)
