import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(level=settings.LOGGING_LEVEL)
