import logging

VLOGGER = logging.getLogger("evaluation")
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s :: %(levelname)-8s :: %(message)s",
)

LOGGER = logging.getLogger("evogfuzz")
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s :: %(levelname)-8s :: %(message)s",
)
