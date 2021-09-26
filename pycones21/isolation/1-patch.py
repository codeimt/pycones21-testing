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

    mock.patch.object(GithubClient, "_get", return_value=m_response).start()
    urls = GithubClient.get_gists_urls()

    assert urls == [response_urls[0]["url"]]


def test_get_gist_names():

    # The mock is still applied as a side-effect from the previous test
    assert isinstance(GithubClient._get, mock.Mock)
