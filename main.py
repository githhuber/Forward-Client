import os
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from configs import Config
from helpers.kanger import Kanger
from helpers.forwarder import ForwardMessage

RUN = {"isRunning": True}
User = Client(
    "pyrogram",
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    in_memory=True,
    session_string=Config.STRING_SESSION
)

@User.on_message((filters.text | filters.media))
async def main(client: Client, message: Message):
    if (-100 in Config.FORWARD_TO_CHAT_ID) or (-100 in Config.FORWARD_FROM_CHAT_ID):
        try:
            await client.send_message(
                chat_id="me",
                text="#VARS_MISSING: Please Set FORWARD_FROM_CHAT_ID or FORWARD_TO_CHAT_ID Config!"
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
        return
    if message.text == "!start" and message.from_user.is_self:
        if not RUN["isRunning"]:
            RUN["isRunning"] = True
        await message.edit_text(
            text=f"Hi, {(await client.get_me()).first_name}!\nThis is a Forwarder Userbot by @AbirHasan2005",
            disable_web_page_preview=True
        )
    elif message.text == "!stop" and message.from_user.is_self:
        RUN["isRunning"] = False
        await message.edit_text("Userbot Stopped!\n\nSend !start to start userbot again.")
    elif message.text == "!help" and message.from_user.is_self and RUN["isRunning"]:
        await message.edit_text(
            text=Config.HELP_TEXT,
            disable_web_page_preview=True
        )
    elif message.text and message.text.startswith("!add_forward_") and message.from_user.is_self and RUN["isRunning"]:
        if len(message.text.split(" ", 1)) < 2:
            return await message.edit(f"{message.text} chat_id")
        for x in message.text.split(" ", 1)[-1].split(" "):
            if x.isdigit() and message.text.startswith("!add_forward_to_chat"):
                Config.FORWARD_TO_CHAT_ID.append(int(x))
            elif x.isdigit() and message.text.startswith("!add_forward_from_chat"):
                Config.FORWARD_FROM_CHAT_ID.append(int(x))
            elif x.lower().startswith("all_joined_"):
                chat_ids = []
                if x.lower() == "all_joined_groups":
                    await message.edit("Listing all joined groups ...")
                    async for dialog in client.iter_dialogs():
                        chat = dialog.chat
                        if chat and (chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]):
                            chat_ids.append(chat.id)
                if x.lower() == "all_joined_channels":
                    await message.edit("Listing all joined channels ...")
                    async for dialog in client.iter_dialogs():
                        chat = dialog.chat
                        if chat and (chat.type == enums.ChatType.CHANNEL):
                            chat_ids.append(chat.id)
                if not chat_ids:
                    return await message.edit("No Chats Found !!")
                for chat_id in chat_ids:
                    if chat_id not in Config.FORWARD_TO_CHAT_ID:
                        Config.FORWARD_TO_CHAT_ID.append(chat_id)
            else:
                pass
        return await message.edit("Added Successfully!")
    elif message.text and message.text.startswith("!remove_forward_") and message.from_user.is_self and RUN["isRunning"]:
        if len(message.text.split(" ", 1)) < 2:
            return await message.edit(f"{message.text} chat_id")
        for x in message.text.split(" ", 1)[-1].split(" "):
            try:
                if x.isdigit() and message.text.startswith("!remove_forward_to_chat"):
                    Config.FORWARD_TO_CHAT_ID.remove(int(x))
                elif x.isdigit() and message.text.startswith("!remove_forward_from_chat"):
                    Config.FORWARD_FROM_CHAT_ID.remove(int(x))
                else:
                    pass
            except ValueError:
                pass
        return await message.edit("Removed Successfully!")

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8080))
    User.run(port=port, workers=4)