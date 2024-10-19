import logging
import requests

log = logging.getLogger()

URL_JOBS = 'https://bn-hiring-challenge.fly.dev/jobs.json'
URL_MEMBERS = 'https://bn-hiring-challenge.fly.dev/members.json'


class Job:
    def __init__(self, title, location):
        self.title = title
        self.location = location

        # derived data, set by parsers etc.
        self.is_internship = False
        self.category = None

    @classmethod
    def factory(cls, json_obj):
        # TODO: I'm assuming this is a trusted internal API so we don't need
        # to be too defensive here. Really, we should at least catch and log
        # errors in the case of missing fields.
        return cls(title=json_obj['title'], location=json_obj['location'])


class Member:
    def __init__(self, name, bio):
        self.name = name
        self.bio = bio

    def requires_internship(self):
        return 'internship' in self.bio.lower()

    def bio_lc(self):
        return self.bio.lower()

    @classmethod
    def factory(cls, json_obj):
        # TODO: Same as in Job.
        return cls(name=json_obj['name'], bio=json_obj['bio'])


def do_download(url):
    resp = requests.get(url)
    # TODO: you should really write some simple validation to handle
    # connection timeouts, SSL errors, etc. Leaving that as a 'nice to have'
    return resp.json()


def download_jobs():
    log.debug("Downloading jobs")
    data = do_download(URL_JOBS)
    return [Job.factory(x) for x in data]


def download_members():
    log.debug("Downloading members")
    data = do_download(URL_MEMBERS)
    return [Member.factory(x) for x in data]
