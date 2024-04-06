
class MockData:

    @staticmethod
    def get_config():
        return {
            "max_email_count": 100,
            "rules_file": "/path/to/rules.yml",
            "google": {
                "credential_file": "/path/to/credential.json",
                "token_file": "/path/to/token.json",
                "scopes": ["scope1", "scope2"],
                "redirect_port": 8080
            },
            "database": {
                "db_name": "test_db",
                "table_name": "emails",
                "host": "localhost",
                "port": "5432",
                "user": "test_user"
            }
        }