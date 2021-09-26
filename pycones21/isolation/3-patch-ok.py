from pycones21.github_client import GithubClient
from unittest import mock


# Or you could use a decorator
@mock.patch("pycones21.github_client.requests.get")
def test_get_gist_urls(m_request):

    response_urls = [
        {
            "url": "https://api.github.com/gists/fc04e72fc7bb4bf0a6c7c09551ad9c34",
        }
    ]

    m_response = mock.MagicMock()
    m_response.json.return_value = response_urls

    m_request.return_value = m_response

    urls = GithubClient.get_gists_urls()

    assert urls == [response_urls[0]["url"]]


def test_get_gist_names():

    assert isinstance(GithubClient._get, mock.Mock)
