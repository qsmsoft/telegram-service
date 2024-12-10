import asyncio
import os

from sqlalchemy.future import select
from telethon import events

from app.db.session import get_db, telegram_client_connection
from app.models.message_model import Message
from app.services.account_service import get_all_active_accounts

clients = []


async def save_message(db, sender_id, sender_name, receiver_id, receiver_name, content, message_id,
                       voice_file_path=None):
    async with db.begin():
        new_message = Message(
            sender_id=sender_id,
            sender_name=sender_name,
            receiver_id=receiver_id,
            receiver_name=receiver_name,
            content=content,
            voice_file_path=voice_file_path,
            message_id=message_id
        )
        db.add(new_message)
    await db.commit()
    await db.refresh(new_message)


def register_handlers(client):
    @client.on(events.NewMessage())
    async def handle_new_message(event):
        sender = await event.get_sender()
        receiver = await event.get_chat() if event.is_private else await event.get_input_chat()

        sender_id = sender.id
        sender_name = sender.username or sender.first_name

        receiver_id = receiver.id
        receiver_name = receiver.username or receiver.first_name

        if sender_id == receiver_id:
            me = await client.get_me()
            receiver_id = me.id
            receiver_name = me.username or me.first_name

        content = event.raw_text if event.raw_text else None
        voice_file_path = None

        if event.voice:
            file_name = f"voice_{event.id}.ogg"
            voice_file_path = os.path.join('../voice_messages', file_name)
            await event.download_media(voice_file_path)

        async  with get_db() as db:
            await save_message(db, sender_id, sender_name, receiver_id, receiver_name, content, event.message.id,
                               voice_file_path)

        print(f"Message from {sender_name} to {receiver_name}: {event.raw_text}")

    @client.on(events.MessageEdited())
    async def handle_edited_message(event):
        sender = await event.get_sender()
        receiver = await event.get_chat() if event.is_private else await event.get_input_chat()

        sender_id = sender.id
        sender_name = sender.username or sender.first_name

        receiver_id = receiver.id
        receiver_name = receiver.username or receiver.title

        async with get_db() as db:
            result = await db.execute(select(Message).filter_by(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message_id=event.message.id,
            ))

            edited_message = result.scalars().first()

            if edited_message:
                edited_message.content = event.raw_text
                await db.commit()

        print(f"Edited message from {sender_name} to {receiver_name}: {event.raw_text}")

    async def send_message(receiver_id, message_text):
        await client.send_message(receiver_id, message_text)

        # Get sender info (client info)
        me = await client.get_me()
        sender_id = me.id
        sender_name = me.username or me.first_name

        # Save sent message to the database
        async with get_db() as db:
            async with db.begin():
                new_message = Message(
                    sender_id=sender_id,
                    sender_name=sender_name,
                    receiver_id=receiver_id,
                    receiver_name='Chat' if not isinstance(receiver_id, int) else f'User {receiver_id}',
                    content=message_text
                )
                db.add(new_message)
            await db.commit()
            await db.refresh(new_message)

        print(f"Sent message to {receiver_id}: {message_text}")


async def start_client(session_name: str, api_id: int, api_hash: str):
    client = telegram_client_connection(session_name, api_id, api_hash)
    register_handlers(client)

    await client.connect()


async def run_multiple_clients():
    clients_info = await get_all_active_accounts()

    global clients

    tasks = []

    for client_info in clients_info:
        task = asyncio.create_task(start_client(
            client_info.session_name,
            client_info.api_id,
            client_info.api_hash
        ))
        tasks.append(task)

    clients = await asyncio.gather(*tasks)
