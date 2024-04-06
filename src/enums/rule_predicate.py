from enum import Enum


class RulePredicate(Enum):
    """
    Enum Mapper class to match Predicate provided in the rules JSON with SQL operator/condition
    """
    CONTAINS = ('contains', 'LIKE')
    DOES_NOT_CONTAINS = ('does not contain', 'NOT LIKE')
    EQUALS = ('equals', '=')
    DOES_NOT_EQUAL = ('does not equal', '!=')
    LESS_THAN = ('less than', '<')
    GREATER_THAN = ('greater than', '>')
    ALL = ('all', 'AND')
    ANY = ('any', 'OR')

    @property
    def predicate(self) -> str:
        return str(self.value[0])

    @property
    def sql_condition(self) -> str:
        return str(self.value[1])

    @staticmethod
    def from_str(predicate: str):
        result = list(filter(lambda rule_predicate: rule_predicate.predicate == predicate.lower(),
                             RulePredicate))
        if len(result) == 1:
            return result[0]
        raise NotImplementedError(f"RulePredicate: {predicate} is not defined in the enum")

