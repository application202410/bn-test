import logging

import downloader
import recommendation
import formatter

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG,
                    datefmt=DATE_FORMAT)
log = logging.getLogger()


def run():
    log.info("Recommendation Application Startup")

    jobs = downloader.download_jobs()
    members = downloader.download_members()
    engine = recommendation.factory_engine('keyword')
    recommendation_map = engine.go(members, jobs)
    formatter.print_output(recommendation_map)

    log.info("Recommendation Application Exit")


if __name__ == '__main__':
    run()
