from enum import Enum, auto


class State(Enum):
    FIRST_NODE = auto()
    CHANGE_LANG = auto()
    REVIEW = auto()
    ADD_T = auto()
    READ_T = auto()
    READ_T_INLINE = auto()
    ADD_DESC = auto()
    ADD_RATING = auto()

    FDBK_SUBJECTS_LIST = auto()
    FDBK_ADD_NEW_SUBJECT = auto()
    FDBK_GET_TEACHER_INFO = auto()
    FDBK_TEACHERS_LIST = auto()
    FDBK_POLLS = auto()
    FDBK_POLLS_ASK_COMMENTS = auto()
    FDBK_POLLS_GET_COMMENTS = auto()

    HELP_CHOSE_SUBJECT = auto()
    HELP_CHOSE_SUBJECT_OTHER = auto()
    HELP_CHOSE_TYPE = auto()
    HELP_CHOSE_AWARD = auto()
    HELP_CHOSE_DESCRIPTION = auto()
    HELP_CHECKING_REQUEST = auto()
    HELP_SUBJECT_AGAIN = auto()
    HELP_SUBJECT_OTHER_AGAIN = auto()
    HELP_TYPE_AGAIN = auto()
    HELP_AWARD_AGAIN = auto()
    HELP_DESCRIPTION_AGAIN = auto()
    HELP_MATCHING = auto()
    HELP_MATCHED = auto()
    ADD_T_INLINE = auto()
    ADDICTIONAL_ADD = auto()
    READ_FROM_SUBJECT = auto()
    ADD_TO_SUBJECT = auto()
    ADD_NEW_SUBJECT = auto()