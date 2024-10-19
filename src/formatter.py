import logging

log = logging.getLogger(__name__)


def print_output(recommendation_map):
    log.debug("Printing output")

    log.info("Job recommendations are as follows:")
    for member, jobs in recommendation_map.items():
        log.info(f"NAME: {member.name} ({member.bio})")
        log.info("RECOMMENDED JOBS:")
        if jobs:
            for job in sorted(jobs, key=lambda x: x.title):
                log.info(f"- {job.title} ({job.location})")
        else:
            log.info("<None>")
