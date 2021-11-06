import os
from github import Github

from . import constants

def get_org(org_name):
    token = os.getenv(constants.API_KEY_NAME)
    ghub = Github(token)
    return ghub.get_organization(org_name)

def get_repos(org_name, org=None):
    if not org:
        org = get_org(org_name)
    return [repo for repo in org.get_repos()]
