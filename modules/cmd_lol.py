from Common import ModuleType
import JimmieBot
import discord
from bs4 import BeautifulSoup
import EmojiEnum
import sys
import Config
import urllib
import asyncio

__name__ = "Bad Joke Module"
__description__ = "Rips a garbage joke from goodbadjobes.com"
__version__ = "1.0"
#Either the command called, or the RegEx pattern used
__trigger__ = "lol"
#Command or Regex Pattern
#TODO: Add more types (Scheduled?)
__type__ = ModuleType.COMMAND
__admin__ = False

#Set by import function of JimmieBot (hopefully)
bot_client = None

#discord.channel.TextChannel.send()

#Called when the trigger phrase/condition is found
async def on_activate(message: discord.message.Message):
    await message.channel.trigger_typing()
    try:
        joke_contents = urllib.request.urlopen("https://www.goodbadjokes.com/random").read().decode()
    except:
        print("Failed to load joke!")
        print(sys.exc_info()[0])
        joke_contents = ""
    soup = BeautifulSoup(joke_contents, "html.parser")
    joke_container = soup.find("dt")
    punchline_container = soup.find("dd")
    
    if (joke_container != None and punchline_container != None):
        await message.channel.send(content="**%s**" % joke_container.string)
        punchline_message = await message.channel.send(content="%s..." % EmojiEnum.thinking)
        await asyncio.sleep(5)
        await punchline_message.edit(content=punchline_container.string)
        await punchline_message.add_reaction(emoji=EmojiEnum.laugh_cry)
    else:
        await message.channel.send(content="Sorry my funny bone isn't feeling very funny right now %s" % EmojiEnum.crying, delete_after=10.0)
        #print("Failed to make joke, dumping contents:\n %s\n%s" % (joke_container.string, punchline_container.string))
        await asyncio.sleep(10)
        await message.delete()