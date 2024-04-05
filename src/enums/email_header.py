from enum import Enum


class EmailHeader(Enum):
    SUBJECT = 'Subject'
    FROM = 'From'
    RECEIVED_DATE = 'Date'
    TO = 'To'
