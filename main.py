import os
import asyncio
from pyrogram import Client, filters, types
from configs import Config
from flask import Flask

# Initialize Flask
app = Flask(__name__)

# Initialize Pyrogram Client
RUN = {"isRunning": True}
User = Client(
    "pyrogram",
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    in_memory=True,
    session_string=Config.STRING_SESSION
)

@User.on_message(filters.me & (filters.text | filters.media))
async def main(client: Client, message: types.Message):
    if (-100 in Config.FORWARD_TO_CHAT_ID) or (-100 in Config.FORWARD_FROM_CHAT_ID):
        try:
            await client.send_message(
                chat_id=message.chat.id,
                text="#VARS_MISSING: Please Set FORWARD_FROM_CHAT_ID or FORWARD_TO_CHAT_ID Config!"
            )
        except asyncio.TimeoutError:
            pass
        return

    if message.text == "!start":
        if not RUN["isRunning"]:
            RUN["isRunning"] = True
        await message.edit_text(
            text=f"Hi, {(await client.get_me()).first_name}!\nThis is a Forwarder Userbot by @AbirHasan2005",
            disable_web_page_preview=True
        )

    elif message.text == "!stop":
        RUN["isRunning"] = False
        await message.edit_text("Userbot Stopped!\n\nSend !start to start the userbot again.")

    elif message.text == "!help" and RUN["isRunning"]:
        await message.edit_text(
            text=Config.HELP_TEXT,
            disable_web_page_preview=True
        )

    elif message.text and message.text.startswith("!add_forward_") and RUN["isRunning"]:
        if len(message.text.split(" ", 1)) < 2:
            return await message.edit(f"{message.text} chat_id")
        
        for x in message.text.split(" ", 1)[-1].split(" "):
            try:
                chat_id = int(x)
                if message.text.startswith("!add_forward_to_chat"):
                    Config.FORWARD_TO_CHAT_ID.append(chat_id)
                elif message.text.startswith("!add_forward_from_chat"):
                    Config.FORWARD_FROM_CHAT_ID.append(chat_id)
            except ValueError:
                pass

        return await message.edit_text("Added Successfully!")

    elif message.text and message.text.startswith("!remove_forward_") and RUN["isRunning"]:
        if len(message.text.split(" ", 1)) < 2:
            return await message.edit(f"{message.text} chat_id")
        
        for x in message.text.split(" ", 1)[-1].split(" "):
            try:
                chat_id = int(x)
                if message.text.startswith("!remove_forward_to_chat"):
                    Config.FORWARD_TO_CHAT_ID.remove(chat_id)
                elif message.text.startswith("!remove_forward_from_chat"):
                    Config.FORWARD_FROM_CHAT_ID.remove(chat_id)
            except ValueError:
                pass

        return await message.edit_text("Removed Successfully!")

# Use a dynamic port for Flask based on environment variable or default to 8080
PORT = int(os.environ.get("PORT", 8080))

@app.route('/')
def hello_world():
    return 'Hello, this is your Pyrogram UserBot!'

if __name__ == "__main__":
    User.start()
    app.run(host='0.0.0.0', port=PORT)