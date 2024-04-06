from enum import Enum


class RuleColumn(Enum):
    """
    Enum Mapper class to match the Field provided in the rules JSON with database Column
    """
    ID = ('', 'id')
    MESSAGE_ID = ('', 'message_id')
    FROM = ('from', 'sender')
    TO = ('to', 'receiver')
    SUBJECT = ('subject', 'subject')
    MESSAGE = ('message', 'message_body')
    RECEIVED_DATE = ('date received', 'received_date')
    LABEL = ('label', 'label')

    @property
    def field(self):
        return str(self.value[0])

    @property
    def column(self):
        return str(self.value[1])

    @staticmethod
    def from_str(field: str):
        result = list(filter(lambda rule_column: rule_column.field == field.lower(), RuleColumn))
        if len(result) == 1:
            return result[0]
        raise NotImplementedError(f"RuleColumn: {field} is not defined in the enum")
