class TestLeakUsers:
    @classmethod
    def setup_class(cls):
        cls.user = {"name": "Lola Mento", "username": "iamauser@user.com"}

    def test_username(self):
        self.user["name"] = "Elsa Murito"

        assert self.user["username"] == "iamauser@user.com"

    def test_name(self):

        # Capasao!??
        assert self.user["name"] == "Lola Mento"
