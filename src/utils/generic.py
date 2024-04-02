import re

import yaml


class GenericUtils:

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
    def remove_extra_whitespaces(text) -> str:
        """
        Removes extra whitespaces and replaces newlines with '/n'
        :param text:
        :return:
        """
        # Remove extra whitespaces using a regular expression
        text = re.sub(r"\s+", " ", text)
        # Replace newlines with '/n'
        text = text.replace("\n", "/n")
        return text
