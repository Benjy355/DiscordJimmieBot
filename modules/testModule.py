from Common import ModuleType
import JimmieBot
import discord

__name__ = "Test module"
__version__ = "1.0"
#Either the command called, or the RegEx pattern used
__trigger__ = "test"
#Command or Regex Pattern
#TODO: Add more types (Scheduled?)
__type__ = ModuleType.COMMAND
__admin__ = False

#Set by import function of JimmieBot (hopefully)
bot_client = None

#Called when the trigger phrase/condition is found
def on_activate(message: discord.message.Message):
    print("On_activate!")
    pass