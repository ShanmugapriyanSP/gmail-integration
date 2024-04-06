from typing import List, Dict


class BatchModifyRequest:
    """
    Used for the Batch Modify call in Gmail
    """

    _msg_ids: List[str]
    _add_label_ids: List[str]
    _remove_label_ids: List[str]

    def __init__(self, msg_ids: List[str], add_label_ids: List[str] = None, remove_label_ids: List[str] = None):
        self._msg_ids = msg_ids
        self._add_label_ids = add_label_ids
        self._remove_label_ids = remove_label_ids

    def json(self) -> Dict:
        request_body = {
            "ids": self._msg_ids
        }

        if self._add_label_ids and len(self._add_label_ids) > 0:
            request_body["addLabelIds"] = self._add_label_ids
        if self._remove_label_ids and len(self._remove_label_ids) > 0:
            request_body["removeLabelIds"] = self._remove_label_ids

        return request_body
