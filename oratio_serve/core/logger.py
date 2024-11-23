import logging
from oratio_serve.core.config import settings

def setup_logging():
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger("oratio_serve")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    return logger