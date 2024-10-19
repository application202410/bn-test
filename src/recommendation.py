import logging

log = logging.getLogger(__name__)


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

    CATEGORY_MAP = {
        "software developer": "Tech",
        "marketing": "Marketing",
        "data scientist": "Tech",
        "legal": "Law",
        "project manager": "Project",
        "sales": "Sales",
        "ux design": "Design",
        "design": "Design"
    }

    def go(self, members, jobs):
        log.debug("Running key word recommendation engine")
        self.process_jobs(jobs)
        recommendations = {}
        for member in members:
            recommendations[member] = self.filter_jobs_for_member(member, jobs)
        return recommendations

    def process_jobs(self, jobs):
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
        for keyword, category in self.CATEGORY_MAP.items():
            if keyword in title_lc:
                return category
        return None

    def filter_jobs_for_member(self, member, jobs):
        bio_lc = member.bio.lower()
        intership_only = ('internship' in bio_lc)

        filtered_jobs = []
        for job in jobs:
            if intership_only and not job.is_internship:
                log.debug(f"{member.name} specifies internship. {
                          job.title} is not one")
                continue

            member_category = self.map_category(bio_lc)
            if member_category and not member_category == job.category:
                log.debug(f"{member.name} wants {member_category}. {
                          job.title} is {job.category}")
                continue

            filtered_jobs.append(job)
        return filtered_jobs


def factory_engine(name):
    if name == 'dummy':
        return DummyEngine()
    elif name == 'keyword':
        return KeyWordMatcherEngine()
    else:
        raise ValueError(f"{name} is not a supported engine")
