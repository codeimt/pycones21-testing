import pytest
from unittest import TestCase
from pycones21.data_models import User
from pycones21.fake_store import FakeStore
from pycones21.user_store import UserStore


# pytest function
def test_get_fake_store():

    user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

    assert FakeStore.get("users", "1") == user


# pytest class
class TestFakeStorePytest:
    @pytest.fixture(autouse=True)
    def fake_store(self):
        FakeStore.clean()

    def test_get_fake_store_in_class(self):

        user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

        assert FakeStore.get("users", "1") == user


# unittest class
class TestFakeStore(TestCase):
    def setUp(self):
        FakeStore.clean()

    def test_get_fake_store_in_class(self):

        user = UserStore.create_user(username="ismaelmt", email="ismael@ismael.com")

        assert FakeStore.get("users", "1") == user
