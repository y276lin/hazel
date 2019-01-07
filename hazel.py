from constants import *
# use existing model
# from rasa_nlu.model import Interpreter
# interpreter = Interpreter.load(MODEL_PATH)

# train new model
from train import interpreter, extract_entities
from db import db
import re
import dateparser

print('=-=-=-=-=-=-=')
print('Model Loaded')
print('=-=-=-=-=-=-=')

# Define the policy rules dictionary
policy_rules = {
    (INIT, "greet"): (INIT, "I'm a bot to remind you"),
    (INIT, "affirm"): (INIT, "I'm a bot to remind you"),
    (INIT, "create_start"): (CREATE_DESCRIPTION, "Ok, start now. please provide a brief description"),
    (CREATE_DESCRIPTION, None): (CREATE_DETAIL, "Please provide more details"),
    (CREATE_DETAIL, None): (CREATE_CONFIRM, "Double check if everything is correct"),
    (CREATE_CONFIRM, 'affirm'): (INIT, 'Done'),
    (DELETE_CONFIRM, 'affirm'): (INIT, 'Done'),
    (INIT, 'read_all'): (INIT, None),
    (INIT, 'read_more'): (INIT, None),
    (INIT, 'delete'): (DELETE_CONFIRM, 'Are you sure you want to delete?'),
    (INIT, 'update'): (UPDATE_DETAIL, 'Please say what you want to update.'),
    (UPDATE_DETAIL, None): (INIT, 'Done'),
}

debug = True


def say(role, msg, prefix='', color=None):
    msg = f"{prefix} {role}: {msg}"

    if color is not None:
        msg = color + msg + bcolors.ENDC

    print(msg)


def bot_say(msg):
    if msg is not None:
        say('BOT', msg, prefix=">>", color=bcolors.OKGREEN)


def user_say(msg):
    if msg is not None:
        say('USER', msg, prefix=">", color=bcolors.FAIL)

def parse_for_entities(task, msg):
    ents = extract_entities(msg)
    bot_say(ents)

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

    bot_say(task)
    return task

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

        bot_say(str(action))
    elif state == INIT and intent == 'read_all':
        tasks = db.read_all()
        res = '\n'
        for index, task in enumerate(tasks):
            tasks[index]['index'] = index + 1
            res += f"{index + 1}: {task['description']}\n"

        bot_say(str(res))
        action['type'] = READ_ACTION
        action['tasks'] = tasks
    elif state == INIT and intent == "read_more":
        tasks = action['tasks']
        index = int(re.search(r"[1-9][0-9]*", msg).group(0))

        if action['type'] == READ_ACTION and index <= len(tasks):
            bot_say(tasks[index - 1])
        else:
            bot_say('Invalid Index. Use [list all] to show all tasks')
    elif state == INIT and intent == 'delete':
        index = int(re.search(r"[1-9][0-9]*", msg).group(0))
        action['type'] = DELETE_ACTION
        action['index'] = index
        tasks = action['tasks']

        if index <= len(tasks):
            task = tasks[index - 1]
            bot_say(task)
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

    return action


# Define send_message()
def send_message(state, action, message):
    user_say(message)

    intent = interpreter.parse(message)['intent']['name']
    print(state, intent)

    if intent == 'quit':
        return INIT, {}

    if state in [CREATE_DESCRIPTION, CREATE_DETAIL, UPDATE_DETAIL]:
        intent = None

    pair = (state, intent)

    if pair not in policy_rules:
        bot_say("Sorry I don't know what to do")
        return state, action

    next_state, response = policy_rules[pair]
    action = take_action(action, message, state, intent)

    if debug is True:
        print(f"state: {state}, intent: {intent}, next_state: {next_state}")

    bot_say(response)
    return next_state, action


# Define send_messages()
def send_messages(messages):
    state = INIT
    action = {}

    for msg in messages:
        state, action = send_message(state, action, msg)


# create
send_messages([
    "Hi",
    "Create new reminder",
    "Dinner on December 13th with David",
    # "Dinner tomorrow with David",
    "3 pm at the Keg in Mississauga",
    'yes',
])

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
send_messages([
    "show me all notes",
    'more on 1',
    "update 1",
    "change the time to 5pm",
    "update 1",
    "Bob is also coming",
    "1",
])
