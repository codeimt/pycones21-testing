from unittest import mock
from pycones21.service import call_github


@mock.patch("pycones21.service.GithubClient.get_gists")
def test_get_gists(m_gists):

    call_github()
    m_gists.assert_called_once()
