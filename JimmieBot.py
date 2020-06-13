import importlib
import EmojiEnum
import os
import Config
import re
import sys

from Common import *

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
                continue

            module = os.path.splitext(full_module)[0]
            full_package = "%s.%s" % (folder.replace(os.path.sep, "."), module)
            #Import the module
            try:
                newest_module = importlib.import_module(full_package)
            except Exception as err:
                print("Failed to load %s: %s" % (full_package, err))
                continue
            #Catch to see if we are importing a compatible module (Check for our usual values)
            #We can't unload modules once we import them... So, we just never ever add it to the Commands/Regex things... ever.
            try:
                newest_module.bot_client = self
                #Add our new module to it's type list
                if (newest_module.__type__ == ModuleType.COMMAND):
                    self._COMMANDS[newest_module.__trigger__] = newest_module
                elif (newest_module.__type__ == ModuleType.REGEX):
                    self._PATTERNS.append(newest_module)
                self._MODULES.append(newest_module)
                print("Loaded [%s]%s" % (newest_module.__version__, newest_module.__name__))
            except AttributeError as err:
                print("Failed to load %s: Invalid Module!" % full_package)
                del newest_module #DON'T KNOW IF THIS WORKS YET, TEST PLS
                continue
            
        print("--Done!--\n")
            
    async def on_ready(self):
        print("Connected to Discord")
        print("%s (%s)\n" % (self.user.name, self.user.id))
    
    async def on_message(self, message: discord.message.Message):
        if (message.author == self.user):
            return

        #REGEX Detection
        for pattern in self._PATTERNS:
            test_match = re.search(pattern.__trigger__, message.content)
            if (test_match != None):
                await pattern.on_activate(message, test_match)
        
        if (not message.content.startswith(self.COMMAND_PREFIX)):
            return
        cleaned_str = message.content.split(" ", 1)
        #[n:] removes the prefix
        cleaned_str = cleaned_str[0][len(self.COMMAND_PREFIX):].lower()
        
        #Command detection
        if (not (cleaned_str in self._COMMANDS)):
            return
        command = self._COMMANDS[cleaned_str]
        if (command.__admin__ and message.author.permissions_in(message.channel)):
            print("%s tried to call admin function %s without permissions" % (message.author.display_name, cleaned_str))
            return
        
        await message.add_reaction(EmojiEnum.thumbs_up)
        await command.on_activate(message)