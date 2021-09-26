from dataclasses import dataclass


@dataclass
class User:

    id: int
    username: str
    email: str

    def get_username(self):
        return self.username
