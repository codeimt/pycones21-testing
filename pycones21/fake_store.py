# Helper module to simulate a data store
from typing import Any, Optional


class FakeStore:
    _data = {}

    @classmethod
    def clean(cls):
        cls._data = {}

    @classmethod
    def set(cls, namespace: str, key: str, val: Any) -> None:
        cls._data[namespace][key] = val

    @classmethod
    def namespace_exists(cls, namespace):
        return namespace in cls._data

    @classmethod
    def set_namespace(cls, namespace: str) -> None:
        cls._data[namespace] = {}

    @classmethod
    def get(cls, namespace: str, key: str) -> Any:
        return cls._data[namespace][key]

    @classmethod
    def count(cls, namespace: Optional[str] = None) -> int:
        if not namespace:
            return len(cls._data.items())
        return len(cls._data[namespace].items())
