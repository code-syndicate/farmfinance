from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot



# First Time chat responder 
@processor(
    state_manager,
    from_states = state_types.Reset, 
    update_types = [ update_types.EditedMessage, update_types.Message ], 
    message_types = [ message_types.Text, ]

)
def respond_to_start( bot : TelegramBot, update : Update, state : TelegramState):
    msg = "Hello!, welcome to Farm Finance.Click /start to get started"
    bot.sendMessage( update.get_chat().get_id(), msg  )

