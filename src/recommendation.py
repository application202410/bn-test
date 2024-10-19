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


def factory_engine(name):
    if name == 'dummy':
        return DummyEngine()
    else:
        raise ValueError(f"{name} is not a supported engine")
