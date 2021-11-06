import os
from github import Github

from . import constants

def get_org(org_name):
    """Gets org from Github"""
    token = os.getenv(constants.API_KEY_NAME)
    ghub = Github(token)
    return ghub.get_organization(org_name)

def get_repos(org_name, org=None):
    """Gets all repos of a given org from Github"""
    if not org:
        org = get_org(org_name)
    return [repo for repo in org.get_repos()]
