from pycones21.user_store import UserStore


def new_count():
    return 10


def test_mocker_context_fail(mocker):
    with mocker.patch.object(UserStore, "count", new=new_count):
        assert isinstance(UserStore.count, mocker.MagicMock)
