import logging
import os

def setup_logger(name, log_file=None, level=logging.INFO):
    """
    Setup logger with console and optional file handlers.
    Falls back to console-only if file logging is unavailable (e.g., Render).
    """
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent adding duplicate handlers
    if not logger.handlers:
        # Console handler (always active)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler — optional, skip gracefully if filesystem is read-only
        if log_file:
            try:
                log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
                os.makedirs(log_dir, exist_ok=True)
                file_path = os.path.join(log_dir, log_file)
                file_handler = logging.FileHandler(file_path)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception:
                pass  # Silent fallback to console-only in cloud environments

    return logger
