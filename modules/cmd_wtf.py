from Common import ModuleType
import JimmieBot
import discord
import sys
import Config
import urllib
import asyncio

__name__ = "WHAT THE FUCK"
__description__ = ""
__version__ = "1.0"
__trigger__ = "wtf"
__type__ = ModuleType.COMMAND
__admin__ = False

bot_client = None

async def on_activate(message: discord.message.Message):
    await message.channel.send(content=". 　  a 　 h\n\n　 a 　 　　 h\n\n　 t 　　 w h 　 　　　　 c　　k\n\n　　T 　 　　 　 　 u\n\n　　　 h　 ₑ　 F")