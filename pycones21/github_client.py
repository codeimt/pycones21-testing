import os
import requests

from typing import Optional, Dict


class GithubClient:

    API_HOST = "https://api.github.com"
    TOKEN = os.getenv("GITHUB_TOKEN")
    AUTH_HEADERS = {"Authorization": f"token {TOKEN}"}

    @classmethod
    def _get(cls, url: str, extra_headers: Optional[Dict] = None):

        if not extra_headers:
            extra_headers = {}

        headers = {"Authorization": cls.AUTH_HEADERS}
        headers.update(**extra_headers)

        response = requests.get(url, headers=headers)

        return response

    @classmethod
    def get_gists_urls(cls):
        response = cls.get_gists()

        return [gist["url"] for gist in response.json()]

    @classmethod
    def get_gists(cls):
        LIST_GISTS_ENDPOINT = f"{cls.API_HOST}/gists"

        response = cls._get(LIST_GISTS_ENDPOINT)

        return response

    @classmethod
    def create_gist(cls, description: str, content: str):
        CREATE_GISTS_ENDPOINT = f"{cls.API_HOST}/gists"

        data = {"description": description, "files": {"content": content}}
        response = requests.post(CREATE_GISTS_ENDPOINT, data, headers=cls.AUTH_HEADERS)

        return response
