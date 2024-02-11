import logging
import sys


def get_logger(CaptchaName: str = "Flask-Session-Captcha") -> logging.Logger:
    """ This function return a stdout Logger
    args:
        . LoggerName:string: name of the logger
    """
    logLevel = logging.INFO
    logformat = logging.Formatter(f"[{CaptchaName}" + "- %(levelname)s] [%(asctime)s] - %(message)s")
    logger = logging.getLogger(CaptchaName)
    logger.setLevel(logLevel)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logLevel)
    handler.setFormatter(logformat)
    logger.addHandler(handler)
    return logger
