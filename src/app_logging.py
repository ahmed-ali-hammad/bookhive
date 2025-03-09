import logging
import sys


class LoggingConfig:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def _configure_logging(self):
        """Configure logging for the application."""

        logger = logging.getLogger("my_app")
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        logger.propagate = False

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger with the specified name.

        Args:
            name (str): The name of the logger.

        Returns:
            logging.Logger: The configured logger instance.
        """
        return logging.getLogger(name)
