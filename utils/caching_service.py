from redis import Redis, ConnectionError
from django.core.cache import cache
from urllib.parse import urlparse
import logging, pickle

from . import github_service, constants

def _setup():
    """Sets up Redis instance and logger"""
    global redis, logger
    redis_url = urlparse(cache._server)
    redis = Redis(host=redis_url.hostname, port=redis_url.port)
    logging.basicConfig()
    logger = logging.getLogger('redis-log')

redis = logger = None
_setup()

def get_redis_instance():
    """Returns Redis instance"""
    return redis

def is_redis_running():
    """Chhecks if Redis Server is running"""
    try:
        redis.ping()
    except ConnectionError:
        logger.error("Redis isn't running. Try running 'redis-server'")
        return False
    else:
        return True

def retrieve_org(org_name):
    """Gets org from cache, or, gets org from Github and sets entry in cache"""
    key = constants.ORG_PREFIX + org_name
    pickled_org = redis.get(key)

    if pickled_org is None:
        org = github_service.get_org(org_name)
        pickled_org = pickle.dumps(org)
        redis.set(key, pickled_org, ex=constants.CACHE_TTL)
    else:
        org = pickle.loads(pickled_org)
    
    return org

def retrieve_repos(org_name):
    """Gets repos from cache, or, gets repos from Github and sets entry in cache"""
    key = constants.REPOS_PREFIX + org_name
    pickled_repos = redis.get(key)

    if pickled_repos is None:
        org = retrieve_org(org_name)
        repos = github_service.get_repos(org_name, org)
        pickled_repos = pickle.dumps(repos)
        redis.set(key, pickled_repos, constants.CACHE_TTL)
    else:
        repos = pickle.loads(pickled_repos)
    
    return repos
