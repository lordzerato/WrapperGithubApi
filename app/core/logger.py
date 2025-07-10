import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

def setup_logging():
    """Configure the logging setup."""
    logging.basicConfig(level=settings.LOGGING_LEVEL)
