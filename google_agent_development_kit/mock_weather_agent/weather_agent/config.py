"""Configuration for the weather agent to suppress warnings."""

import logging
import warnings

def configure_logging():
    """Configure logging to suppress ADK warnings."""
    # Suppress warnings using the warnings module
    warnings.filterwarnings("ignore", message=".*there are non-text parts in the response.*")
    
    # Configure logging to suppress warnings
    logging.getLogger("google.adk").setLevel(logging.ERROR)
    logging.getLogger("google.genai").setLevel(logging.ERROR)
    
    # Redirect warnings to logging
    logging.captureWarnings(True)
    warnings_logger = logging.getLogger("py.warnings")
    warnings_logger.setLevel(logging.ERROR)