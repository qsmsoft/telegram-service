import asyncio
import os

from telethon import TelegramClient, events

from app.core.config import API_ID, API_HASH
from app.db.session import engine, Base, get_db
from app.models.message import Message

# Initialize database
Base.metadata.create_all(bind=engine)

# Initialize Telegram client
client = TelegramClient('userbot', int(API_ID), API_HASH)


@client.on(events.NewMessage())
async def handle_new_message(event):
    sender = await event.get_sender()
    receiver = await event.get_chat() if event.is_private else await event.get_input_chat()

    sender_id = sender.id
    sender_name = sender.username or sender.first_name

    receiver_id = receiver.id
    receiver_name = receiver.username or receiver.title

    if sender_id == receiver_id:
        receiver_id = (await client.get_me()).id
        receiver_name = (await client.get_me()).username or (await client.get_me()).first_name

    content = event.raw_text if event.raw_text else None
    voice_file_path = None

    # Check if the message contains a voice message
    if event.voice:
        file_name = f"voice_{event.id}.ogg"
        voice_file_path = os.path.join('../voice_messages', file_name)
        await event.download_media(voice_file_path)

    # Save message to the database
    db = next(get_db())
    new_message = Message(
        sender_id=sender_id,
        sender_name=sender_name,
        receiver_id=receiver_id,
        receiver_name=receiver_name,
        content=content,
        voice_file_path=voice_file_path,
        message_id=event.message.id
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    print(f"Message from {sender_name} to {receiver_name}: {event.raw_text}")


@client.on(events.MessageEdited())
async def handle_edited_message(event):
    sender = await event.get_sender()
    receiver = await event.get_chat() if event.is_private else await event.get_input_chat()
    message_id = event.message.id

    sender_id = sender.id
    sender_name = sender.username or sender.first_name

    receiver_id = receiver.id
    receiver_name = receiver.username or receiver.title

    if sender_id == receiver_id:
        receiver_id = (await client.get_me()).id
        receiver_name = (await client.get_me()).username or (await client.get_me()).first_name

    # Update message in the database
    db = next(get_db())
    edited_message = db.query(Message).filter_by(
        sender_id=sender_id,
        receiver_id=receiver_id,
        message_id=message_id,
    ).first()
    edited_message.content = event.raw_text
    db.commit()

    print(f"Edited message from {sender_name} to {receiver_name}: {event.raw_text}")


async def send_message(receiver_id, message_text):
    await client.send_message(receiver_id, message_text)

    # Get sender info (client info)
    me = await client.get_me()
    sender_id = me.id
    sender_name = me.username or me.first_name

    # Save sent message to the database
    db = next(get_db())
    new_message = Message(
        sender_id=sender_id,
        sender_name=sender_name,
        receiver_id=receiver_id,
        receiver_name='Chat' if not isinstance(receiver_id, int) else f'User {receiver_id}',
        content=message_text
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    print(f"Sent message to {receiver_id}: {message_text}")


async def run_client(api_id, api_hash, phone_number, session_name):
    async with TelegramClient(session_name, api_id, api_hash) as client:
        await client.start(phone=phone_number)
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            code = input(f'Enter the code for {session_name}: ')
            await client.sign_in(phone_number, code)

        # Get client's own ID and username
        me = await client.get_me()
        client_id = me.id
        client_username = me.username or me.first_name
        print(f"Client ID for {session_name}: {client_id}")
        print(f"Client Username for {session_name}: {client_username}")

        # Add event handler
        client.add_event_handler(handle_new_message, events.NewMessage())

        # Send a test message
        await send_message(5651362280, 'test message from server')

        print(f"Client {session_name} is running...")
        await client.run_until_disconnected()


async def add_new_session(sessions):
    api_id = input('Enter API ID: ')
    api_hash = input('Enter API Hash: ')
    phone_number = input('Enter Phone Number: ')
    session_name = input('Enter Session Name: ')

    session_task = run_client(api_id, api_hash, phone_number, session_name)
    sessions.append(session_task)
    await asyncio.gather(*sessions)
