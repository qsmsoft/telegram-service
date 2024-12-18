# from fastapi import APIRouter, Depends, HTTPException, Body
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.crud import accounts as crud_client
# from app.crud.accounts import get_account_info, get_account, get_account_by_phone
# from app.db.config import get_db
# from app.models.account_model import Account
# from app.schemas.account_schema import AccountCreate
# from app.services.account_service import status_changed
#
# router = APIRouter()
#
#
# @router.post("/")
# async def create_client(client_info: AccountCreate, session: AsyncSession = Depends(get_db)):
#     if await get_account_by_phone(session, client_info.phone_number):
#         raise HTTPException(status_code=400, detail="Client already exists.")
#     return await crud_client.create_account(account_info=client_info)
#
#
# @router.post("/connect/{session_name}")
# async def connect(session_name: str):
#     client_info = await get_account_info(session_name)
#
#     try:
#         client = await get_account(client_info)
#         if not await client.is_user_authorized():
#             return {"message": "Session expired. Re-login required."}
#         return {"message": "Connected using previous session!"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# @router.post("/send_code/{session_name}")
# async def send_code(session_name: str):
#     client_info = await get_account_info(session_name)
#
#     try:
#         client = await get_account(client_info)
#         if not await client.is_user_authorized():
#             sent_code = await client.send_code_request(client_info.phone_number)
#             async with get_db() as session:
#                 result = await session.execute(select(Account).filter_by(session_name=session_name))
#                 client_info = result.scalar_one_or_none()
#
#                 client_info.phone_code_hash = sent_code.phone_code_hash
#
#                 session.add(client_info)
#                 await session.commit()
#
#             return {"message": "Verification code sent to your phone."}
#         return {"message": "Already authorized."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# @router.post("/login/{session_name}")
# async def login(session_name: str, code: str = Body(..., embed=True)):
#     client_info = await get_account_info(session_name)
#
#     try:
#         client = await get_account(client_info)
#         if not await client.is_user_authorized():
#             await client.sign_in(client_info.phone_number, code, phone_code_hash=client_info.phone_code_hash)
#             await status_changed(client_info.phone_number)
#             return {"message": "Successfully logged in!"}
#         return {"message": "Already logged in."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# @router.post("/disconnect/{session_name}")
# async def disconnect(session_name: str):
#     client_info = await get_account_info(session_name)
#
#     try:
#         client = await get_account(client_info)
#         if client.is_connected():
#             await client.disconnected
#         return {"message": f"Disconnected from Telegram session {session_name}!"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# @router.get("/status/{session_name}")
# async def status(session_name: str):
#     client_info = await get_account_info(session_name)
#
#     try:
#         client = await get_account(client_info)
#         is_connected = client.is_connected()
#         return {"connected": is_connected}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# @router.get("/logout/{session_name}")
# async def logout(session_name: str):
#     client_info = await get_account_info(session_name)
#
#     client = await get_account(client_info)
#     await client.log_out()
#     await status_changed(client_info.phone_number)
#
#     return {"status": f"Logged out of {client_info.session_name}"}
