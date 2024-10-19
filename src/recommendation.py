import logging
import json

log = logging.getLogger(__name__)

CATEGORY_JSON_FILE = "./data/category.json"


class DummyEngine:
    """The very simplest engine possible. This one just finds
    available jobs. I.e. every member will get every job. This
    is probably not much use but is the bare bones version of
    'find me a job'.
    """

    def go(self, members, jobs):
        log.debug("Running dummy recommendation engine")
        return {member: jobs for member in members}


class KeyWordMatcherEngine:
    """This is a very hand-cranked engine. It is very flexible,
    in that we can tweak and tune it as much as we like until we
    get the right results. But... that's going to be a lot of work!"""

    def __init__(self):
        with open(CATEGORY_JSON_FILE, 'r') as f:
            self.CATEGORY_MAP = json.load(f)

    def go(self, members, jobs):
        log.debug("Running key word recommendation engine")
        self.process_jobs(jobs)
        recommendations = {}
        for member in members:
            recommendations[member] = self.filter_jobs_for_member(member, jobs)
        return recommendations

    def process_jobs(self, jobs):
        """"
        This does some up-front categorisation of jobs, really just so we don't 
        need to repeat it every single iteration of the loop. Ideally, this data
        would be extracted as part of the API we used.
        """
        # Job level - map internships separately from contract jobs
        # TODO: you'd probaby split out part-time, fixed-term, etc here too!
        for job in jobs:
            # no messing about with case-sensitive matching
            title_lc = job.title.lower()
            if 'internship' in title_lc:
                job.is_internship = True

            mapped_category = self.map_category(title_lc)
            if mapped_category:
                job.category = mapped_category

    def map_category(self, title_lc):
        """
        Spot job category keywords in the text and map to a general category
        """
        for keyword, category in self.CATEGORY_MAP.items():
            if keyword in title_lc:
                return category
        return None

    def extract_locations(self, member, locations):
        """
        Get any locations a user has mentioned in their bio
        """
        return [x for x in locations if x in member.bio_lc()]

    def filter_internship(self, member, intership_only, job):
        """
        If a user mentions internships, we restrict their results
        to just internships. 
        """
        if intership_only and not job.is_internship:
            log.debug(f"{member.name} specifies internship. {
                job.title} is not one")
            return False
        return True

    def filter_category(self, member, job):
        """
        If we can get a category from the member bio, we only return jobs in the
        same category.
        """
        member_category = self.map_category(member.bio_lc())
        if member_category and not member_category == job.category:
            log.debug(f"{member.name} wants {member_category}. {
                job.title} is {job.category}")
            return False
        return True

    def filter_location(self, available_locations, member, job):
        """
        Any location the user has mentioned will be used to filter jobs to those
        locations. 
        """
        # TODO: This would clearly benefit from some mapping. E.g. if a user says "Scotland"
        # we should clearly show them jobs in Edinburgh
        member_locations = self.extract_locations(member, available_locations)
        if member_locations and job.location.lower() not in member_locations:
            log.debug(f"{member.name} locations are {member_locations}. {
                job.title} is in {job.location}")
            return False
        return True

    def filter_jobs_for_member(self, member, jobs):
        """
        Try every job against this user.
        """
        intership_only = member.requires_internship()
        available_locations = set([job.location.lower() for job in jobs])

        return [job for job in jobs if all([
            self.filter_internship(member, intership_only, job),
            self.filter_category(member, job),
            self.filter_location(available_locations, member, job)
        ])]


def factory_engine(name):
    if name == 'dummy':
        return DummyEngine()
    elif name == 'keyword':
        return KeyWordMatcherEngine()
    else:
        raise ValueError(f"{name} is not a supported engine")
