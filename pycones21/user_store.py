from pycones21.fake_store import FakeStore
from pycones21.data_models import User


class UserStore:

    namespace_name = "users"

    @classmethod
    def create_user(cls, username: str, email: str) -> User:

        if not FakeStore.namespace_exists("users"):
            FakeStore.set_namespace("users")

        user = User(id=cls.count() + 1, username=username, email=email)

        FakeStore.set(cls.namespace_name, str(user.id), user)

        return user

    @classmethod
    def get_user_by_id(cls, user_id: int) -> User:

        return FakeStore.get(cls.namespace_name, str(user_id))

    @classmethod
    def count(cls) -> int:
        return FakeStore.count(cls.namespace_name)
