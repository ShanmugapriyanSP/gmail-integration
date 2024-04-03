from typing import List

from config import Config
from database.postgre_sql_manager import PostgreSqlManager
from enums.rule_action import RuleAction
from enums.rule_column import RuleColumn
from enums.rule_predicate import RulePredicate
from model.condition import Condition
from model.rule import Rule
from service.gmail_service import GmailService
from service.oauth_service import OAuthService
from utils.generic import GenericUtils


class EmailRuleProcessor:
    _config_vars: Config
    _gmail_service: GmailService
    _oauth_service: OAuthService
    _sql_manager: PostgreSqlManager
    _rules: List[Rule]

    def __init__(self):
        self._config_vars = Config()
        self._oauth_service = OAuthService(self._config_vars)
        self._gmail_service = GmailService(self._oauth_service)
        self._sql_manager = PostgreSqlManager(self._config_vars)

    def parse_rules(self):
        rules = GenericUtils.load_json(self._config_vars.credential_file)
        self._rules = [Rule(rule) for rule in rules]

    @staticmethod
    def get_column(field: str) -> str:
        return RuleColumn.from_str(field).column()

    @staticmethod
    def get_sql_condition(predicate: str) -> str:
        return RulePredicate.from_str(predicate).get_sql_condition()

    def prepare_query(self, predicate: str, conditions: List[Condition]) -> str:
        sql_query = f"SELECT {RuleColumn.MESSAGE_ID.column()} from {Config().db_table_name} WHERE"
        condition_sql = []
        for cond in conditions:
            sql_operator = self.get_sql_condition(cond.predicate)
            value = f"'%{cond.value}%'" if sql_operator == "LIKE" else f"'{cond.value}'"
            condition_sql.append(f"{self.get_column(cond.field)} {sql_operator} {value}")

        if predicate == RulePredicate.ALL.get_predicate():
            sql_query += f' {RulePredicate.ALL.get_sql_condition()} '.join(condition_sql)
        elif predicate == RulePredicate.ANY.get_predicate():
            sql_query += f' {RulePredicate.ANY.get_sql_condition()} '.join(condition_sql)
        else:
            raise NotImplementedError(f"Predicate {predicate} is not defined!!")

        return sql_query

    def apply_actions(self):

        for rule in self._rules:

            query = self.prepare_query(rule.predicate, rule.conditions)
            # Fetch emails based on conditions
            emails = self._sql_manager.fetch_emails(query)

            # Apply actions to fetched emails
            for action in rule.actions:
                match action:
                    case RuleAction.MARK_AS_READ.value:
                        print(emails)
                        return
                    case RuleAction.MARK_AS_UNREAD.value:
                        print(emails)
                        pass
                    case RuleAction.MOVE_MESSAGE.value:
                        print(emails)
                        pass
                # Add more actions as needed

    def process(self):
        self.parse_rules()
        self.apply_actions()


if __name__ == '__main__':
    EmailRuleProcessor().process()
