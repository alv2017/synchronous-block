import logging
from datetime import datetime
from api.config import ROOT_DIRECTORY
from uvicorn.logging import ColourizedFormatter


ts = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
LOG_FILE_LOCATION = ROOT_DIRECTORY / "logs" / f"performance_{ts}.log"
LOG_LEVEL = logging.INFO

_logger = logging.getLogger("performance_logger")
_logger.setLevel(LOG_LEVEL)

# Console Handler
console_handler = logging.StreamHandler()
console_formatter = ColourizedFormatter(
    "%(levelprefix)s PERFORMANCE -> %(message)s",
    use_colors=True
)
console_handler.setFormatter(console_formatter)

# File Handler
file_handler = logging.FileHandler(LOG_FILE_LOCATION, mode="a")
file_formatter = logging.Formatter(
    "%(asctime)s, %(levelname)s, %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)

_logger.addHandler(console_handler)
_logger.addHandler(file_handler)