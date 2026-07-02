"""
Purpose: Configuration module for the Fraud Investigation Agent.
Handles loading environment variables, validating presence of API keys, and setting model constants.
"""

import os
import logging
from typing import Final
from dotenv import load_dotenv

# Initialize logging configuration safely across modules
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("backend.config")

# Load environment variables from .env file if it exists
load_dotenv()

# Configuration and Constants
OPENAI_API_KEY: Final[str] = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: Final[str] = os.getenv("OPENAI_MODEL", "gpt-4o")
MAX_RETRIES: Final[int] = int(os.getenv("MAX_RETRIES", "3"))
APP_LOGIN_PASSWORD: Final[str] = os.getenv("APP_LOGIN_PASSWORD", "pwd")

def validate_config() -> bool:
    """
    Validates that essential configurations are present.
    
    Returns:
        bool: True if configuration is valid, False otherwise.
    """
    if not OPENAI_API_KEY:
        logger.error("Missing critical configuration: OPENAI_API_KEY environment variable is empty.")
        return False
    logger.info(u"Configuration validation successful. Model set to: %s", OPENAI_MODEL)
    return True
