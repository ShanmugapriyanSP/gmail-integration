from pathlib import Path
from typing import List

from utils.generic import GenericUtils

CONFIG_FILE = str(Path(__file__).parent / "../conf/config.yml")


class Config:
    _instance = None
    _credential_file: str = None
    _token_file: str
    _scopes: List[str]
    _redirect_port_number: int
    _search_label: str
    _max_email_count: int

    # Singleton class
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            config = GenericUtils.load_yaml(CONFIG_FILE)
            # Get the parent directory of the config file
            config_parent_dir = Path(CONFIG_FILE).parent
            # Store absolute path for files
            cls._instance._credential_file = (config_parent_dir / ".." / config['google']['credential_file']).resolve()
            cls._instance._token_file = (config_parent_dir / ".." / config['google']['token_file']).resolve()
            cls._instance._scopes = config["google"]["scopes"]
            cls._instance._redirect_port_number = config["google"]["redirect_port_number"]
            cls._instance._search_label = config["search_label"]
            cls._instance._max_email_count = config["max_email_count"]
        return cls._instance

    @property
    def search_label(self):
        return self._search_label

    @property
    def max_email_count(self):
        return self._max_email_count

    @property
    def credential_file(self):
        return self._credential_file

    @property
    def token_file(self):
        return self._token_file

    @property
    def scopes(self):
        return self._scopes

    @property
    def redirect_port_number(self):
        return self._redirect_port_number
