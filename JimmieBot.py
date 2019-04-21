import importlib
from Common import *
import os

#VERSION 2, BABE

__title__ = "JimmieBot"
__author__ = "Benjy355"
__version__ = 2.0

import asyncio
import discord

class JimmieBot(discord.Client):
    #Contains the literal modules loaded
    _MODULES = []

    _COMMANDS = {}
    #RegEx pattern
    _PATTERNS = []

    COMMAND_PREFIX = "!"

    #Decorator for module to register itself as a regex pattern

    def __init__(self):
        super().__init__()
        self.load_modules()

    def load_modules(self, folder="modules"):
        #Used to load in all COMMAND/PATTERN modules
        #TODO: Add ability to wipe out/reload modules?
        try:
            modules = os.listdir(folder)
        except FileNotFoundError:
            print("Module folder '%s' not found!" % os.path.abspath(folder))
            return
        
        print("--Loading Modules--")
        for full_module in modules:
            #NOTE: os.path.isfile returns true on literally nothing? What the fuck, python
            if (os.path.isdir(full_module)):
                print("Ignoring %s" % full_module)
                break

            module = os.path.splitext(full_module)[0]
            full_package = "%s.%s" % (folder.replace(os.path.sep, "."), module)
            #Import the module
            try:
                newest_module = importlib.import_module(full_package)
            except ImportError as err:
                print("Failed to load %s: %s" % (full_package, err))
                break
            #Catch to see if we are importing a compatible module (Check for our usual values)
            #TODO: Check for the actual call function as well, instead of using a try/catch
            try:
                print("Loaded [%s]%s" % (float(newest_module.__version__), newest_module.__name__))
            except AttributeError as err:
                print("Failed to load %s: Invalid Module" % full_package)
                break
            self._MODULES.append(newest_module)
            newest_module.bot_client = self
            #Add our new module to it's type list
            if (newest_module.__type__ == ModuleType.COMMAND):
                self._COMMANDS[newest_module.__trigger__] = newest_module
            elif (newest_module.__type__ == ModuleType.REGEX):
                self._PATTERNS.append(newest_module)
        print("--Done!--\n")
            
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