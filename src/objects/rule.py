from typing import List, Dict, Union

from objects.condition import Condition


class Rule:
    _description: str
    _predicate: str
    _conditions: List[Condition]
    _actions: Dict[str, Union[str, bool]]

    def __init__(self, rule: dict):
        self._description = rule['description']
        self._predicate = rule['predicate']
        self._conditions = [Condition(condition) for condition in rule['conditions']]
        self._actions = rule['actions']

    @property
    def description(self) -> str:
        return self._description

    @property
    def predicate(self) -> str:
        return self._predicate

    @property
    def conditions(self) -> List[Condition]:
        return self._conditions

    @property
    def actions(self) -> Dict[str, Union[str, bool]]:
        return self._actions
