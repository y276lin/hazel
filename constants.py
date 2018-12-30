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
UPDATE_ACTION = "UPDATE_ACTION"
DELETE_ACTION = "DELETE_ACTION"
DELETE_CONFIRM = "DELETE_CONFIRM"

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
