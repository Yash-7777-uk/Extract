#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) ACE 

import os

class Config(object):
    # get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6134545369:AAHwFsSr7IaKEX-IpipLaTpdqxQcqzAhkag")
    API_ID = int(os.environ.get("API_ID", "29103942")
    API_HASH = os.environ.get("API_HASH", "3a10eb2080e0fe8ee87dc74f6c141aea")
    AUTH_USERS = "1260699325"

