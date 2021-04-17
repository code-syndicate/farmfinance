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
    '/withdraw',
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
        msg2 = '1. Join our telegram group at http://t.me/farmfinancebsc/.\n2. Join our telegram channel at http://t.me/farmfinanceupdates/.\n'
        msg3 = '3. Follow our twitter account at http://twitter.com/farm_financeBsc/\n4. Like and retweet our pinned tweet about the airdrop on twitter. '
        msg4 = '\n5. Use our FarmFinance logo as your profile picture on telegram and twitter.'
        msg5 = '\n\n\nlick /menu for a list of available options.'

        msg = msg1 + msg2 + msg3 + msg4 + msg5
        
        state.set_memory({
            'submittedTwitterLink' : False,
            'setLogo' : False,
            'RetweetedPost' : False,
            'completedAllTasks' : False,
        })

        bot.sendMessage(update.get_chat().get_id(), msg)
    else:
        msg = "Hello " + username + ", welcome to Farm Finance.Click  /start  to get started."
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
        reply = 'Here are the available actions.\n\n1.Send /account for account info.\n2.Send /withdraw  to request for withdrawal.'
        bot.sendMessage(update.get_chat().get_id(), reply )

    elif command == '/account':
        info = ""
        if state.get_memory()['completedAllTasks'] is True:
            info = "You have  been verified for withdrawal"
        else:
            info = "You have not been verified for withdrawal"
        reply = 'Here is your account info\n\nWithdrawal status : ' + info
        bot.sendMessage(update.get_chat().get_id(), reply )

    elif command == '/withdraw':
        if state.get_memory()['completedAllTasks'] is True:
            msg = "Congratulations! You have been verified for withdrawal.\n\nEnter your FAFI token wallet address below."
            state.set_name('waiting_for_wallet_address')
            bot.sendMessage(update.get_chat().get_id(), msg )
        else:

            reply = 'You have  not  been verified for withdrawal by the admins.Please make sure you have completed all tasks, then try again later.Thank you.'
            bot.sendMessage(update.get_chat().get_id(), reply )
            raise ProcessFailure
    
    elif command == '/procedures':
        reply = "Follow  the following procedures to receive your airdrop.\n\n"
        msg1 = "Complete the tasks below to get up to $50 FAFI token.\n\n"
        msg2 = '1. Join our telegram group at http://t.me/farmfinancebsc/\n2. Join our telegram channel at http://t.me/farmfinanceupdates/.\n'
        msg3 = '3. Follow our twitter account at http://twitter.com/farm_financeBsc/\n4. Like and retweet our pinned tweet about the airdrop on twitter.\n '
        msg4 = '5. Use our FarmFinance logo as your profile picture on telegram and twitter.'
        reply += msg1 + msg2 + msg3 + msg4
        bot.sendMessage(update.get_chat().get_id(),  reply )
    


