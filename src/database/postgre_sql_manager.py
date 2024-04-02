import psycopg2

from model.email import Email


class PostgresManager:

    def __init__(self, host, port, database, user, password):
        self.connection = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id SERIAL PRIMARY KEY,
                sender TEXT NOT NULL,
                subject TEXT NOT NULL,
                received_date TEXT NOT NULL,
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
