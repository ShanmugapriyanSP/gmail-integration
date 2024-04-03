from typing import List

from model.condition import Condition


class Rule:

    _predicate: str
    _conditions: List[Condition]
    _actions: List[str]

    def __init__(self, rule: dict):
        self._predicate = rule['predicate']
        self._conditions = [Condition(condition) for condition in rule['conditions']]
        self._actions = rule['actions']

    @property
    def predicate(self) -> str:
        return self._predicate

    @property
    def conditions(self) -> List[Condition]:
        return self._conditions

    @property
    def actions(self) -> List[str]:
        return self._actions
