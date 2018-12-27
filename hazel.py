# Import necessary modules
from rasa_nlu.model import Interpreter
from constants import *

# interpreter = Interpreter.load(MODEL_PATH)
# interpreter = rasa_nlu.model.Interpreter.load(MODEL_PATH)
from train import interpreter

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


def say(role, msg, prefix=''):
    print(f"{prefix} {role}: {msg}")


def bot_say(msg):
    say('BOT', msg, ">>")


def user_say(msg):
    say('USER', msg, ">")


def take_action(action, msg, state, intent):
    if debug is True:
        print('action', action, state, intent)

    if state == CREATE_START:
        action['type'] = CREATE_ACTION
    elif state == CREATE_DESCRIPTION:
        action['description'] = msg
    elif state == CREATE_DETAIL:
        action['detail'] = msg
    elif state == CREATE_CONFIRM and intent == 'affirm':
        print('save', action)

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
    "This is a description",
    "here are the details",
    'yes',
])
