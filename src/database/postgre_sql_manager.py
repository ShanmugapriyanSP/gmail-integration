import psycopg2

from config import Config
from enums.rule_column import RuleColumn
from model.email import Email


class PostgreSqlManager:
    _table_name: str

    def __init__(self, config_vars: Config):
        self._table_name = config_vars.db_table_name
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
        """

        :return:
        """
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self._table_name} (
                {RuleColumn.ID.column()} SERIAL PRIMARY KEY,
                {RuleColumn.MESSAGE_ID.column()} TEXT NOT NULL,
                {RuleColumn.FROM.column()} TEXT NOT NULL, 
                {RuleColumn.TO.column()} TEXT NOT NULL, 
                {RuleColumn.SUBJECT.column()} TEXT NOT NULL, 
                {RuleColumn.RECEIVED_DATE.column()} TIMESTAMP NOT NULL,
                {RuleColumn.MESSAGE.column()} TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def insert_emails(self, emails: list[Email]):
        """

        :param emails:
        :return:
        """
        email_data = [(email.message_id, email.sender, email.to, email.subject, email.received_date, email.message_body)
                      for email in emails]
        self.cursor.executemany(f"""
            INSERT INTO {self._table_name} (
                {RuleColumn.MESSAGE_ID.column()},
                {RuleColumn.FROM.column()},
                {RuleColumn.TO.column()}, 
                {RuleColumn.SUBJECT.column()},
                {RuleColumn.RECEIVED_DATE.column()},
                {RuleColumn.MESSAGE.column()}
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """, email_data)
        self.connection.commit()

    def fetch_emails(self, query: str):
        """

        :param query:
        :return:
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        """

        :return:
        """
        self.cursor.close()
        self.connection.close()
