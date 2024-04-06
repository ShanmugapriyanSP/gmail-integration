from itertools import chain
from typing import List

from config import Config
from data.sql_client import SqlClient
from enums.rule_action import RuleAction
from enums.rule_column import RuleColumn
from enums.rule_predicate import RulePredicate
from model.condition import Condition
from model.email import Email
from model.rule import Rule
from service.gmail_service import GmailService
from service.oauth_service import OAuthService
from utils.generic import GenericUtils


class EmailRuleProcessor:
    _config_vars: Config
    _gmail_service: GmailService
    _oauth_service: OAuthService
    _sql_client: SqlClient
    _rules: List[Rule]

    def __init__(self):
        self._config_vars = Config()
        self._oauth_service = OAuthService(self._config_vars)
        self._gmail_service = GmailService(self._oauth_service)
        self._sql_client = SqlClient(self._config_vars)

    def parse_rules(self):
        rules = GenericUtils.load_json(self._config_vars.rules_file)['rules']
        self._rules = [Rule(rule) for rule in rules]

    @staticmethod
    def get_column(field: str) -> str:
        return RuleColumn.from_str(field).column

    @staticmethod
    def get_sql_condition(predicate: str) -> str:
        return RulePredicate.from_str(predicate).sql_condition

    def prepare_query(self, predicate: str, conditions: List[Condition]) -> str:
        sql_query = (f"SELECT {RuleColumn.MESSAGE_ID.column}, {RuleColumn.LABEL.column} "
                     f"from {Config().db_table_name} WHERE ")
        condition_sql = []
        for cond in conditions:
            sql_operator = self.get_sql_condition(cond.predicate)
            match sql_operator:
                case RulePredicate.CONTAINS.sql_condition:
                    value = f"'%{cond.value}%'"
                case RulePredicate.GREATER_THAN.sql_condition | RulePredicate.LESS_THAN.sql_condition:
                    value = f"CURRENT_TIMESTAMP - INTERVAL '{cond.value}'"
                case _:
                    value = cond.value
            condition_sql.append(f"{self.get_column(cond.field)} {sql_operator} {value}")

        # Construct the conditions
        if predicate == RulePredicate.ALL.predicate:
            sql_query += f' {RulePredicate.ALL.sql_condition} '.join(condition_sql)
        elif predicate == RulePredicate.ANY.predicate:
            sql_query += f' {RulePredicate.ANY.sql_condition} '.join(condition_sql)
        else:
            raise NotImplementedError(f"Predicate {predicate} is not defined!!")

        return sql_query

    def _mark_message(self, action_value, emails: List[Email]):
        """

        :param action_value:
        :param emails:
        :return:
        """
        add_label_ids, remove_label_ids = [], []
        remove_label_ids.append("UNREAD") if action_value else add_label_ids.append("UNREAD")
        msg_ids = [email.message_id for email in emails]
        self._gmail_service.batch_modify(msg_ids, add_label_ids, remove_label_ids)

    def _move_message(self, action_value, emails: List[Email]) -> None:
        """

        :param action_value:
        :param emails:
        :return:
        """
        add_label_ids, remove_label_ids = [], []
        add_label_ids.append(action_value)
        msg_ids = []
        for email in emails:
            if email.label != action_value:
                remove_label_ids.append(email.label)
                msg_ids.append(email.message_id)
        self._gmail_service.batch_modify(msg_ids, add_label_ids, remove_label_ids)

    def apply_actions(self):
        for rule in self._rules:
            query = self.prepare_query(rule.predicate, rule.conditions)
            # Fetch emails based on conditions
            emails: List[Email] = self._sql_client.fetch_emails(query)
            # Apply actions to fetched emails
            for action, action_value in rule.actions.items():
                match action.lower():
                    case RuleAction.MARK_AS_READ.value:
                        self._mark_message(action_value, emails)
                    case RuleAction.MOVE_MESSAGE.value:
                        self._move_message(action_value, emails)

    def process(self):
        self.parse_rules()
        self.apply_actions()


if __name__ == '__main__':
    EmailRuleProcessor().process()
