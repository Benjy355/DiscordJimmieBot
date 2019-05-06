from Common import *
import discord
import re

REGEX_STEAM_LINKS_PATTERN = r"(steam://openurl/)?(https?://store\.steampowered\.com/\S*)"

__name__ = "Steam link fixer"
__description__ = "Replaces regular Steam store links with one that will open in Steam."
__version__ = "1.0"
__trigger__ = r"(steam://openurl/)?(https?://store\.steampowered\.com/\S*)"
__type__ = ModuleType.REGEX
__admin__ = False

bot_client = None

async def on_activate(message: discord.message.Message, match_result):
    if (not match_result.group(1)):
        #Fix that link!
        good_link = "steam://openurl\%s" % match_result.group(2)
        stripped_message = re.sub(REGEX_STEAM_LINKS_PATTERN, "--", message.content)
        await message.channel.send("Better Link:\n%s\n%s:\n%s" % (good_link, message.author.mention, stripped_message))
        await message.delete()