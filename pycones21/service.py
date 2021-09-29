from pycones21.github_client import GithubClient


def call_github():
    gists = GithubClient.get_gists()
    return gists
