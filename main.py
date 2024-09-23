import discord
from discord.ext import commands
import discord.utils
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")
afk_users = []


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Over Genesis", type=1))
    print("Bot is ready")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1033805907387228262)
    await channel.send(f"{member} has joined the server")


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1033805907387228262)
    await channel.send(f"{member} has left the server")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Invalid command used.")


@bot.command()
async def ping(ctx):
    await ctx.send(f"The ping is {round(bot.latency*1000)}ms")


@bot.command(aliases=["8ball"])
async def _8ball(ctx):
    responses = ["It is certain.", "It is decidedly so.", "Without a doubt", "Definitely", "Yes", "You may rely on it",
                 "As I see it, yes", "Most likely", "Outlook good", "Signs point to yes.", "Reply hazy, try again",
                 "Ask again later", "Better not tell you now", "Cannot predict now", "Concentrate and ask again.",
                 "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]

    await ctx.send(f"{random.choice(responses)}")


@bot.command()
async def gay(ctx, *, member: discord.Member):
    per = random.randint(0, 100)
    await ctx.send(f"{member} is {per}% gay")


@bot.command()
async def afk(ctx, *, args):
    msg = " ".join(args)
    afk_users.append(ctx.author.id)
    afk_users.append(msg)
    await ctx.send("Afk has been set!")


@bot.event
async def on_message(message):
    for i in range(len(afk_users)):
        if f"<@{afk_users[i]}>" in message.split():
            await message.channel.send(f"He is afk")


@bot.command()
async def help(ctx):
    message = discord.Embed(title="Help", description="Use g!help (command) for extended information")

    message.add_field(name="Casual", value="ping, afk")
    message.add_field(name="Fun", value="gay,8ball")
    message.add_field(name="Moderation", value="clear,kick,ban,unban,tempban,mute,unmute")
    await ctx.send(embed=message)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Deleted {amount} messages!")


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please specify the amount of messages to delete")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You do not have the permissions to use this command")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: commands.MemberConverter, *, reason=None):
    await ctx.guild.kick(member, reason=reason)
    await ctx.send(f"Kicked {member}")


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please specify who to kick")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You do not have the permissions to use this command")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: commands.MemberConverter, *, reason=None):
    await ctx.guild.ban(member, reason=reason)
    await ctx.send(f"Banned {member}")


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please specify who to ban")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You do not have the permissions to use this command")


class DurationConverter(commands.ColourConverter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ["s", "m", "h", "d"]:
            return int(amount), unit

        raise commands.BadArgument(message="Not a valid duration")


@bot.command()
@commands.has_permissions(ban_members=True)
async def tempban(ctx, member: commands.MemberConverter, *, duration: DurationConverter):
    multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    amount, unit = duration
    await ctx.guild.ban(member)
    await ctx.send(f"Banned **{member}** for **{amount}{unit}**")
    await asyncio.sleep(amount*multiplier[unit])
    await ctx.guild.unban(member)


@tempban.error
async def tempban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please specify who to temporarily ban")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You do not have the permissions to use this command")


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = ctx.guild.bans()
    member_name, member_discriminant = member.split("#")

    async for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminant):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please specify who to unban")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You do not have the permissions to use this command")


class TimeConverter(commands.ColourConverter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ["s", "m", "h", "d"]:
            return int(amount), unit

        raise commands.BadArgument(message="Not a valid duration")


@bot.command()
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, id=1034811528337178654)
    await member.add_roles(role)
    await ctx.send(f"{member} was Muted")


@bot.command()
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, id=1034811528337178654)
    await member.remove_roles(role)
    await ctx.send(f"{member} was Unmuted")


@bot.command()
async def members(ctx, *, role1: discord.Role):
    role = discord.utils.get(ctx.guild.roles, name=f"{role1.name}")
    l = []
    if role is None:
        await ctx.send(f'There is no "{role1}" role on this server!')
        return
    ok = 0
    for member in ctx.guild.members:
        ok = ok + 1
        if role1 in member.roles:
            l.append(f"{member.mention}({member})")
            print(member)
            await ctx.send(f"{member.mention}({member})")
    res2 = "\n".join(l)
    print(res2)
    embed = discord.Embed(title=f"Members in {role1.name}", description=f"{res2}", colour=discord.Colour.blue())
    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)
    if len(l) == 0:
        await ctx.send(f"Nobody has the role {role1}")


@bot.command()
async def roles(ctx, role: discord.Role):
    for member in ctx.guild.members:
        if role in member.roles:
            await ctx.send(f"{member.name}")


@bot.command()
async def dmall1(ctx):
    if ctx.author.display_name == "Prodigy":
        await ctx.send("doing")
        for member in ctx.guild.members:
            try:
                await member.send("Welcome to Minoru Studios\n"
                                 "We are working on games inspired by the anime Jujutsu Kaisen and are nearing a tester release\n"
                                "In lieu of that, we are hosting a **500 robux** giveaway in our server which you can join\n"
                                "Our server invite link:\n"
                                "https://discord.gg/Y9Wf7DDrvX")
            except:
                print("Couldnt DM")
        await ctx.send("Done")


@bot.command()
async def dmall2(ctx):
    if ctx.author.display_name == "Prodigy":
        await ctx.send("doing")
        for member in ctx.guild.members:
            try:
                await member.send("Welcome to Minoru Studios\n"
                                    "We are working on games inspired by the anime Jujutsu Kaisen and are nearing a tester release\n"
                                    "In lieu of that, we are hosting a **500 robux** giveaway in our server which you can join\n"
                                    "Our server invite link:\n"
                                    "https://discord.gg/Y9Wf7DDrvX")
            except:
                print("Couldnt DM")
        await ctx.send("Done")

bot.run(TOKEN)