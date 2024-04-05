from utils.generic import GenericUtils


class Email:

    _message_id: str = None
    _sender: str = None
    _to: str = None
    _subject: str = None
    _received_date: str = None
    _message_body: str = None
    _label: str = None

    def __init__(self, message_id: str = None, label: str = None, sender: str = None, to: str = None,
                 subject: str = None, received_date: str = None, message_body: str = None):
        self._message_id = message_id
        self._label = label
        self._sender = sender
        self._to = to
        self._subject = subject
        self._received_date = received_date
        self._message_body = message_body

    @property
    def message_id(self):
        return self._message_id

    @message_id.setter
    def message_id(self, message_id):
        self._message_id = message_id

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, sender):
        self._sender = sender

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, to):
        self._to = to

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

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = str(label)

    def __str__(self):
        return (f"{'*' * 50}\nFrom: {self.sender}\nTo: {self.to}\nSubject: {self.subject}\n"
                f"Received Date: {self.received_date}\nLabel: {self.label}\n"
                f"Message Body: {self.message_body}\n{'*' * 50}")
