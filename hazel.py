from constants import *
# use existing model
# from rasa_nlu.model import Interpreter
# interpreter = Interpreter.load(MODEL_PATH)

# train new model
from train import interpreter, extract_entities
from db import db

print('=-=-=-=-=-=-=')
print('Model Loaded')
print('=-=-=-=-=-=-=')

# Define the policy rules dictionary
policy_rules = {
    (INIT, "greet"): (INIT, "I'm a bot to remind you"),
    (INIT, "create_start"): (CREATE_DESCRIPTION, "Ok, start now. please provide a brief description"),
    (CREATE_DESCRIPTION, None): (CREATE_DETAIL, "Please provide more details"),
    (CREATE_DETAIL, None): (CREATE_CONFIRM, "Double check if everything is correct"),
    (CREATE_CONFIRM, 'affirm'): (INIT, 'Done'),
}

debug = True


def say(role, msg, prefix='', color=None):
    msg = f"{prefix} {role}: {msg}"

    if color is not None:
        msg = color + msg + bcolors.ENDC

    print(msg)


def bot_say(msg):
    say('BOT', msg, prefix=">>", color=bcolors.FAIL)


def user_say(msg):
    say('USER', msg, prefix=">", color=bcolors.OKGREEN)


def take_action(action, msg, state, intent):
    if debug is True:
        print('action', action, state, intent)

    if state == CREATE_START:
        action['type'] = CREATE_ACTION
    elif state == CREATE_DESCRIPTION:
        action['description'] = msg
    elif state == CREATE_DETAIL:
        action['detail'] = msg
        ents = extract_entities(action['description'] + '. ' + action['detail'])
        print(ents)

        # parse for location
        locations = [ents['FAC'], ents['ORG'], ents['GPE']]
        locations = [str(item) for item in locations if item is not None]
        action['locations'] = ', '.join(locations) if len(locations) > 0 else None

        # parse for time
        times = [ents['TIME'], ents['DATE']]
        times = [str(item) for item in times if item is not None]
        action['times'] = ', '.join(times) if len(times) > 0 else None

        # parse for people
        action['people'] = str(ents['PERSON']) if 'PERSON' in ents else None

        bot_say(str(action))
    elif state == CREATE_CONFIRM and intent == 'affirm':
        print('save', action)
        db.create(action)

    return action


# Define send_message()
def send_message(state, action, message):
    user_say(message)

    intent = interpreter.parse(message)['intent']['name']

    if intent == 'quit':
        return INIT, {}

    if state == CREATE_DESCRIPTION or state == CREATE_DETAIL:
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


# Send the messages
send_messages([
    "Hi",
    "Create new reminder",
    "Dinner on December 13th with David",
    # "Dinner tomorrow with David",
    "3 pm at the Keg in Mississauga",
    'yes',
])
