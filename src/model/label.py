
class Label:

    _id: str
    _name: str

    def __init__(self, _id: str, name: str):
        self._id = _id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
