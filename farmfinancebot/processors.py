from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot

valid_commands = [ 
    '/start',
    '/commands',
    '/withdraw',
    '/account',
]



# First Time chat responder 
@processor(
    state_manager,
    from_states = [ state_types.Reset, state_types.All  ], 
    update_types = [ update_types.EditedMessage, update_types.Message ], 
    message_types = [ message_types.Text, ],
    success = 'waiting_for_start_command',

)
def first_timers_responder( bot : TelegramBot, update : Update, state : TelegramState):
    msg = "Hello!, welcome to Farm Finance.Click /start to get started"
    bot.sendMessage( update.get_chat().get_id(), msg  )


# /start command responder 
@processor(
    state_manager,
    from_states = [ 'waiting_for_start_command',],
    update_types = [ update_types.EditedMessage, update_types.Message ],
    message_types = [ message_types.Text, ],
    # success = 'sent_start',
)
def respond_to_start( bot : TelegramBot, update : Update, state : TelegramState):
    msg = 'Welcome to Farm Finance Token.Please check out the  /procedures to qualify for our upcoming airdrop'
    if  not (str(update.get_message().get_text()) in valid_commands ):
        msg = "Please send a valid command.Send /commands to see available commands"
        bot.sendMessage( update.get_chat().get_id(), msg )
    
    bot.sendMessage( update.get_chat().get_id(), msg)




