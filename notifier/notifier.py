import json
import logging
import os
import time
from typing import Dict

import requests

logger = logging.getLogger("moodle_scraper")


class Notifier:
    def __init__(self):
        self.hook = os.getenv("SLACK_NOTIFIER_HOOK")

    def notify(self, msg: str) -> None:
        if "DEV_RUN" in os.environ:
            return
        wrapped_msg: str = f"moodle-scraper:\n{msg}"
        slack_data: Dict[str, str] = {"text": wrapped_msg}

        time.sleep(5)
        response = requests.post(
            url=self.hook,
            data=json.dumps(slack_data),
            headers={"Content-Type": "application/json"},
        )

        logger_msg = "Message sent to slack notifier webhook"
        if response.ok:
            logger.debug("%s successful", logger_msg)
        else:
            logger.debug("%s not successful", logger_msg)
