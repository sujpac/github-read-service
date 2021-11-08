import os, requests, logging
from github import Github

from . import constants


logger = logging.getLogger(__name__)


def is_github_available():
    response = proxy_request('zen')
    return response and response.status_code == 200


def get_org(org_name):
    """Gets org from Github"""
    token = os.getenv(constants.API_KEY_NAME, '...')
    ghub = Github(token)
    try:
        return ghub.get_organization(org_name)
    except BaseException as err:
        logger.error(f"Unexpected {err=}, {type(err)=}")
        return None


def get_repos(org_name, org=None):
    """Gets all repos of a given org from Github"""
    if not org:
        org = get_org(org_name)
        if not org:
            return None
    try:
        repos = org.get_repos()
    except BaseException as err:
        logger.error(f"Unexpected {err=}, {type(err)=}")
        return None
    return [repo for repo in repos]


def proxy_request(resource):
    """Proxies a GET request to the Github API"""
    token = os.getenv(constants.API_KEY_NAME, '...')
    query_url = f'https://api.github.com/{resource}'
    params = {"state": "open",}
    headers = {'Authorization': f'token {token}'}
    try:
        return requests.get(query_url, headers=headers, params=params)
    except BaseException as err:
        logger.error(f"Unexpected {err=}, {type(err)=}")
        return None
