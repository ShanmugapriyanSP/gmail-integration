import os
from pathlib import Path
from typing import List

from utils.generic import GenericUtils

CONFIG_FILE = str(Path(__file__).parent / "../conf/config.yml")


class Config:
    _instance = None
    _search_label: str
    _max_email_count: int
    _credential_file: str
    _token_file: str
    _scopes: List[str]
    _redirect_port: int
    _db_name: str
    _db_host: str
    _db_port: str
    _db_user: str
    _db_password: str

    # Singleton class
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            config = GenericUtils.load_yaml(CONFIG_FILE)
            # Generic
            cls._instance._search_label = config["search_label"]
            cls._instance._max_email_count = config["max_email_count"]

            # Get the parent directory of the config file
            config_parent_dir = Path(CONFIG_FILE).parent
            # Google specific properties
            cls._instance._credential_file = (config_parent_dir / ".." / config['google']['credential_file']).resolve()
            cls._instance._token_file = (config_parent_dir / ".." / config['google']['token_file']).resolve()
            cls._instance._scopes = config["google"]["scopes"]
            cls._instance._redirect_port = config["google"]["redirect_port"]

            # Database properties
            cls._instance._db_name = config["database"]["name"]
            cls._instance._db_host = config["database"]["host"]
            cls._instance._db_port = config["database"]["port"]
            cls._instance._db_user = config["database"]["user"]
            cls._instance._db_password = os.getenv("POSTGRESQL_DB_PASSWORD")
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
    def redirect_port(self):
        return self._redirect_port

    @property
    def db_name(self):
        return self._db_name

    @property
    def db_host(self):
        return self._db_host

    @property
    def db_port(self):
        return self._db_port

    @property
    def db_user(self):
        return self._db_user

    @property
    def db_password(self):
        return self._db_password
