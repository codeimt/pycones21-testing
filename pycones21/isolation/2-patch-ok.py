from pycones21.github_client import GithubClient
from unittest import mock


def test_get_gist_urls():

    response_urls = [
        {
            "url": "https://api.github.com/gists/fc04e72fc7bb4bf0a6c7c09551ad9c34",
        }
    ]

    m_response = mock.MagicMock()
    m_response.json.return_value = response_urls

    # Wrap the code where we want the patch to take effect with a context manager
    with mock.patch.object(GithubClient, "_get", return_value=m_response):
        urls = GithubClient.get_gists_urls()

    assert urls == [response_urls[0]["url"]]


def test_get_gist_names():

    assert isinstance(GithubClient._get, mock.Mock)
