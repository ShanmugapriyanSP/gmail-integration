from enum import Enum

class RuleAction(Enum):

    MARK_AS_READ = 'Mark as read'
    MARK_AS_UNREAD = 'Mark as unread'
    MOVE_MESSAGE = 'Move message'