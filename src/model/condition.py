
class Condition:

    _field: str
    _predicate: str
    _value: str

    def __init__(self, condition: dict):
        self._field = condition['field']
        self._predicate = condition['predicate']
        self._value = condition['value']

    @property
    def field(self) -> str:
        return self._field

    @property
    def predicate(self) -> str:
        return self._predicate

    @property
    def value(self) -> str:
        return self._value
