from constants import *
# use existing model
# from rasa_nlu.model import Interpreter
# interpreter = Interpreter.load(MODEL_PATH)

# train new model
from train import interpreter, extract_entities
from db import db
import dateparser, timeago, re, random, datetime

print('=-=-=-=-=-=-=')
print('Model Loaded')
print('=-=-=-=-=-=-=')

# Define the policy rules dictionary
policy_rules = {
    (INIT, "greet"): (INIT, greeting_msgs),
    (INIT, "affirm"): (INIT, greeting_msgs),
    (INIT, "create_start"): (CREATE_DESCRIPTION, create_start_msgs),
    (CREATE_DESCRIPTION, None): (CREATE_DETAIL, create_detail_msgs),
    (CREATE_DETAIL, None): (CREATE_CONFIRM, create_confirmation_msgs),
    (CREATE_CONFIRM, 'affirm'): (INIT, completion_msgs),
    (DELETE_CONFIRM, 'affirm'): (INIT, completion_msgs),
    (READ_BY_DEADLINE_ACTION, None): (INIT, None),
    (INIT, 'read_all'): (INIT, None),
    (INIT, 'read_more'): (INIT, None),
    (INIT, 'delete'): (DELETE_CONFIRM, 'Are you sure you want to delete?'),
    (INIT, 'update'): (UPDATE_DETAIL, 'Please tell me what you want to update.'),
    (UPDATE_DETAIL, None): (INIT, completion_msgs),
}

debug = True


def say(role, msg, prefix='', color=None):
    msg = f"{prefix} {role}: {msg}"

    if color is not None:
        msg = color + msg + bcolors.ENDC

    print(msg)


def bot_say(msg):
    global global_res

    global_res.append(msg)

    if msg is not None:
        say('BOT', msg, prefix=">>", color=bcolors.OKGREEN)


def user_say(msg):
    if msg is not None:
        say('USER', msg, prefix=">", color=bcolors.FAIL)


def parse_for_entities(task, msg, quiet=False):
    ents = extract_entities(msg)
    print('[ents]: ', ents)

    # parse for location
    locations = []
    if 'FAC' in ents and ents['FAC'] is not None:
        locations.append(ents['FAC'])
    if 'ORG' in ents and ents['ORG'] is not None:
        locations.append(ents['ORG'])
    if 'GPE' in ents and ents['GPE'] is not None:
        locations.append(ents['GPE'])
    locations = [ents['FAC'], ents['ORG'], ents['GPE']]
    # Remove None and cast to String
    locations = [str(item) for item in locations if item is not None]
    if len(locations) > 0:
        task['locations'] = ", ".join(locations)

    # parse for time
    times = []
    if 'TIME' in ents and ents['TIME'] is not None:
        times.append(ents['TIME'])
    if 'DATE' in ents and ents['DATE'] is not None:
        times.append(ents['DATE'])
    # Remove None and cast to String
    times = [str(item) for item in times if item is not None]
    if len(times) > 0:
        action_times = ", ".join(times)
        task['times'] = action_times
        task['deadline'] = dateparser.parse(action_times)

    # parse for people
    if 'PERSON' in ents and ents['PERSON'] is not None:
        people = [str(person) for person in ents['PERSON']]
        task['people'] = ", ".join(people)

    if quiet is False:
        bot_say(prettify_task(task))

    return task

def prettify_task(task):
    temp = ""
    key_arr = ['description', 'detail', 'locations', 'people', 'deadline']
    name_arr = ['Description', 'Detail', 'Location', 'People', 'Deadline']

    for index, (key, name) in enumerate(zip(key_arr, name_arr)):
        if key in task and task[key] is not None:
            if key == 'detail':
                temp += f"<{name}>:\n {task[key]}\n"
            else:
                temp += f"<{name}>: {task[key]}\n"

    return temp

def prettify_tasks_summary(tasks):
    res = ''
    now = datetime.datetime.now()
    for index, task in enumerate(tasks):
        tasks[index]['index'] = index + 1
        deadline = task['deadline']

        if deadline is None:
            res += f"{index + 1}: {task['description']}\n"
        else:
            res += f"{index + 1}: {task['description']} [{timeago.format(deadline, now)}]\n"

    return res

