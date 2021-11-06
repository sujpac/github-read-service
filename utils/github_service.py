import os, requests
from github import Github

from . import constants

def get_org(org_name):
    """Gets org from Github"""
    token = os.getenv(constants.API_KEY_NAME, '...')
    ghub = Github(token)
    return ghub.get_organization(org_name)

def get_repos(org_name, org=None):
    """Gets all repos of a given org from Github"""
    if not org:
        org = get_org(org_name)
    return [repo for repo in org.get_repos()]

def send_get_request(resource):
    """Send a GET request to the Github API"""
    token = os.getenv(constants.API_KEY_NAME, '...')
    query_url = f'https://api.github.com/{resource}'
    params = {"state": "open",}
    headers = {'Authorization': f'token {token}'}
    return requests.get(query_url, headers=headers, params=params)
