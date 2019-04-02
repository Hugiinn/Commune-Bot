import discord, pickle, os

class CommuneBot:

    def __init__(self):
        self.client = discord.Client()

        self.client.event(self.on_ready)
        self.client.event(self.on_message)

        # Set /home/%user%/CommuneBot/ as save directory. If folder doesn't exist, create it.
        self. saveLocation = os.path.expanduser("~") + "/CommuneBot/"

        if not os.path.isdir(self.saveLocation):
            os.mkdir(self.saveLocation)

        # Load file. If it doesn't exist, create empty list.
        try:
            with open(self.saveLocation + "permittedRoles.pickle", "rb") as f:
                self.roles = pickle.load(f)
        except:
            self.roles = []

    async def start(self):
        TOKEN = os.environ["TOKEN"]
        await self.client.run(TOKEN)

    async def on_message(self, message):

        if message.content.startswith("!"):
            contentList = message.content.split()

            # Command for adding roles the list of permitted roles that users can assign to themselves.
            if contentList[0] == "!permit":

                # If the user has the Bot Operator role.
                permitRole = discord.utils.get(message.author.server.roles, name="Bot Operator")
                if permitRole in message.author.roles:

                    roleName = " ".join(contentList[1:])
                    self.roles.append(roleName)

                    # Save.
                    with open(self.saveLocation + "permittedRoles.pickle", "wb") as f:
                        pickle.dump(self.roles, f)

                    msg = "Updated! Current list of approved roles: " + ', '.join(self.roles)
                    await self.client.send_message(message.channel, msg)

                # If the user doesn't have the bot operator role.
                else:
                    await self.client.send_message(message.channel, "You are not allowed to add roles to the list.")

            # Command for users to give themselves roles.
            if contentList[0] == "!role":

                roleName = " ".join(contentList[1:])
                try:
                    role = discord.utils.get(message.author.server.roles, name=roleName)
                    await self.client.add_roles(message.author, role)
                except:
                    await self.client.send_message(message.channel, "Role does not exist.")

        else:
            return

    async def on_ready(self):
        print("Bot is up & running.")
        print(self.client.user)
        await self.client.change_presence(game=discord.Game(name="Absolute unit of a bot."))



