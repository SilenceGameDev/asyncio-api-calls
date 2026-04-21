import logging

from rich.logging import RichHandler

logger = logging.getLogger(__name__)

# the handler determines where the log go: stdout/file
shell_handler = RichHandler() # shows logs in shell
# file_handler = logging.FileHandler("debug.log") # show logs in a separate file # removing file handler since it clashed with vercel

# used to configure the level to send out
logger.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.DEBUG)
# file_handler.setLevel(logging.INFO)
# note if logger.setLevel is set to a higher level than the handler, that handler will not be able to access any log lower than that level. Ex: if logger is set to CRITICAL then handler is set to Warning the handler will NOT see any logs below CRITICAL.

# the formatter determines what our logs will look like
fmt_shell = "%(message)s"
fmt_file = "%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"

shell_formatter = logging.Formatter(fmt_shell)
file_formatter = logging.Formatter(fmt_file)

# here we hook everything together
shell_handler.setFormatter(shell_formatter)
# file_handler.setFormatter(file_formatter)

logger.addHandler(shell_handler)
# logger.addHandler(file_handler)

# Example statements to include in other files to log
# logger.debug('this is a debug statement')
# logger.info('this is a info statement')
# logger.warning('this is a warning statement')
# logger.critical('this is a critical statement')
# logger.error('this is a error statement')