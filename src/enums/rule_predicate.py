from enum import Enum


class RulePredicate(Enum):
    CONTAINS = ('Contains', 'LIKE')
    EQUALS = ('Equals', '=')
    DOES_NOT_EQUAL = ('Does not equal', '!=')
    LESS_THAN = ('Less than', '<')
    GREATER_THAN = ('Greater than', '>')
    ALL = ('All', 'AND')
    ANY = ('Any', 'OR')

    @property
    def predicate(self) -> str:
        return str(self.value[0])

    @property
    def sql_condition(self) -> str:
        return str(self.value[1])

    @staticmethod
    def from_str(predicate: str):
        result = list(filter(lambda rule_predicate: rule_predicate.predicate == predicate.capitalize(),
                             RulePredicate))
        if len(result) == 1:
            return result[0]
        raise NotImplementedError(f"RulePredicate: {predicate} is not defined in the enum")

