from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio
import getpass

async def analyze_telegram_channel():
    api_id = 'PASTE'
    api_hash = 'PASTE'
    channel_username = '@'

    client = TelegramClient('my_session', api_id, api_hash)
    
    try:
        await client.start(
            phone=lambda: input("Введите номер телефона (+...): "),
            code_callback=lambda: input("Код из Telegram: "),
            password=lambda: getpass.getpass("Пароль 2FA (если есть): ")
        )
        
        # Исправленный запрос GetHistoryRequest
        all_messages = []
        total_views = 0
        total_messages = 0
        max_views = 0
        max_views_date = None
        offset_id = 0

        while True:
            history = await client(GetHistoryRequest(
                peer=channel_username,
                offset_id=offset_id,
                offset_date=None,    # Добавлено
                add_offset=0,        # Добавлено
                limit=100,
                max_id=0,
                min_id=0,
                hash=0
            ))
            
            if not history.messages:
                break

            for msg in history.messages:
                if hasattr(msg, 'views') and msg.views:
                    if msg.views > max_views:
                        max_views = msg.views
                        max_views_date = msg.date
                    total_views += msg.views
                    total_messages += 1

            all_messages.extend(history.messages)
            offset_id = history.messages[-1].id if history.messages else 0

        # Остальной код остается без изменений
        if not all_messages:
            print("Канал пуст.")
            return

        first_msg = all_messages[-1]
        first_views = getattr(first_msg, 'views', 'N/A')

        avg_views = total_views / total_messages if total_messages else 0

        last_msg = all_messages[0]
        last_views = getattr(last_msg, 'views', 'N/A')

        print(f"1. Просмотров первого сообщения: {first_views}")
        print(f"2. Максимум: {max_views} ({max_views_date})")
        print(f"3. Среднее: {avg_views:.1f}")
        print(f"4. Просмотров последнего: {last_views}")

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await client.disconnect()

asyncio.run(analyze_telegram_channel())
