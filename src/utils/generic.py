import json
import logging
import os
import re
from datetime import datetime

import yaml

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %z"


class GenericUtils:

    @staticmethod
    def get_logger(name):
        """
        Initialises  logger
        :param name:
        :return:
        """
        logging.basicConfig(
            level=os.getenv("LOG_LEVEL", "DEBUG")
        )
        return logging.getLogger(name)

    @staticmethod
    def load_yaml(config_file) -> dict:
        """
        Loads yaml file
        :param config_file:
        :return:
        """
        with open(config_file, 'r') as config:
            return yaml.safe_load(config)

    @staticmethod
    def load_json(json_file) -> dict:
        """
        Loads json file
        :param json_file:
        :return:
        """
        with open(json_file, 'r') as file:
            return json.load(file)

    @staticmethod
    def remove_extra_whitespaces(text) -> str:
        """
        Removes extra whitespaces and replaces newlines with '/n'
        :param text:
        :return:
        """
        # Remove extra whitespaces using a regular expression
        text = re.sub(r"\s+", " ", text)
        text = text.replace("\n", "/n")
        return text

    @staticmethod
    def remove_timezone_info(date_string):
        """
        Uses regex to remove timezone info
        :param date_string:
        :return:
        """
        # Define a regular expression pattern to match timezone info
        pattern = r'\s*\([A-Za-z]+\)\s*'
        # Use re.sub() to remove timezone info from the date string
        return re.sub(pattern, '', date_string)

    @staticmethod
    def format_date(date_str):
        """
        Parses the date and returns in a required format
        :param date_str:
        :return:
        """
        # Parse the date string into a datetime object
        date_str = GenericUtils.remove_timezone_info(date_str)
        date_formats = [
            '%d %b %Y %H:%M:%S %z',
            '%a, %d %b %Y %H:%M:%S %z',
        ]
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass

        return None
