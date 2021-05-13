from telethon import TelegramClient, events, Button
import telethon.sync
import socks
import asyncio
import html
import os

# replace the credentials with your own
API_ID = "API_ID" in os.environ and os.environ["API_ID"] or 1234567
API_HASH = "API_HASH" in os.environ and os.environ["API_HASH"] or 'yourhash'
BOT_TOKEN = "BOT_TOKEN" in os.environ and os.environ[
    "BOT_TOKEN"] or 'yourbottoken'
CHAT_ID = "CHAT_ID" in os.environ and os.environ["CHAT_ID"] or 'chatid'
ADMIN_ID = "ADMIN_ID" in os.environ and os.environ["ADMIN_ID"] or 'adminid'

# https://docs.telethon.dev/en/latest/basic/signing-in.html
api_id = str(API_ID)
api_hash = API_HASH
bot_token = BOT_TOKEN

proxy = None

chat_id = int(CHAT_ID)
admin_id = int(ADMIN_ID)

welcome_message = 'test welcome message'

# keep track of user profile of the group chat
user_profile = {}


@events.register(events.CallbackQuery)
async def bot_callback_handler(event):
    if event.data:
        print('test bot_callback_handler: ', event.data)


@events.register(events.NewMessage)
async def bot_message_handler(event):
    if event.raw_text.startswith('/start'):
        await event.respond(welcome_message, parse_mode='markdown')
    elif event.raw_text.startswith('/debug'):
        # do nothing for debugging for now
        pass
    elif event.chat_id == chat_id:
        message = event.message
        #print(message.id, message.from_id, message.post_author, message.date, message.raw_text.strip())
        history_meta = '[META] {} {} {}\n'.format(
            message.id, user_profile[message.from_id]['username'], message.date)
        history = '[MESSAGE] ' + message.raw_text.strip()
        print(history_meta, history)
        lock = asyncio.Lock()
        async with lock:
            with open('logs/log-{}-{}-{}.txt'.format(str(message.date.year), str(message.date.month), str(message.date.day)), mode='a+', encoding='utf-8') as f:
                f.write(history_meta)
                f.write(history + '\n')
                f.close()
    else:
        # more support could be implemented in the future
        pass

loop = asyncio.get_event_loop()

print('initializing client...')

client = TelegramClient('session/client', api_id, api_hash,
                        connection_retries=None, proxy=proxy, loop=loop)
client.start()

print('client successfully initilialized!')

print('initializing bot...')

bot = TelegramClient('session/bot', api_id, api_hash,
                     connection_retries=None, proxy=proxy, loop=loop)
bot.add_event_handler(bot_message_handler)
bot.add_event_handler(bot_callback_handler)
bot.start(bot_token=bot_token)

print('bot successfully initialized!')

print('initializing user info...')
for user in client.iter_participants(chat_id):
    #print(user.id, user.first_name, user.last_name, user.username, user.bot)
    user_profile[user.id] = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'is_bot': user.bot
    }
print('user info successfully initialized!')

try:
    loop.run_forever()
except KeyboardInterrupt:
    client.disconnect()
    print('bot stopped!')
