import logging

"""
Debug = 10: This level gives detailed information, useful only when a problem is being diagnosed.
Info = 20: This is used to confirm that everything is working as it should.
Warning = 30: This level indicates that something unexpected has happened or some problem is about to happen in the near future.
Error = 40: As it implies, an error has occurred. The software was unable to perform some function.
Critical = 50: A serious error has occurred. The program itself may shut down or not be able to continue running properly.
"""


def add_logging_level(level_name, level_num, method_name=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `level_name` becomes an attribute of the `logging` module with the value
    `level_num`. `method_name` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `method_name` is not specified, `level_name.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> add_logging_level('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not method_name:
        method_name = level_name.lower()

    if hasattr(logging, level_name):
       raise AttributeError(f"{level_name} already defined in logging module")
    if hasattr(logging, method_name):
       raise AttributeError(f"{method_name} already defined in logging module")
    if hasattr(logging.getLoggerClass(), method_name):
       raise AttributeError(f"{method_name} already defined in logger class")

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(level_num):
            self._log(level_num, message, args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(level_num, message, *args, **kwargs)

    logging.addLevelName(level_num, level_name)
    setattr(logging, level_name, level_num)
    setattr(logging.getLoggerClass(), method_name, logForLevel)
    setattr(logging, method_name, logToRoot)


add_logging_level("INTERNAL", logging.DEBUG - 5)


class ColorFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    purple = "\x1b[35;20m"
    blue = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    orange = "\x1b[34;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"

    bold = "\033[1m"
    reset = "\x1b[0m"
    fmt = "{0}[%(asctime)s] {1}%(levelname)s{2} {3}%(funcName)s (%(filename)s:%(lineno)d): %(message)s{4}"
    fmt_internal = "{0}[%(asctime)s] (%(filename)s): %(message)s{1}"

    FORMATS = {
        logging.INTERNAL: fmt.format(green, bold, reset, green, reset),
        logging.DEBUG: fmt.format(grey, bold, reset, grey, reset),
        logging.INFO: fmt.format(grey, bold, reset, grey, reset),
        logging.WARNING: fmt.format(yellow, bold, reset, yellow, reset),
        logging.ERROR: fmt.format(red, bold, reset, red, reset),
        logging.CRITICAL: fmt.format(bold_red, bold, reset, bold_red, reset)
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(fmt=log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


class ColorFormatterInverted(logging.Formatter):

    grey = "\x1b[30;47m"
    green = "\x1b[30;42m"
    purple = "\x1b[45m"
    blue = "\x1b[46m"
    yellow = "\x1b[30;43m"
    orange = "\x1b[44m"
    red = "\x1b[41m"
    bold_red = "\x1b[41;1m"

    bold = "\033[1m"
    reset = "\x1b[0m"
    fmt = "{0}[%(asctime)s] {1}%(levelname)s{2} {3}%(funcName)s (%(filename)s:%(lineno)d): %(message)s{4}"
    fmt_internal = "{0}[%(asctime)s] (%(filename)s): %(message)s{1}"

    FORMATS = {
        logging.INTERNAL: fmt.format(green, bold, reset, green, reset),
        logging.DEBUG: fmt.format(grey, bold, reset, grey, reset),
        logging.INFO: fmt.format(grey, bold, reset, grey, reset),
        logging.WARNING: fmt.format(yellow, bold, reset, yellow, reset),
        logging.ERROR: fmt.format(red, bold, reset, red, reset),
        logging.CRITICAL: fmt.format(bold_red, bold, reset, bold_red, reset)
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(fmt=log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


BASE_LOGGING_LEVEL = logging.INTERNAL
STREAM_LOGGING_LEVEL = logging.INTERNAL
FILE_LOGGING_LEVEL = logging.INFO

PATH_NAME = "%(pathname)s"
FILE_NAME = "%(filename)s"

def init_logger(log_to_console: bool=True, log_to_file: bool=True, invert_colors: bool=False,
                base_logging_level: int=BASE_LOGGING_LEVEL, stream_logging_level: int=STREAM_LOGGING_LEVEL,
                file_logging_level: int=FILE_LOGGING_LEVEL, rewrite_log_file: bool=True,
                display_init_message: bool=True):
    global logger

    logger = logging.getLogger(__name__)
    logger.setLevel(base_logging_level)

    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])

    if log_to_console:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(stream_logging_level)
        if invert_colors:
            stream_handler.setFormatter(ColorFormatterInverted())
        else:
            stream_handler.setFormatter(ColorFormatter())

        logger.addHandler(stream_handler)

    if log_to_file:
        file_mode = "w" if rewrite_log_file else "a"
        file_handler = logging.FileHandler(filename=f"{__package__}.log", mode=file_mode)
        file_handler.setLevel(file_logging_level)

        file_formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)s %(funcName)s (%(filename)s:%(lineno)d): %(message)s\nFile \"%(pathname)s:%(lineno)d\"\n",
            datefmt="%Y-%m-%d %H:%M:%S",)
        file_handler.setFormatter(file_formatter)

        logger.addHandler(file_handler)

    if display_init_message:
        logger.internal("Initialized Logger!")

init_logger(log_to_file=False, display_init_message=False)