
import os
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from configs import Config

RUN = {"isRunning": True}
User = Client(
    "pyrogram",
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    session_name=Config.STRING_SESSION
)


@User.on_message((filters.text | filters.media) & filters.me)
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
    if message.text == "!start":
        if not RUN["isRunning"]:
            RUN["isRunning"] = True
        await message.edit_text(
            text=f"Hi, {(await client.get_me()).first_name}!\nThis is a Forwarder Userbot by @AbirHasan2005",
            disable_web_page_preview=True
        )
    elif message.text == "!stop" and RUN["isRunning"]:
        RUN["isRunning"] = False
        return await message.edit_text("Userbot Stopped!\n\nSend !start to start userbot again.")
    elif message.text == "!help" and RUN["isRunning"]:
        await message.edit_text(
            text=Config.HELP_TEXT,
            disable_web_page_preview=True
        )
    elif message.text and message.text.startswith("!add_forward_") and RUN["isRunning"]:
        if len(message.text.split(" ", 1)) < 2:
            return await message.edit_text(f"{message.text} chat_id")
        for x in message.text.split(" ", 1)[-1].split(" "):
            if x.isdigit() and message.text.startswith("!add_forward_to_chat"):
                Config.FORWARD_TO_CHAT_ID.append(int(x))
            elif x.isdigit() and message.text.startswith("!add_forward_from_chat"):
                Config.FORWARD_FROM_CHAT_ID.append(int(x))
            elif x.lower().startswith("all_joined_"):
                chat_ids = []
                if x.lower() == "all_joined_groups":
                    await message.edit_text("Listing all joined groups ...")
                    async for dialog in client.iter_dialogs():
                        chat = dialog.chat
                        if chat and (chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]):
                            chat_ids.append(chat.id)
                elif x.lower() == "all_joined_channels":
                    await message.edit_text("Listing all joined channels ...")
                    async for dialog in client.iter_dialogs():
                        chat = dialog.chat
                        if chat and (chat.type == enums.ChatType.CHANNEL):
                            chat_ids.append(chat.id)
                if not chat_ids:
                    return await message.edit_text("No Chats Found!")
                for chat_id in chat_ids:
                    if chat_id not in Config.FORWARD_TO_CHAT_ID:
                        Config.FORWARD_TO_CHAT_ID.append(chat_id)
            else:
                pass
        return await message.edit_text("Added Successfully!")
    elif message.text and message.text.startswith("!remove_forward_") and RUN["isRunning"]:
        if len(message.text.split(" ", 1)) < 2:
            return await message.edit_text(f"{message.text} chat_id")
        for x in message.text.split(" ", 1)[-1].split(" "):
            if x.isdigit() and message.text.startswith("!remove_forward_to_chat"):
                Config.FORWARD_TO_CHAT_ID.remove(int(x))
            elif x.isdigit() and message.text.startswith("!remove_forward_from_chat"):
                Config.FORWARD_FROM_CHAT_ID.remove(int(x))
            else:
                pass
        return await message.edit_text("Removed Successfully!")


def run_userbot():
    User.run()


if __name__ == "__main__":
    run_userbot()