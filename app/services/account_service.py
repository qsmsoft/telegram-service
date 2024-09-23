# Initialize Telegram client
import asyncio

from sqlalchemy.orm import Session
from telethon import TelegramClient

from app.core.config import API_ID, API_HASH
from app.models.account import Account

client = TelegramClient('userbot', int(API_ID), API_HASH)


async def run_client(api_id, api_hash, phone_number, session_name):
    async with TelegramClient(session_name, api_id, api_hash) as client:
        await client.start(phone=phone_number)
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            code = input(f'Enter the code for {session_name}: ')
            await client.sign_in(phone_number, code)

        # # Get client's own ID and username
        # me = await client.get_me()
        # client_id = me.id
        # client_username = me.username or me.first_name
        # print(f"Client ID for {session_name}: {client_id}")
        # print(f"Client Username for {session_name}: {client_username}")

        await client.run_until_disconnected()


async def add_new_session(db: Session, account_id: int, sessions):
    account = db.query(Account).filter(Account.id == account_id).first()

    session_task = run_client(account.api_id, account.api_hash, account.phone_number, account.session_name)
    sessions.append(session_task)
    await asyncio.gather(*sessions)


