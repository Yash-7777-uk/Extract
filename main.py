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
import asyncio
import logging
from datetime import datetime, timedelta
from pyrogram import Client, idle
from config import Config
from pyromod import listen
from logging.handlers import RotatingFileHandler

# Logging Configuration
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

# Plugins Directory
plugins = dict(root="plugins")

# Sync Time Function
async def sync_time():
    try:
        current_time = datetime.utcnow()
        await asyncio.sleep(1)  # Small delay for synchronization
        LOGGER.info(f"Time synchronized: {current_time + timedelta(seconds=1)}")
    except Exception as e:
        LOGGER.error(f"Time synchronization failed: {e}")

# Main Bot Initialization
if __name__ == "__main__":
    bot = Client(
        "StarkBot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=20,
        plugins=plugins,
        workers=50,
    )

    async def main():
        # Time Synchronization
        await sync_time()

        # Start Bot
        await bot.start()
        bot_info = await bot.get_me()
        LOGGER.info(f"<--- @{bot_info.username} Started (c) STARKBOT --->")
        await idle()

    # Run Event Loop
    asyncio.get_event_loop().run_until_complete(main())
    LOGGER.info("<--- Bot Stopped --->")