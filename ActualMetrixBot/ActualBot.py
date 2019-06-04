import discord
import youtube_dl
from discord.ext import commands

#id = 579081919526993947

def read_token(): #Retrieves token from txt
    with open("token.txt","r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()

client = commands.Bot(command_prefix='&')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='[&] | Serving Metrix'))
    print("Metrix Bot is ready")


@client.event  # System functions
async def on_message(message):
    botName = ["MetriX e-Sports Bot [&]#9861"]

    with open('censor.txt', 'r') as f:  # reads censor.txt

        censor = [line.strip() for line in f]

    with open('raffle.txt', 'r+') as f: #reads raffle list

        rafflelist = [line.strip() for line in f]

    if str(message.author) not in botName:  # Prevents bot from reading own message
        for word in censor:  # word censor
            if message.content.count(f"""{word} """) > 0:
                await message.channel.purge(limit=1)
                await message.channel.send(f"""{message.author.mention} used a bad word""")
                return

            elif message.content == word:
                await message.channel.purge(limit=1)
                await message.channel.send(f"""{message.author.mention} used a bad word""")
                return

    if str(message.author) not in botName:  # Prevents bot from reading own message
        if str(message.channel) == "•》suggestions":  # adds emojis to votes
            await message.add_reaction(emoji='👍')
            await message.add_reaction(emoji='👎')
            await message.add_reaction(emoji='🤷')
            return
   
    await client.process_commands(message)


@client.command() # Kick command
async def kick(ctx, member : discord.Member, *, reason=None):
    rstr = reason
    await member.kick(reason=reason)
    await ctx.channel.send(f"{member} has been kicked by {ctx.author.mention} \n Reason: {rstr}")


@client.command()  # Ban command
async def ban(ctx, member : discord.Member, *, reason=None):
    rstr = reason
    await member.ban(reason=reason)
    await ctx.channel.send(f"{member} has been banned by {ctx.author.mention} \n Reason: {rstr}")


@client.command()  # Unban command
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.send(f"{ctx.author.mention} unbanned {user.name}#{user.discriminator}")
            return


@client.command()  # Gives command list
async def commands(message):
    embed = discord.Embed(title="Bot Command Help", description="Commands for Metrix Esports Bot",
                          color=discord.Colour.blurple())
    embed.add_field(name="Bot prefix", value="The bot prefix for Metrix Esports Bot is [&]")
    embed.add_field(name="&hello", value="Bot greets the user.")
    embed.add_field(name="&users", value="Bot shows total number of members in the server excluding bots")
    embed.add_field(name="&tryout", value="Adds user to the tryout list, unspammable")
    embed.add_field(name="&tryoutNA", value="Shows NA tryout list, staff only")
    embed.add_field(name="&tryoutEU", value="Shows EU tryout list, staff only")
    embed.add_field(name="&tryoutAsia", value="Shows Asia tryout list, staff only")
    embed.add_field(name="&trydone", value="Removes member from respective tryout list, staff only")
    embed.add_field(name="&ban", value="Bans the mentioned user, reason is optional. Staff only")
    embed.add_field(name="&kick", value="Kicks the mentioned user, reason is optional. Staff only")
    embed.add_field(name="&unban", value="Unbans user, use discord name and discriminator. Staff only")
    await message.channel.send(content=None, embed=embed)


@client.command()  # Latency checker
async def ping(ctx):
    await ctx.channel.send(f"Pong!\n Took {round(client.latency*1000)}ms to respond!")

@client.command()  # Tryout command
async def tryout(message):
    NArolelist = [f"{member.mention}" for member in message.guild.get_role(572054683896774676).members]
    EUrolelist = [f"{member.mention}" for member in message.guild.get_role(572054606578974751).members]
    Asiarolelist = [f"{member.mention}" for member in message.guild.get_role(572054734190542867).members]

    with open('tryoutNA.txt', 'r+') as f:  # reads NA Tryout list

        NAtryout = [line.strip() for line in f]

    with open('tryoutEU.txt', 'r+') as f:  # reads EU Tryout list

        EUtryout = [line.strip() for line in f]

    with open('tryoutAsia.txt', 'r+') as f:  # reads Asia Tryout list

        Asiatryout = [line.strip() for line in f]

    if message.author.mention in NArolelist:  # NA
        if message.author.mention not in NAtryout:
            f = open("tryoutNA.txt", "a+")
            f.write(message.author.mention)
            f.close()
            await message.channel.send(f"""{message.author.mention} has been added to the NA tryout list""")
            return

        elif message.author.mention in NArolelist:
            await message.channel.send(
                f"""{message.author.mention}, you have already been added to the NA tryout list!""")
            return

    elif message.author.mention in EUrolelist:  # EU
        if message.author.mention not in EUtryout:
            f = open("tryoutEU.txt", "a+")
            f.write(message.author.mention)
            f.close()
            await message.channel.send(f"""{message.author.mention} has been added to the EU tryout list""")
            return

        elif message.author.mention in EUtryout:
            await message.channel.send(
                f"""{message.author.mention}, you have already been added to the EU tryout list!""")
            return

    elif message.author.mention in Asiarolelist:  # Asia
        if message.author.mention not in Asiatryout:
            f = open("tryoutAsia.txt", "a+")
            f.write(message.author.mention)
            f.close()
            await message.channel.send(f"""{message.author.mention} has been added to the Asia tryout list""")
            return

        elif message.author.mention in Asiarolelist:
            await message.channel.send(
                f"""{message.author.mention}, you have already been added to the Asia tryout list!""")
            return

    else:
        await message.channel.send(f"""{message.author.mention}, you need to select a region to apply for tryouts.""")


