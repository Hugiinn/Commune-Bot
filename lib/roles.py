# Roles handling file
import pickle, discord

class roleFunctions:

    # Command for adding roles the list of permitted roles that users can assign to themselves.
    async def addPermitRole (self, client, message, contentList, permittedRoles, saveLocation):

        # Command for getting the "Bot Operator" role's code.
        permitRole = discord.utils.get(message.author.server.roles, name="Bot Operator")

        # Check if user is allowed to add roles to the list.
        if permitRole in message.author.roles:

            roleName = " ".join(contentList[1:])

            # Check if the role given as an argument even exists.
            if discord.utils.get(message.author.server.roles, name=roleName) is not None:

                # Check if the role isn't already in the list.
                if roleName not in permittedRoles:

                    permittedRoles.append(roleName)
                    with open(saveLocation + "permittedRoles.pickle", "wb") as f:
                        pickle.dump(permittedRoles, f)

                    msg = "Updated! Current list of approved roles: " + ', '.join(permittedRoles)
                    await client.send_message(message.channel, msg)

                else:
                    await client.send_message(message.channel, "Already in the list.")


            else:
                await client.send_message(message.channel, "Not a valid role")

        # If the user doesn't have the bot operator role.
        else:
            await client.send_message(message.channel, "You are not allowed to add roles to the list.")

    # Command for deleting roles for the permittedRoles list.
    async def delPermitRole (self, client, message, contentList, permittedRoles, saveLocation):

        # Command for getting the "Bot Operator" role's code.
        permitRole = discord.utils.get(message.author.server.roles, name="Bot Operator")

        # Check if user is allowed to remove roles from the list.
        if permitRole in message.author.roles:

            roleName = " ".join(contentList[1:])

            if roleName in permittedRoles:
                permittedRoles.remove(roleName)
                msg = roleName + " removed. Current list of approved roles: " + ', '.join(permittedRoles)
                await client.send_message(message.channel, msg)

            else:
                await client.send_message(message.channel, "The role you're trying to delete isn't in the list of permitted roles.")

    # Command for users to give themselves roles.
    async def giveRole (self, client, message, contentList, permittedRoles):

            roleName = " ".join(contentList[1:])

            role = discord.utils.get(message.author.server.roles, name=roleName)

            # Check if the role exists.
            if role is None:
                await client.send_message(message.channel, "Role does not exist.")
                return

            # Check if the desired role is permitted or not.
            if roleName in permittedRoles:
                await client.add_roles(message.author, role)
                await client.send_message(message.channel, "Added!")
            else:
                await client.send_message(message.channel, "You are not allowed to give yourself that role.")

    # Command for users to delete roles themselves.
    async def delRole(self, client, message, contentList):
        roleName = " ".join(contentList[1:])
        role = discord.utils.get(message.author.server.roles, name=roleName)

        # Check if the role exists.
        if role is None:
            await client.send_message(message.channel, "You're trying to remove a role you either don't have or doesn't exist, dummy.")
        else:
            await client.remove_roles(message.author, role)
            await client.send_message(message.channel, "Removed!")