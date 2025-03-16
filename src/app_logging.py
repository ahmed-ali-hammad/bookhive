import logging
import sys


class LoggingConfig:
    _logger = None

    @classmethod
    def get_logger(cls, logger_name: str) -> logging.Logger:
        """
        Get a logger with the specified name. If the logger is not already configured,
        it sets up logging.

        Args:
            logger_name (str): The name of the logger".

        Returns:
            logging.Logger: The configured logger instance.
        """
        if cls._logger is None:
            # Adding "BookHive" prefix to the logger name
            name = "BookHive" + "." + logger_name

            cls._logger = logging.getLogger(name)
            cls._logger.setLevel(logging.DEBUG)

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                "%(levelname)s:     %(asctime)s - %(name)s - %(message)s"
            )

            console_handler.setFormatter(formatter)

            cls._logger.addHandler(console_handler)
            cls._logger.propagate = False

        return cls._logger
