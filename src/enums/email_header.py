from enum import Enum


class EmailHeader(Enum):
    SUBJECT = 'Subject'
    FROM = 'From'
    RECEIVED_DATE = 'Date'
    TO = 'To'
    #
    # @staticmethod
    # def from_str(header):
    #     result = list(filter(lambda email_header: email_header == header, EmailHeader))
    #     if len(result) == 1:
    #         return result[0]
    #     raise NotImplementedError(f'EmailHeader: {header} is not defined in the enum')
