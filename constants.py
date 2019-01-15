# INIT = 0
# CREATE_START = 1
# CREATE_DESCRIPTION = 2
# CREATE_DETAIL = 3
# CREATE_CONFIRM = 4

INIT = "INIT"
CREATE_START = 'CREATE_START'
CREATE_DESCRIPTION = "CREATE_DESCRIPTION"
CREATE_DETAIL = 'CREATE_DETAIL'
CREATE_CONFIRM = 'CREATE_CONFIRM'

CREATE_ACTION = "CREATE_ACTION"
READ_ACTION = "READ_ACTION"
READ_BY_DEADLINE_ACTION = "READ_BY_DEADLINE_ACTION"
UPDATE_ACTION = "UPDATE_ACTION"
DELETE_ACTION = "DELETE_ACTION"

DELETE_CONFIRM = "DELETE_CONFIRM"
UPDATE_CONFIRM = "UPDATE_CONFIRM"

UPDATE_DETAIL = "UPDATE_DETAIL"

MODEL_PATH = './model/hazel/dev'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# standard messages
greeting_msgs = [
    "Hi, I'm a bot to remind you! ",
    "Hi, I'm Hazel, your personal reminder. Let's start with create or review your notes",
    "Hello, I'm Hazel. You can create or review your tasks now!",
]

completion_msgs = [
    "Done",
    "Finished",
    "Good to go!",
    "Completed",
]
create_start_msgs = [
    "Ok, start now. please provide a brief description",
    "Let's get started. May I have a brief description from you?"
]
create_detail_msgs = [
    "Please provide more details",
    "May I have some more details?",
]
create_confirmation_msgs = [
    'Double check if everything is correct.',
    'Please confirm the information.',
]
goodbye_msgs = [
    'Bye, have a good day! 👌',
    'Okay, see you. 🙋'
]

dont_know_what_todo_msgs = [
    "Sorry I didn't understand you.",
    "Pardon?",
]

