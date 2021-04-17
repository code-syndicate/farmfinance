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
    from_states = state_types.Reset,
    update_types = [ update_types.EditedMessage, update_types.Message ], 
    message_types = message_types.Text,
    success = 'waiting_for_start_command',
    fail = state_types.Keep,

)
def begin( bot : TelegramBot, update : Update, state : TelegramState):
    msg = "Hello!, welcome to Farm Finance.Click /start to get started"
    bot.sendMessage( update.get_chat().get_id(), msg  )


# # Start Command acceptor
# @processor(
#     state_manager,
#     from_states = 'waiting_for_start_command',
#     update_types = [ update_types.EditedMessage, update_types.Message],
#     message_types = message_types.Text,
#     success = 'started_bot',
#     fail = state_types.Keep,
# )
# def start(bot : TelegramBot, update : Update, state : TelegramState):
#     chat_msg = str(state.get_message().get_text())
#     if chat_msg == '/start':
#         msg = "Welcome to FarmFinance,follow these /procedures to qualify for our airdrop.Send /commands for a list of available commands."
#         bot.sendMessage( update.get_chat().get_id(), msg )
#     else:
#         msg = 'Please send a valid command.Check /commands'
#         bot.sendMessage( update.get_chat().get_id(), msg)
#         raise ProcessFailure

