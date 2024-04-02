import psycopg2

from config import Config
from model.email import Email


class PostgreSqlManager:

    def __init__(self, config_vars: Config):
        self.connection = psycopg2.connect(
            host=config_vars.db_host,
            port=config_vars.db_port,
            database=config_vars.db_name,
            user=config_vars.db_user,
            password=config_vars.db_password
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id SERIAL PRIMARY KEY,
                sender TEXT NOT NULL,
                subject TEXT NOT NULL,
                received_date TIMESTAMP NOT NULL,
                message_body TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def insert_emails(self, emails: list[Email]):
        email_data = [(email.sender, email.subject, email.received_date, email.message_body) for email in emails]
        self.cursor.executemany(
            "INSERT INTO emails (sender, subject, received_date, message_body) VALUES (%s, %s, %s, %s)", email_data
        )
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
