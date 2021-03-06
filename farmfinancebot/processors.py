from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.exceptions import ProcessFailure
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot

valid_commands = [
    '/Continue',
    '/Account',
    '/Proceed',
    # '/Procedures',
    # '/Withdraw',
    '/Next'
    

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

# msg2 = "\U00002744 Join our telegram <a href = 'http://t.me/farmfinancebsc/'> group </a> and  <a href = 'http://t.me/farmfinanceupdates/'> channel </a>.\n\n"
#         msg3 = "\U00002744 Follow us on <a href = 'http://twitter.com/farm_financeBsc/'> twitter </a>, like and retweet the pinned post about our airdrop.\n\n "
#         msg4 = '\U00002744 Once done, click on /proceed\n'
#         msg5 = '\n\nClick /menu for a list of other available options.'


# Start Command acceptor
@processor(
    state_manager,
    from_states=state_types.Reset,
    update_types=[update_types.EditedMessage, update_types.Message],
    message_types=message_types.Text,
    success='command_mode',
    fail=state_types.Keep,
)
def start(bot: TelegramBot, update: Update, state: TelegramState):
    chat_msg = str(update.get_message().get_text())
    username = state.telegram_user.first_name.capitalize()
    if chat_msg == '/Start' or chat_msg == '/start':
        msg1 = "Hello " + username + " \U000026C4 , I am your friendly Farm Finance Airdrop bot.\n\nPlease do the required tasks to get up to $100 FAFI token.\n\n\U00002744 1 FAFI = 1 USD\n\nFor joining the Airdrop and completing the task, you automatically qualify for our Airdrop tokens.\n\n "
        msg0 = '\U00002744 No referrals needed \n\n\nClick /Proceed to continue'
        
        msg = msg1 + msg0 

        state.set_memory({
            'submittedTwitterLink': False,
            'setLogo': False,
            'RetweetedPost': False,
            'completedAllTasks': False,
        })

        bot.sendMessage(update.get_chat().get_id(), msg, parse_mode=TelegramBot.PARSE_MODE_HTML, )
    else:
        msg = "Hello " + username + \
            " \U000026C4 , welcome to Farm Finance.Click  /Start  to get started."
        bot.sendMessage(update.get_chat().get_id(), msg)
        raise ProcessFailure


# Procedures Acceptor
@processor(
    state_manager,
    from_states= [ 'asked_for_telegram_join', 'command_mode','asked_for_twitter_join'],
    update_types=[update_types.EditedMessage, update_types.Message],
    message_types=message_types.Text,
    # success= 'waiting_for_wallet_address',
    fail=state_types.Keep,

)
def command_processor(bot, update, state):
    chat_msg = str(update.get_message().get_text())
    username = state.telegram_user.first_name.capitalize()

    command = chat_msg

    if command == '/Continue':
        key = state.get_memory().get('saidHi', None)
        if key is None:
            state.update_memory({
                'saidHi' : True
            })
            msg = "\U00002744 Send 'Hi' to the <a href = 'http://t.me/farmfinancebsc/'> group chat </a>\n\nOnce done, click /Continue"
            bot.sendMessage(update.get_chat().get_id(), msg, parse_mode=TelegramBot.PARSE_MODE_HTML )
            raise ProcessFailure

        if state.name == "asked_for_telegram_join":
            msg1 = "\U00002744 Follow us on <a href = 'http://twitter.com/farm_financeBsc/'> twitter </a>, like and retweet the pinned post about our airdrop.\n\n "
            msg2 = "\n\n Once done, click /Next "
            msg = msg1 + msg2
            state.set_name('asked_for_twitter_join')
            bot.sendMessage(update.get_chat().get_id(), msg, parse_mode=TelegramBot.PARSE_MODE_HTML )
        else:
            msg = "\U00002744 Please join telegram our group and channel before proceeding."
            bot.sendMessage(update.get_chat().get_id(), msg)
            raise ProcessFailure

    if command == '/Account':
        info = ""
        if state.get_memory()['completedAllTasks'] is True:
            info = "You have  been verified for withdrawal \U00002714"
        else:
            info = "You are not yet eligible for withdrawal \U0000274c"

        reply = 'Here is your account info\n\nWithdrawal status : ' + info
        bot.sendMessage(update.get_chat().get_id(), reply)

    elif command == '/Next':
        key = state.get_memory().get('warned',None)
        if key :
            msg = "\U00002744 Enter your Bep20 Binance smartchain address(ex. Trust Wallet, Metamask, etc, exchange wallets not applicable for airdrop)."
            state.set_name('waiting_for_wallet_address')
            
            bot.sendMessage(update.get_chat().get_id(), msg )
        else:
            msg = "	\U00002757 Please ensure you have completed all tasks or you won't be eligible for the Airdrop.\n\nCheck again and click /Next to continue"
            state.update_memory({
                'warned' : True
            })
            bot.sendMessage(update.get_chat().get_id(), msg)
            raise ProcessFailure

    elif command == '/Proceed':
        msg1 = "\U00002744 Join our telegram <a href = 'http://t.me/farmfinancebsc/'> group </a> and  <a href = 'http://t.me/farmfinanceupdates/'> channel </a>.\n\n "
        msg2 = " Once done, click /Continue"
        msg = msg1 + msg2
        state.set_name('asked_for_telegram_join')
        
        bot.sendMessage(update.get_chat().get_id(), msg, parse_mode=TelegramBot.PARSE_MODE_HTML)
        # state.set_name('waiting_for_wallet_address')
        # else:

        #     reply = 'You are not yet eligible for withdrawal \U0000274c Please make sure you have completed all tasks, then try again later.Thank you.'
        #     bot.sendMessage(update.get_chat().get_id(), reply )
        #     raise ProcessFailure

    elif command == '/Procedures':
        reply = "Follow  the following procedures to receive your airdrop.\n\n"
        msg1 = "Complete the tasks below to get up to $100 FAFI token.\n\n"
        msg2 = "\U00002744 Join our telegram <a href = 'http://t.me/farmfinancebsc/'> group </a> and <a href = 'http://t.me/farmfinanceupdates/'> channel </a>.\n\n"
        msg3 = "\U00002744 Follow us on <a href = 'http://twitter.com/farm_financeBsc/'> twitter </a>, like and retweet the pinned tweet about our airdrop.\n\n "
        msg4 = '\U00002744 Once done, click on /proceed\n'
        reply += msg1 + msg2 + msg3 + msg4
        bot.sendMessage(update.get_chat().get_id(),  reply,
                        parse_mode=TelegramBot.PARSE_MODE_HTML)

    elif not(chat_msg in valid_commands):
        msg = ' \U0000203C You are a user of the this bot already.Please continue from where you last stopped \U0000203C'
        bot.sendMessage(update.get_chat().get_id(), msg)
        raise ProcessFailure


#  wallet Acceptor
@processor(
    state_manager,
    from_states='waiting_for_wallet_address',
    update_types=[update_types.EditedMessage, update_types.Message],
    message_types=message_types.Text,
    success='waiting_for_twitter_username',
    fail=state_types.Keep,

)
def wallet_processor(bot, update, state):
    addr = str(update.get_message().get_text())
    if not( len(addr) == 42 ) or not(addr.isalnum()):
        msg = "\U0000274c Please enter a valid wallet address"
        bot.sendMessage(update.get_chat().get_id(), msg)
        raise ProcessFailure
    else:
        msg = "\U00002744 Enter your twitter username(ex. @drake)"
        # state.set_name('waiting_for_twitter_username')
        state.set_memory({
            'Wallet Address': addr,
            'completedAllTasks': state.get_memory()['completedAllTasks'],
        })
        bot.sendMessage(update.get_chat().get_id(), msg)


#  Twitter uanme Acceptor
@processor(
    state_manager,
    from_states='waiting_for_twitter_username',
    update_types=[update_types.EditedMessage, update_types.Message],
    message_types=message_types.Text,
    # success=  'submitted_twitter_name',
    fail=state_types.Keep,

)
def twitter_username_processor(bot, update, state):
    uname = str(update.get_message().get_text())
    if len(uname) > 25 or uname.isdigit() or  not (uname[0] == '@'):
        msg = "\U0000274c Please enter a valid twitter username( ex. @jack23 )"
        bot.sendMessage(update.get_chat().get_id(), msg)
        raise ProcessFailure
    else:
        msg1 = "	\U00002728 Congratulations! You have successfully completed the tasks for the FAFI Airdrop campaign.\n\n"
        msg2 = "Tokens will be automatically distributed to the submitted wallet address at the end of the Airdrop campaign when it is time for distribution. "
        msg = msg1 + msg2
        state.set_name('submitted_twitter_name')
        state.set_memory({
            'Twitter Username':  uname,
            'completedAllTasks': state.get_memory()['completedAllTasks'],
            'Wallet Address': state.get_memory()['Wallet Address'],
        })
        bot.sendMessage(update.get_chat().get_id(), msg)




# #   User Joined Acceptor
# @processor(
#     state_manager,
#     from_states= 'asked_for_telegram_join',
#     update_types= [ update_types.Message, update_types.ChannelPost, ],
#     message_types = [ message_types.NewChatMembers, message_types.Text ],
#     # success=  'submitted_twitter_name',
#     fail=state_types.Keep,

# )
# def joined_processor(bot, update, state):
#     state.update_memory({
#         'joinedGroup' : True
#     })
#     bot.sendMessage(update.get_chat().get_id(), "Welcome to our group")
