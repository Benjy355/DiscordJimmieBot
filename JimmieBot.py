#VERSION 2, BABE

__title__ = "JimmieBot"
__author__ = "Benjy355"
__version__ = 2.0

import asyncio
import discord

class JimmieBot(discord.Client):
    async def on_ready(self):
        print("Connected to Discord")
        print("%s (%s)\n" % (self.user.name, self.user.id))