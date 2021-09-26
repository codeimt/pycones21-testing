from pycones21.user_store import UserStore
from pycones21.fake_store import FakeStore


def test_create_user():
    user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

    assert user.username == "ismaelmt"

    assert user.email == "ismael@ismael.com"
    assert UserStore.count() == 1


def test_user_amount():

    # We want that each test have a clean DB
    # This test will fail, but it shouldn't.
    assert FakeStore.count() == 0
