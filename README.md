# github-read-service
This is a service that provides custom API's to read organizational data from Github. It is implemented with Python, Django, and Django Rest Framework. The service uses Redis as an in-memory cache to facilitate better performance, as well as to be able to scale the app without risk of crossing API rate limits. The organization used by default is [parse-community](https://github.com/parse-community) - this can be changed by modifying DEFAULT_ORG in utils/constants.py.


## API Documentation
We use parse-community as the Github org:
```
/orgs/parse-community
/orgs/parse-community/members
/orgs/parse-community/repos
```

The following custom views for organization repositories are provided by the app and are cached periodically:
```
/view/top/N/forks (Top-N repos by number of forks)
/view/top/N/last_updated (Top-N repos by last updated time)
/view/top/N/open_issues (Top-N repos by open issues)
/view/top/N/stars (Top-N repos by stars)
/view/top/N/watchers (Top-N repos by watchers)
```

All other API endpoints are proxied through the service to Github. E.g.:
[/zen](http://127.0.0.1:8000/{resource}/) outputs the response from a GET /zen request to the [Github API](https://api.github.com/zen)
```
/zen
/gists
/users/octocat/
/repos/facebook/react/issues
[etc.]
```

Lastly, also provided is a healthcheck endpoint that returns an HTTP 200 when the service is ready to serve responses:
```
/healthcheck
```


## Setup
The following instructions are written for MacOS/Linux machines with the latest version of [Python 3](https://www.python.org/downloads/) installed:

1. Clone repository
```
cd ~
git clone https://github.com/sujpac/github-read-service.git
cd github-read-service/
```

2. Create new virtual environment, install pip dependencies, make migrations
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

3. Generate a new [GitHub token](https://github.com/settings/tokens) and save the raw value to an environment variable through your shell's configuration file
```
export GITHUB_TOKEN=[insert_your_github_token]
echo "export GITHUB_TOKEN=${GITHUB_TOKEN}" >> ~/.zshrc
```

4. Install Redis and start up Redis Server
```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
sudo make install
redis-server
```

5. Run the Django app (in a different terminal window)
```
cd ~/github-read-service/
source env/bin/activate
python manage.py runserver
```

6. Test the service on by testing API endpoints through your browser, e.g., go [to this URL](http://127.0.0.1:8000/view/top/10/forks/) to get the top 10 repos by forks. Test how the service responds to cache failures by ending the ```redis-server``` process or running ```redis-cli``` and testing out commands such as ```flushall``` which deletes all keys. Simulate Github outage by testing the service with no server-side Internet connection with or without cached data. Try proxying an invalid resource to the GitHub API.

7. To test multiple instances locally on different ports, run the Django app again passing in a new port number (on a different terminal window)
```
cd ~/github-read-service/
source env/bin/activate
python manage.py runserver 8001
```
