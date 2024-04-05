from enum import Enum


class RuleColumn(Enum):
    ID = ('', 'id')
    MESSAGE_ID = ('', 'message_id')
    FROM = ('From', 'sender')
    TO = ('To', 'receiver')
    SUBJECT = ('Subject', 'subject')
    MESSAGE = ('Message', 'message_body')
    RECEIVED_DATE = ('Date Received', 'received_date')
    LABEL = ('Label', 'label')

    @property
    def field(self):
        return str(self.value[0])

    @property
    def column(self):
        return str(self.value[1])

    @staticmethod
    def from_str(field: str):
        result = list(filter(lambda rule_column: rule_column.field == field.capitalize(), RuleColumn))
        if len(result) == 1:
            return result[0]
        raise NotImplementedError(f"RuleColumn: {field} is not defined in the enum")
