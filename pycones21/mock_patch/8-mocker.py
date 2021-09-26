from pycones21.user_store import UserStore


def test_mocker_context(mocker):
    with mocker.patch.object(UserStore, "count"):
        assert isinstance(UserStore.count, mocker.MagicMock)
