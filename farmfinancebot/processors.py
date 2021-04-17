from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.exceptions import ProcessFailure
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot

valid_commands = [
    '/menu',
    '/account',
    '/proceed',
    '/procedures'
    
]


# # First Time chat responder
# @processor(
#     state_manager,
#     from_states=state_types.Reset,
#     update_types=[update_types.EditedMessage, update_types.Message],
#     message_types=message_types.Text,
#     success='waiting_for_start_command',
#     fail=state_types.Keep,

# )
# def begin(bot: TelegramBot, update: Update, state: TelegramState):
#     msg = "Hello, welcome to Farm Finance.Click /start to get started"
#     bot.sendMessage(update.get_chat().get_id(), msg)


# Start Command acceptor
@processor(
    state_manager,
    from_states=  state_types.Reset,
    update_types=[update_types.EditedMessage, update_types.Message],
    message_types=message_types.Text,
    success='command_mode',
    fail=state_types.Keep,
)
def start(bot : TelegramBot , update : Update, state : TelegramState):
    chat_msg = str(update.get_message().get_text())
    username = state.telegram_user.first_name.capitalize()
    if chat_msg == '/start':
        msg1 = "Hello " + username + ", I am your friendly FarmFinance Airdrop bot.\nComplete the tasks below to get up to $50 FAFI token.\n\n"
        msg2 = "\U00002733 Join our telegram <a href = 'http://t.me/farmfinancebsc/'> group  </a> and  <a href = 'http://t.me/farmfinanceupdates/'> channel </a>.\n\n"
        msg3 = "\U00002733 Follow us on <a href = 'http://twitter.com/farm_financeBsc/'> twitter </a>, retweet the pinned tweet about our airdrop.\n\n "
        msg4 = '\U00002733 Once done, click on /proceed\n'
        msg5 = '\n\nClick /menu for a list of other available options.'

        msg = msg1 + msg2 + msg3  + msg4 + msg5
        
        state.set_memory({
            'submittedTwitterLink' : False,
            'setLogo' : False,
            'RetweetedPost' : False,
            'completedAllTasks' : False,
        })

        bot.sendMessage(update.get_chat().get_id(), msg, parse_mode =  TelegramBot.PARSE_MODE_HTML)
    else:
        msg = "Hello " + username + " \U000026C4 , welcome to Farm Finance.Click  /start  to get started."
        bot.sendMessage(update.get_chat().get_id(), msg)
        raise ProcessFailure


# Procedures Acceptor
@processor(
    state_manager,
    from_states='command_mode',
    update_types=[update_types.EditedMessage, update_types.Message],
    message_types=message_types.Text,
    success=state_types.Keep,
    fail=state_types.Keep,

)
def command_processor(bot, update, state):
    chat_msg = str(update.get_message().get_text())
    username = state.telegram_user.first_name.capitalize()

    if not( chat_msg in valid_commands ):
        msg = 'Please send a valid action.Click /menu for available options.'
        bot.sendMessage(update.get_chat().get_id(), msg)
        raise ProcessFailure
    
    command = chat_msg

    if command == '/menu':
        reply = 'Here are the available actions.\n\n\U00002733Send /account for account info.\n\n\U00002733Send /withdraw  to request for withdrawal.'
        bot.sendMessage(update.get_chat().get_id(), reply )

    elif command == '/account':
        info = ""
        if state.get_memory()['completedAllTasks'] is True:
            info = "You have  been verified for withdrawal \U00002714"
        else:
            info = "You are not yet eligible for withdrawal \U0000274c"
        reply = 'Here is your account info\n\nWithdrawal status : ' + info
        bot.sendMessage(update.get_chat().get_id(), reply )

    elif command == '/proceed':
        if state.get_memory()['completedAllTasks'] is True:
            msg = " \U00002714.\n\nEnter your Bep20 Binance smartchain address(ex. Trust Wallet, Metamask, etc, exchange wallets not applicable for airdrop)."
            state.set_name('waiting_for_wallet_address')
            bot.sendMessage(update.get_chat().get_id(), msg )
        else:

            reply = 'You are not yet eligible for withdrawal \U0000274c Please make sure you have completed all tasks, then try again later.Thank you.'
            bot.sendMessage(update.get_chat().get_id(), reply )
            raise ProcessFailure
    
    elif command == '/procedures':
        reply = "Follow  the following procedures to receive your airdrop.\n\n"
        msg1 = "Complete the tasks below to get up to $50 FAFI token.\n\n"
        msg2 = "\U00002733 Join our telegram <a href = 'http://t.me/farmfinancebsc/'> group  </a> and  <a href = 'http://t.me/farmfinanceupdates/'> channel </a>.\n\n"
        msg3 = "\U00002733 Follow us on <a href = 'http://twitter.com/farm_financeBsc/'> twitter </a>, retweet the pinned tweet about our airdrop.\n\n "
        msg4 = '\U00002733 Once done, click on /proceed\n'
        reply += msg1 + msg2 + msg3 + msg4
        bot.sendMessage(update.get_chat().get_id(),  reply , parse_mode =  TelegramBot.PARSE_MODE_HTML )


    


