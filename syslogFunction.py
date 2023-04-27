import logging
from logging.handlers import SysLogHandler
import json


def sent_syslog(content):
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        syslog_handlr = SysLogHandler(address=(config["Host"], config["Port"]))
        # we just need to change the
        logger = logging.getLogger()
        logger.addHandler(syslog_handlr)
        logger.setLevel(logging.INFO)
        # Send the log file contents to syslog
        logger.info(content)
        return {
            "error": False
        }
    except Exception as e:
        return {
            "error": True,
            "msg": f"Error sending syslog: {e}"
        }
