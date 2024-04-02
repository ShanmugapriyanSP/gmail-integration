from utils.generic import GenericUtils


class Email:

    _sender: str
    _subject: str
    _received_date: str
    _message_body: str

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, sender):
        self._sender = sender

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, subject):
        self._subject = subject

    @property
    def received_date(self):
        return self._received_date

    @received_date.setter
    def received_date(self, received_date):
        self._received_date = GenericUtils.format_date(received_date)

    @property
    def message_body(self):
        return self._message_body

    @message_body.setter
    def message_body(self, message_body):
        self._message_body = message_body

    def __str__(self):
        return f"{'*' * 50}\nSender: {self._sender}\nSubject: {self._subject}\nReceived Date: {self._received_date}\n"\
               f"Message Body: {self._message_body}\n{'*' * 50}"
