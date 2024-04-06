from logging import Logger
from typing import List

from config import Config
from data.sql_client import SqlClient
from enums.rule_action import RuleAction
from enums.rule_column import RuleColumn
from enums.rule_predicate import RulePredicate
from objects.condition import Condition
from objects.email import Email
from objects.rule import Rule
from service.gmail_service import GmailService
from service.oauth_service import OAuthService
from utils.generic import GenericUtils


class EmailRuleProcessor:
    _config_vars: Config
    _gmail_service: GmailService
    _oauth_service: OAuthService
    _sql_client: SqlClient
    _rules: List[Rule]
    _logger: Logger

    def __init__(self, gmail_service: GmailService, sql_client: SqlClient):
        self._config_vars = Config()
        self._gmail_service = gmail_service
        self._sql_client = sql_client
        self._logger = GenericUtils.get_logger(self.__class__.__name__)

    def parse_rules(self):
        rules = GenericUtils.load_json(self._config_vars.rules_file)['rules']
        self._rules = [Rule(rule) for rule in rules]

    @staticmethod
    def get_column(field: str) -> str:
        return RuleColumn.from_str(field).column

    @staticmethod
    def get_sql_condition(predicate: str) -> str:
        return RulePredicate.from_str(predicate).sql_condition

    @staticmethod
    def prepare_query(predicate: str, conditions: List[Condition]) -> str:
        """
        Constructs the SQL query based on the provided predicate and conditions
        :param predicate:
        :param conditions:
        :return:
        """
        sql_query = (f"SELECT {RuleColumn.MESSAGE_ID.column}, {RuleColumn.LABEL.column} "
                     f"FROM {Config().db_table_name} WHERE ")
        condition_sql = []
        for cond in conditions:
            sql_operator = EmailRuleProcessor.get_sql_condition(cond.predicate)
            match sql_operator:

                case RulePredicate.CONTAINS.sql_condition | RulePredicate.DOES_NOT_CONTAINS.sql_condition:
                    value = f"'%{cond.value}%'"
                    column = EmailRuleProcessor.get_column(cond.field)

                case RulePredicate.GREATER_THAN.sql_condition | RulePredicate.LESS_THAN.sql_condition:
                    value = f"INTERVAL '{cond.value}'"
                    column = f"AGE(CURRENT_TIMESTAMP, {EmailRuleProcessor.get_column(cond.field)})"

                case _:
                    value = f"'{cond.value}'"
                    column = EmailRuleProcessor.get_column(cond.field)

            condition_sql.append(f"{column} {sql_operator} {value}")

        # Construct the conditions
        if predicate.lower() == RulePredicate.ALL.predicate:
            sql_query += f' {RulePredicate.ALL.sql_condition} '.join(condition_sql)
        elif predicate.lower() == RulePredicate.ANY.predicate:
            sql_query += f' {RulePredicate.ANY.sql_condition} '.join(condition_sql)
        else:
            raise NotImplementedError(f"Predicate {predicate.lower()} is not defined!!")

        return sql_query

    def _mark_message(self, action_value, emails: List[Email]):
        """
        Mark the message as read or unread
        :param action_value:
        :param emails:
        :return:
        """
        add_label_ids, remove_label_ids = set(), set()
        remove_label_ids.add("UNREAD") if action_value else add_label_ids.add("UNREAD")
        msg_ids = [email.message_id for email in emails]
        self._logger.info(f"Marking emails as {'Read' if action_value else 'Unread'}")
        self._gmail_service.update_labels(
            message_ids=msg_ids,
            add_label_ids=list(add_label_ids),
            remove_label_ids=list(remove_label_ids)
        )

    def _move_message(self, action_value, emails: List[Email]) -> None:
        """
        Move message from one folder to another
        :param action_value:
        :param emails:
        :return:
        """
        add_label_ids, remove_label_ids = set(), set()
        add_label_ids.add(action_value)
        msg_ids = []

        for email in emails:
            if email.label != action_value:
                remove_label_ids.add(email.label)
                msg_ids.append(email.message_id)
        self._logger.info(f"Moving Emails to {action_value} folder")
        self._gmail_service.update_labels(
            message_ids=msg_ids,
            add_label_ids=list(add_label_ids),
            remove_label_ids=list(remove_label_ids)
        )

    def apply_actions(self):
        """
        * Parse through each rule and fetch the list of matching emails
        * Apply the action for the matching emails based on the rule
        :return:
        """
        for rule in self._rules:
            self._logger.info(f"Processing Rule: {rule.description}")
            query = self.prepare_query(rule.predicate, rule.conditions)
            # Fetch emails based on conditions
            emails: List[Email] = self._sql_client.fetch_emails(query)
            # Apply actions to fetched emails
            self._logger.info(f"{len(emails)} emails fetched for rule: {rule.description}")
            for action, action_value in rule.actions.items():
                match action.lower():

                    case RuleAction.MARK_AS_READ.value:
                        self._mark_message(action_value, emails)

                    case RuleAction.MOVE_MESSAGE.value:
                        self._move_message(action_value, emails)

    def process(self):
        """
        * Parse the rules
        * Apply action based on the rules
        :return:
        """
        self.parse_rules()
        self.apply_actions()


if __name__ == '__main__':
    EmailRuleProcessor(
        gmail_service=GmailService(OAuthService()),
        sql_client=SqlClient()
    ).process()
