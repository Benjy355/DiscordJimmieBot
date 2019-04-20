#VERSION 2, BABE

__title__ = "JimmieBot"
__author__ = "Benjy355"
__version__ = 2.0

import asyncio
import discord

class JimmieBot(discord.Client):
    COMMANDS = {}
    #RegEx pattern
    PATTERNS = []

    COMMAND_PREFIX = "!"

    async def on_ready(self):
        print("Connected to Discord")
        print("%s (%s)\n" % (self.user.name, self.user.id))
    
    async def on_message(self, message: discord.message.Message):
        if (message.author == self.user):
            return
        if (not message.content.startswith(self.COMMAND_PREFIX)):
            return
            
        cleaned_str = message.content.split(" ", 1)
        #[n:] removes the prefix
        cleaned_str = cleaned_str[0][len(self.COMMAND_PREFIX):].lower()