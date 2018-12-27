# Import necessary modules
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config

# Create a trainer that uses this config
trainer = Trainer(config.load("./config/config_spacy.yml"))

# Load the training data
training_data = load_data('./config/rasa.json')

# Create an interpreter by training the model
interpreter = trainer.train(training_data)

print('=-=-=-=-=-=-=-=-=-=')
print('Model Training Done')
print('=-=-=-=-=-=-=-=-=-=')

# Define the states
from constants import *

# Define the policy rules dictionary
policy_rules = {
    (INIT, "greet"): (INIT, "I'm a bot to remind you"),
    (INIT, "create_start"): (CREATE_START, "Ok, start now. please provide a brief description"),
    # (CREATE_START, 'create_description'): (CREATE_DESCRIPTION, "perfect, the beans are on their way!"),
    # (CREATE_DESCRIPTION, "create_details"): (CREATE_DETAIL,
    #                                          "We have two kinds of coffee beans - the Kenyan ones make a slightly sweeter coffee, and cost $6. The Brazilian beans make a nutty coffee and cost $5.")
}


# Define send_messages()
def send_messages(messages):
    state = INIT
    for msg in messages:
        state = send_message(state, msg)


def interpret(message):
    msg = message.lower()
    if 'order' in msg:
        return 'order'
    elif 'yes' in msg:
        return 'affirm'
    elif 'no' in msg:
        return 'deny'
    return 'none'


# Define policy()
def policy(intent):
    # Return "do_pending" if the intent is "affirm"
    if intent == "affirm":
        return "do_pending", None
    # Return "Ok" if the intent is "deny"
    if intent == "deny":
        return "OK", None
    if intent == "order":
        return "Unfortunately, the Kenyan coffee is currently out of stock, would you like to order the Brazilian beans?", "Alright, I've ordered that for you!"


def send_message(message, pending):
    print(f"USER : {message}")
    answer, pending_action = policy(interpret(message))
    if answer == "do_pending" and pending is not None:
        print("BOT : {}".format(pending))
    else:
        print("BOT : {}".format(answer))
    return pending_action


# Send the messages
send_messages([
    "what can you do for me?",
    "make a new reminder",
    "Finish midterm project before wednesday",
])
