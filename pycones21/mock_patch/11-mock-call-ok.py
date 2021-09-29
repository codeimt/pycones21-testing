from unittest import mock
from pycones21.github_client import GithubClient


@mock.patch.object(GithubClient, "_get")
def test_assertion(m_get):
    with mock.patch.object(GithubClient, "get_gists_urls") as m_get_gists:
        GithubClient.get_gists()
    m_get_gists.assert_called_once()