@client.command() #Pulls NA tryout list
async def tryoutNA(message):
    import os

    staff = [f"{member.mention}" for member in message.guild.get_role(569458583935254538).members]

    if message.author.mention in staff:  # Restricts command to staff
        if os.stat("tryoutNA.txt").st_size is not 0:  # Checks to make sure list is not empty
            f = open("tryoutNA.txt", "r+")
            if f.mode == "r+":
                NAlist = f.read()
                await message.channel.send(f"""{NAlist}""")

        elif os.stat("tryoutNA.txt").st_size == 0:  # List empty error message
            await message.channel.send(f"""There are currently no people on the NA tryout list""")

    elif message.author.mention not in staff:  # Role error message
        await message.channel.send(
            f"""{message.author.mention}, you have to be staff to access tryout lists!""")


@client.command() #Pulls EU tryout list
async def tryoutEU(message):
    import os

    staff = [f"{member.mention}" for member in message.guild.get_role(569458583935254538).members]

    if message.author.mention in staff:  # Restricts command to staff
        if os.stat("tryoutEU.txt").st_size is not 0:  # Checks to make sure list is not empty
            f = open("tryoutEU.txt", "r+")
            if f.mode == "r+":
                EUlist = f.read()
                await message.channel.send(f"""{EUlist}""")

        elif os.stat("tryoutEU.txt").st_size == 0:  # List empty error message
            await message.channel.send(f"""There are currently no people on the EU tryout list""")

    elif message.author.mention not in staff:  # Role error message
        await message.channel.send(
            f"""{message.author.mention}, you have to be staff to access tryout lists!""")


@client.command() #Pulls Asia tryout list
async def tryoutAsia(message):
    import os

    staff = [f"{member.mention}" for member in message.guild.get_role(569458583935254538).members]

    if message.author.mention in staff:  # Restricts command to staff
        if os.stat("tryoutAsia.txt").st_size is not 0:  # Checks to make sure list is not empty
            f = open("tryoutAsia.txt", "r+")
            if f.mode == "r+":
                Asialist = f.read()
                await message.channel.send(f"""{Asialist}""")

        elif os.stat("tryoutAsia.txt").st_size == 0:  # List empty error message
            await message.channel.send(f"""There are currently no people on the Asia tryout list""")

    elif message.author.mention not in staff:  # Role error message
        await message.channel.send(
            f"""{message.author.mention}, you have to be staff to access tryout lists!""")


@client.command() #Removes member from tryout list
async def trydone(message, member: discord.Member):

    with open('tryoutNA.txt', 'r+') as f: #reads NA Tryout list

        NAtryout = [line.strip() for line in f]

    with open('tryoutEU.txt', 'r+') as f: #reads EU Tryout list

        EUtryout = [line.strip() for line in f]

    with open('tryoutAsia.txt', 'r+') as f: #reads Asia Tryout list

        Asiatryout = [line.strip() for line in f]

    valid_users = [f"{member.mention}" for member in message.guild.get_role(569190860957417502).members]
    staff = [f"{member.mention}" for member in message.guild.get_role(569458583935254538).members]

    if message.author.mention in staff:

        if member is not None:
            target = f"<@{member.id}>"
            if target in valid_users:
                if target in NAtryout:
                    with open("tryoutNA.txt", "r") as f:
                        lines = f.readlines()
                    with open("tryoutNA.txt", "w") as f:
                        for line in lines:
                            if line.strip("\n") != target:
                                f.write(line)
                    await message.channel.send(f"""{message.author.mention} has tried out {target}""")
                    return

                elif target in EUtryout:
                    with open("tryoutEU.txt", "r") as f:
                        lines = f.readlines()
                    with open("tryoutEU.txt", "w") as f:
                        for line in lines:
                            if line.strip("\n") != target:
                                f.write(line)
                    await message.channel.send(f"""{message.author.mention} has tried out {target}""")
                    return

                elif target in Asiatryout:
                    with open("tryoutAsia.txt", "r") as f:
                        lines = f.readlines()
                    with open("tryoutAsia.txt", "w") as f:
                        for line in lines:
                            if line.strip("\n") != target:
                                f.write(line)
                    await message.channel.send(f"""{message.author.mention} has tried out {target}""")
                    return

                else:
                    await message.channel.send(f"""The specified member is not on any of the tryout lists.""")

            elif target not in valid_users:
                await message.channel.send(
                    f"""{target} is not a valid member, please check your spelling and try again.""")  # Third level error message
                return

        elif member is None:
            await message.channel.send(
                f"""Please mention a member for this function to work""")  # Second level error message
            return

@client.command() #Shows total number of members
async def users(message):
    id = client.get_guild(569129875147980810)
    bot_num = 5 #Number of bots

    await message.channel.send(f"""Number of members in this server: {id.member_count - bot_num}""")


@client.command() #Greeting command
async def hello(message):
    await message.channel.send(f"Hello {message.author.mention}, Metrix e-Sports Bot is here to serve you!")

client.run(token)