def take_action(action, msg, state, intent):
    if debug is True:
        print('action', action, state, intent)

    if state == CREATE_START:
        action['type'] = CREATE_ACTION
    elif state == CREATE_DESCRIPTION:
        action['description'] = msg
    elif state == CREATE_DETAIL:
        action['detail'] = msg

        msg_to_parse = action['description'] + '. ' + action['detail']
        action = parse_for_entities(action, msg_to_parse)
    elif state == INIT and intent == 'read_all':
        entities = parse_for_entities({}, msg, quiet=True)
        print(entities)

        deadline = None
        tasks = []

        if entities is None or 'deadline' not in entities:
            tasks = db.read_all()
        else:
            deadline = entities['deadline']
            tasks = db.read(deadline)

        if len(tasks) == 0:
            if deadline is None:
                bot_say('You have no tasks. Use <create new> to create a new task.')
            else:
                bot_say(f'You have no tasks due {entities["times"]}. Would you like to see your upcoming tasks?')
                return action, READ_BY_DEADLINE_ACTION
        else:
            res = prettify_tasks_summary(tasks)

            bot_say(str(res))
            action['type'] = READ_ACTION
            action['tasks'] = tasks
    elif state == READ_BY_DEADLINE_ACTION and intent == 'affirm':
        tasks = db.read_all(True)

        if (len(tasks)==0):
            bot_say('You have no tasks. Use <create new> to create a new task.')
        else:
            res = prettify_tasks_summary(tasks)

            bot_say(str(res))
            action['type'] = READ_ACTION
            action['tasks'] = tasks
    elif state == READ_BY_DEADLINE_ACTION and intent != 'affirm':
        bot_say("I will take that as a [no] 🈲️")
    elif state == INIT and intent == "read_more":
        tasks = action['tasks']
        index = int(re.search(r"[1-9][0-9]*", msg).group(0))

        if action['type'] == READ_ACTION and index <= len(tasks):
            task = tasks[index - 1]
            bot_say(prettify_task(task))
        else:
            bot_say('Invalid Index. Use [list all] to show all tasks')
    elif state == INIT and intent == 'delete':
        index = int(re.search(r"[1-9][0-9]*", msg).group(0))
        action['type'] = DELETE_ACTION
        action['index'] = index
        tasks = action['tasks']

        if index <= len(tasks):
            task = tasks[index - 1]
            bot_say(prettify_task(task))
        else:
            bot_say('Invalid Index. Use [list all] to show all tasks')
    elif state == DELETE_CONFIRM and intent == 'affirm':
        tasks = action['tasks']
        index = action['index']

        if action['type'] == DELETE_ACTION and index <= len(tasks):
            task = tasks[index - 1]
            bot_say(f'Deleting {index}: {task["description"]}')
            db.delete(task['id'])
        else:
            bot_say('Invalid Index. Use [list all] to show all tasks')
    elif state == CREATE_CONFIRM and intent == 'affirm':
        print('save', action)
        db.create(action)

        del_key_arr = ['description', 'detail', 'times', 'locations', 'people', 'deadline']
        for key in del_key_arr:
            if key in action:
                del action[key]

        print('db action done')
    elif state == INIT and intent == 'update':
        parsed_index = int(re.search(r"[1-9][0-9]*", msg).group(0))

        if parsed_index is None and 'index' not in action:
            bot_say("Invalid Index. Use [list all] to show all tasks")
            return

        if parsed_index is not None:
            action['index'] = parsed_index

        tasks = action['tasks']
        if tasks is None or action['index'] > len(tasks):
            bot_say("Invalid Index. Use [list all] to show all tasks")
            return
    elif state == UPDATE_DETAIL:
        bot_say(msg)
        print('before >> ', action)
        index = action['index']
        task = action['tasks'][index - 1]
        task['detail'] = '\n[update]\n'.join([task['detail'], msg])

        msg_to_parse = task['description'] + '. ' + task['detail']
        task = parse_for_entities(task, msg_to_parse)
        action['tasks'][index - 1] = task
        print('after >> ', action)
        db.update(action)

    return action, None


# Define send_message()
def send_message(state, action, message):
    global global_res

    user_say(message)

    parse_result = interpreter.parse(message)
    intent = parse_result['intent']['name']
    confidence = parse_result['intent']['confidence']
    print(state, intent, confidence)

    if intent == 'quit':
        bot_say(random.choice(goodbye_msgs))
        return INIT, {}

    pair = (state, intent)
    skip_intent = False
    if state in [CREATE_DESCRIPTION, CREATE_DETAIL, UPDATE_DETAIL, READ_BY_DEADLINE_ACTION]:
        pair = (state, None)
        skip_intent = True

    if skip_intent == False and (pair not in policy_rules or confidence < 0.35):
        bot_say(random.choice(dont_know_what_todo_msgs))
        return state, action

    next_state, response = policy_rules[pair]
    action, proposed_next_state = take_action(action, message, state, intent)

    if proposed_next_state is not None:
        next_state = proposed_next_state

    if debug is True:
        print(f"state: {state}, intent: {intent}, next_state: {next_state}")

    if type(response) == type([]):
        bot_say(random.choice(response))
    else:
        bot_say(response)

    print("r>", global_res)
    return next_state, action


# Define send_messages()
global_state = INIT
global_action = {}
global_res = []


def send_messages(messages):
    global global_state
    global global_action

    for msg in messages:
        global_state, global_action = send_message(global_state, global_action, msg)


def wechat_send_message(message):
    global global_state
    global global_action
    global global_res
    global_res = []

    global_state, global_action = send_message(global_state, global_action, message)
    return global_res


# create
# send_messages([
#     "Hi",
#     "Create new reminder",
#     "Dinner on December 13th with David",
#     # "Dinner tomorrow with David",
#     "3 pm at the Keg in Mississauga",
#     'yes',
# ])

# read
# send_messages([
#     "show me my notes",
#     "more on 2",
#     "more details on 3",
#     "remove 2",
#     "yea",
#     "show me all notes",
# ])

# update
# send_messages([
#     "show me all notes",
#     'more on 1',
#     "update 1",
#     "change the time to 5pm",
#     "update 1",
#     "Bob is also coming",
#     "1",
# ])
