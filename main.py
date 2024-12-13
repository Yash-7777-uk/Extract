#  MIT License

#

#  Copyright (c) 2019-present Dan <https://github.com/delivrance>

#

#  Permission is hereby granted, free of charge, to any person obtaining a copy

#  of this software and associated documentation files (the "Software"), to deal

#  in the Software without restriction, including without limitation the rights

#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell

#  copies of the Software, and to permit persons to whom the Software is

#  furnished to do so, subject to the following conditions:

#

#  The above copyright notice and this permission notice shall be included in all

#  copies or substantial portions of the Software.

#

#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR

#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,

#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE

#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER

#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,

#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

#  SOFTWARE


import os
import time
import asyncio
import logging
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

from config import Config
from pyrogram import Client, idle
from pyrogram.errors import BadMsgNotification
from pyromod import listen

# Logger setup
LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=5000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

# Auth Users
AUTH_USERS = [int(chat) for chat in Config.AUTH_USERS.split(",") if chat != ""]

# Prefixes
prefixes = ["/", "~", "?", "!"]

# Plugins
plugins = dict(root="plugins")

# Bot Initialization
bot = Client(
    "StarkBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=20,
    plugins=plugins,
    workers=50,
)


# Time Sync Function
async def sync_time():
    try:
        utc_now = datetime.utcnow()
        adjusted_time = utc_now + timedelta(seconds=2)  # Small adjustment
        os.environ["TZ"] = "UTC"
        time.tzset()
        LOGGER.info(f"Time synchronized to: {adjusted_time}")
    except Exception as e:
        LOGGER.error(f"Time synchronization failed: {e}")


# Retry Mechanism for Connection
async def connect_with_retries(bot, retries=3, delay=5):
    for attempt in range(retries):
        try:
            await bot.start()
            return  # Successful connection
        except BadMsgNotification:
            LOGGER.warning(f"Time sync failed. Retrying in {delay} seconds...")
            await asyncio.sleep(delay)
    raise RuntimeError("Failed to connect after multiple retries.")


# Main Function
async def main():
    await sync_time()  # Sync time before starting
    await connect_with_retries(bot)  # Attempt connection with retries
    bot_info = await bot.get_me()
    LOGGER.info(f"<--- @{bot_info.username} Started (c) STARKBOT --->")
    await idle()


# Start the Bot
if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        LOGGER.info("<---Bot Stopped-->")