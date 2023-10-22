import logging
import os
import sys

from loguru import logger

from inscricoes.settings import LOG_LEVEL


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


# LOG_LEVELs
# 0: INFO
# 1: DEBUG
# 2: DEBUG with TRACE
# 3: TRACE with all TRACES

# Start logger
if LOG_LEVEL == "3":
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    logger.warning("logger level set to DEBUG with full TRACING")

elif LOG_LEVEL == "2":
    logger.info("logger level set to DEBUG with TRACE")

elif LOG_LEVEL == "1":
    logger.remove()
    logger.info("logger level set to DEBUG")
    logger.add(
        sys.stdout,
        colorize=True,
        level="DEBUG",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        backtrace=True,
        diagnose=False,
    )

else:
    logger.remove()
    logger.info("logger level set to INFO")
    logger.add(
        sys.stdout,
        colorize=True,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        backtrace=True,
        diagnose=False,
    )
