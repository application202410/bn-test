import json

from src import downloader

# content of test_sample.py


example_jobs = [
    {
        "title": "Software Developer",
        "location": "London"
    },
    {
        "title": "Marketing Internship",
        "location": "York"
    },
]
example_members = [
    {
        "name": "Joe",
        "bio": "I'm a designer from London, UK"
    },
    {
        "name": "Marta",
        "bio": "Example Bio"
    },
]


def test_jobs_download():
    jobs = [downloader.Job.factory(x) for x in example_jobs]
    assert len(jobs) == 2
    assert jobs[0].title == 'Software Developer'
    assert jobs[1].location == 'York'


def test_member_download():
    members = [downloader.Member.factory(x) for x in example_members]
    assert len(members) == 2
    assert members[0].name == 'Joe'
    assert members[1].bio == 'Example Bio'
