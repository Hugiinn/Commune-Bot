import os, pickle, discord
from lib.roles import roleFunctions

class CommuneBot:

    def __init__(self):
        self.client = discord.Client()
        self.roleFunctions = roleFunctions()

        self.client.event(self.on_ready)
        self.client.event(self.on_message)

        # Set /home/%user%/CommuneBot/ as save directory. If folder doesn't exist, create it.
        self.saveLocation = os.path.expanduser("~") + "/CommuneBot/"

        if not os.path.isdir(self.saveLocation):
            os.mkdir(self.saveLocation)

        # Load file. If it doesn't exist, create empty list.
        try:
            with open(self.saveLocation + "permittedRoles.pickle", "rb") as f:
                self.permittedRoles = pickle.load(f)
        except:
            self.permittedRoles = []

    async def start(self):
        TOKEN = os.environ["TOKEN"]
        await self.client.run(TOKEN)

    async def on_message(self, message):

        if message.content.startswith("!"):
            contentList = message.content.split()

            if contentList[0] == "!permit":
                await self.roleFunctions.addPermitRole(self.client, message, contentList, self.permittedRoles, self.saveLocation)

            if contentList[0] == "!unpermit":
                await self.roleFunctions.delPermitRole(self.client, message, contentList, self.permittedRoles, self.saveLocation)

            if contentList[0] == "!role":
                await self.roleFunctions.giveRole (self.client, message, contentList, self.permittedRoles)

            if contentList[0] == "!delrole":
                await self.roleFunctions.delRole(self.client, message, contentList)

            if contentList[0] == "!permitted":
                msg = "The current list of permitted roles are: " + ', '.join(self.permittedRoles)
                await self.client.send_message(message.channel, msg)

        else:
            return

    async def on_ready(self):
        print("Bot is up & running.")
        print(self.client.user)
        await self.client.change_presence(game=discord.Game(name="Absolute unit of a bot."))



