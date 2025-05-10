from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError, RPCError
import asyncio

# ← Вставьте вашу StringSession здесь (генерируется один раз)
SESSION = '1ApWapzMBu7G3YntF3mL9cFAyTBtvxvWgfqTQJgJwccZHtirfzhVxTh4R3H08KFsAtIbhqnLVJpzwaAJqp6Hvd1049BXKO_cHyJyKNDdKc9LrtmVdyTtM4gc8zCWq-_BXAIni6wCHL0D3TUuDRR3hUV_PLvs_W0hr5XI-2ZyK0W1IJa-8TSn971St8mBij1XYTspQq3g89uRc7byUztbBqISc9zuHaAlpI4Wj3Kw9luLWXDZIpG2q62HveTmLzz5iNJGdCs1JN3xdxG1uSKqAKjfIMm84Q73bCjugYQVMJ49ONmyiHXIbpxFXwyPly73aziwWbXPcVB7rm0waXgO0rfnhtMVw5b8='
API_ID, API_HASH = 23459666, '2fede010ea846fa23ceea24bcd59ee02'
TARGET_USER = -1002464920043
KEYWORDS = ['розыгрыш', 'итоги', 'конкурс', 'победитель']

# Указываем параметры устройства, чтобы избежать подозрений Telegram
client = TelegramClient(
    StringSession(SESSION), API_ID, API_HASH,
    device_model='iPhone 13 Pro Max',
    system_version='14.4',
    app_version='7.8.0',
    lang_code='ru',
    system_lang_code='ru',
    auto_reconnect=True,
    connection_retries=None,
    retry_delay=5,
    sequential_updates=True,
    flood_sleep_threshold=120
)

@client.on(events.NewMessage)
async def handler(event):
    text = event.raw_text.lower()
    if any(kw in text for kw in KEYWORDS):
        try:
            await client.forward_messages(TARGET_USER, event.message)
        except FloodWaitError as e:
            print(f"FloodWait: жду {e.seconds}s") 
            await asyncio.sleep(e.seconds)
        except RPCError as e:
            print(f"RPCError: {e}, переподключаюсь…") 
            await client.disconnect()
            await client.connect()

async def main():
    await client.start()         # Без запроса кода после первого раза
    await client.catch_up()      # Догоняем офлайн-апдейты
    print("Бот запущен") 
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
