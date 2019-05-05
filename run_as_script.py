#Runs JimmieBot as a normal script
from JimmieBot import JimmieBot
from discord_oauth import BOT_TOKEN

jBot = JimmieBot()
jBot.run(BOT_TOKEN)
#Should we try to catch it when it crashes? (As it always does)
#No. We shouldn't, until we fix our module loading system to not double load modules on startup