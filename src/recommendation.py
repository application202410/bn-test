import logging

log = logging.getLogger(__name__)


class DummyEngine:
    def go(self, members, jobs):
        log.debug("Running dummy recommendation engine")
        return {}


def factory_engine(name):
    if name == 'dummy':
        return DummyEngine()
    else:
        raise ValueError(f"{name} is not a supported engine")
