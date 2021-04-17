from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.exceptions import ProcessFailure
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot


# First Time chat responder
@processor(
    state_manager,
    from_states=state_types.Reset,
    update_types=[update_types.EditedMessage, update_types.Message],
    message_types=message_types.Text,
    success='waiting_for_start_command',
    fail=state_types.Keep,

)
def begin(bot: TelegramBot, update: Update, state: TelegramState):
    msg = "Hello, welcome to Farm Finance.Click /start to get started"
    bot.sendMessage(update.get_chat().get_id(), msg)


# Start Command acceptor
@processor(
    state_manager,
    from_states='waiting_for_start_command',
    update_types=[update_types.EditedMessage, update_types.Message],
    message_types=message_types.Text,
    success='menu_mode',
    fail=state_types.Keep,
)
def start(bot, update, state):
    chat_msg = str(update.get_message().get_text())
    if chat_msg == '/start':
        msg = "Welcome to FarmFinance Airdrop,follow these  /procedures  to qualify for our airdrop.Send  /menu for a list of available actions"
        bot.sendMessage(update.get_chat().get_id(), msg)
    else:
        msg = 'Please send /start to get started.'
        bot.sendMessage(update.get_chat().get_id(), msg)
        raise ProcessFailure


# Procedures Acceptor
@processor(
    state_manager,
    from_states='menu_mode',
    update_types=[update_types.EditedMessage, update_types.Message],
    message_types=message_types.Text,
    success=state_types.Keep,
    fail=state_types.Keep,

)
def menu(bot, update, state):
    chat_msg = str(update.get_message().get_text())
    if chat_msg == '/menu':
        msg = 'Here are the available actions\n\n. 1. send /account for account info.\n2. Send /withdraw for withdrawal'
        bot.sendMessage(update.get_chat().get_id(), msg)
    else:
        msg = "Please send a valid command"
        bot.sendMessage(update.get_chat().get_id(), msg)
        raise ProcessFailure
