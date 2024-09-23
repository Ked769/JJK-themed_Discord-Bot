import discord
from discord.ext import commands
import datetime
import random
import asyncio
from openai import OpenAI


class Talk(discord.ui.View):
    def __init__(self, ctx, author: discord.Member, member: discord.Member):
        super().__init__(timeout=15)
        self.value = None
        self.ctx = ctx
        self.member = member
        self.author = author
        self.button = False

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id != interaction.user.id:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f"You are not {self.member.name}", ephemeral=True)
        else:
            self.button = True
            # noinspection PyUnresolvedReferences
            await self.ctx.send(f"Im glad that we were able to end this without any unnecessary conflict")
            await self.ctx.send(f"https://tenor.com/view/naruto-gif-18958435")
            if self.member.top_role >= self.author.top_role:
                await self.ctx.send("Lets move forward as better people.")
            else:
                await self.ctx.send(f"Take the time to reconsider your past actions and move forward towards a better future.")
                newtime = datetime.timedelta(seconds=600)
                await self.member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                await interaction.message.delete()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id != interaction.user.id:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f"You are not {self.member.name}", ephemeral=True)
        else:
            self.button = True
            if self.member.top_role >= self.author.top_role:
                await self.ctx.send("Seems like I am incapable of understanding your pain.")
                await self.ctx.send("https://tenor.com/view/memories-naruto-past-uzumaki-snow-gif-18461895")
            else:
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message("You have denied it", ephemeral=True)
                await interaction.message.delete()
                await asyncio.sleep(1)
                await self.ctx.send("Seems like the only thing that I can give you is death")
                await asyncio.sleep(1)
                await self.ctx.send("https://tenor.com/view/naruto-rasengan-gif-5914321062346592896")
                await asyncio.sleep(3)
                roles = self.member.roles[1:]
                role_to_remove = random.choice(roles)
                await self.member.remove_roles(role_to_remove)
                newtime = datetime.timedelta(seconds=7200)
                await self.member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                await self.ctx.send("https://tenor.com/view/rasenshuriken-naruto-kakuzu-gif-18438957")
                await self.ctx.send(f"The whirling chakra needles due to the Rasenshuriken have pricked out **{role_to_remove.name}** "
                                    f"and left **{self.member}** incapable of combat for 2 hours")

    async def on_timeout(self):
        if self.button is False:
            await self.ctx.send("Seems like you aren't interested in hearing me out.")
            await self.ctx.send("https://tenor.com/view/naruto-gif-25133827")
            if self.member.top_role >= self.author.top_role:
                await self.ctx.send("Let's have a meaningful chat next time.")
            else:
                newtime = datetime.timedelta(seconds=1200)
                await self.member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                await self.ctx.send("I hope you're in a better mindset the next time we meet.")


class casual(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.data = {}
        self.snippet = {}
        self.inf = {}
        self.chimera = {}
        self.ai = {}
        self.num = 0
        self.client = OpenAI(api_key="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")
        self.client = OpenAI(api_key="api-key")
        self.timer = 60
        self.jogo = {}
        self.naoya = {}
        self.simple_domain = {}

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Valorant", type=1))
        print("Bot is ready")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = discord.utils.get(member.guild.channels, id=921477389777784832)
        embed = discord.Embed(title="Welcome", colour=discord.Colour.blue())
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name=f"Hey {member}",
                        value="Welcome to Minoru Games, you can purchase the tester shirt for **Kaizen Battlegrounds** at the link given below:\n"
                              "[**ACE Games Tester Shirt**](https://www.roblox.com/catalog/16573070108/Tester)")
        await channel.send(f"{member.mention}", embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.channels, id=1221289130537910386)
        await channel.send(f"{member} has left the server")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 1035197793041662033:
            if payload.emoji.name == "darkmatter":
                give_role = discord.utils.get(payload.member.guild.roles, name="NA")
                await payload.member.add_roles(give_role)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = discord.utils.get(after.guild.channels, id=1227717178564939886)
        if before.content != after.content:
            if before.author.bot is False:
                embed = discord.Embed(title=f"{after.author.name}\nMessage Edited", colour=discord.Colour.blurple(),
                                      timestamp=before.created_at)
                embed.set_thumbnail(url=after.author.avatar.url)
                embed.add_field(name="Before:", value=f"{before.content}", inline=False)
                embed.add_field(name="After:", value=f"{after.content}", inline=False)
                embed.add_field(name="Channel:", value=f"{after.channel.jump_url}", inline=False)
                # noinspection PyArgumentList
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = discord.utils.get(message.guild.channels, id=1221289130537910387)
        if message.guild.id in self.snippet:
            self.snippet[message.guild.id].clear()
        self.snippet[message.guild.id] = []
        self.snippet[message.guild.id].append(message.author.id)
        self.snippet[message.guild.id].append(message.content)
        for i in message.stickers:
            self.snippet[message.guild.id].append(i.url)
        if message.author.bot is False:
            embed = discord.Embed(title=f"{message.author.name}\nMessage Deleted", colour=discord.Colour.blurple(), timestamp=message.created_at)
            embed.set_thumbnail(url=message.author.avatar.url)
            embed.add_field(name="Content:", value=f"{message.content}", inline=False)
            attachments = []
            for image in message.attachments:
                attachments.append(image.url)
            if len(message.attachments) == 1:
                embed.set_image(url=f"{' '.join(attachments)}")
            elif len(message.attachments) > 0:
                embed.add_field(name="Attachments:", value=f"{' '.join(attachments)}", inline=False)
            embed.add_field(name="Channel:", value=f"{message.channel.jump_url}", inline=False)
            # noinspection PyArgumentList
            await channel.send(embed=embed)

    @commands.command(help="Returns the ping")
    async def ping(self, ctx):
        await ctx.send(f"The ping is {round(self.bot.latency * 1000)}ms")

    @commands.command(help="Returns the stats of the user")
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        roles = []
        for role in member.roles:
            roles.append(role)

        embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)

        embed.set_author(name=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        embed.add_field(name="ID:", value=member.id, inline=False)
        embed.add_field(name="Server Name:", value=member.display_name, inline=False)

        embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"),
                        inline=False)
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline=False)

        embed.add_field(name=f"Roles ({len(roles)}):", value=" ".join([role.mention for role in roles]), inline=False)
        embed.add_field(name="Top Role:", value=member.top_role.mention, inline=False)

        embed.add_field(name="Bot?", value=member.bot, inline=False)

        await ctx.send(embed=embed)

    @commands.command(help="Returns the server stats")
    async def serverinfo(self, ctx):
        roles = []
        for role in ctx.guild.roles:
            roles.append(role)
        embed = discord.Embed(colour=discord.Colour.green(), timestamp=ctx.message.created_at)

        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text=f"Required by {ctx.author}", icon_url=ctx.author.avatar.url)

        embed.add_field(name="Name:", value=ctx.guild.name, inline=False)
        embed.add_field(name="Roles:", value=len(ctx.guild.roles), inline=False)

        embed.add_field(name="Members:", value=ctx.guild.member_count, inline=False)
        embed.add_field(name="Channels:", value=len(ctx.guild.channels), inline=False)

        embed.add_field(name="Emojis:", value=len(ctx.guild.emojis), inline=False)
        embed.add_field(name="Owner:", value=ctx.guild.owner, inline=False)

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        if user.guild.id in self.data:
            if user.id in self.data[user.guild.id]:
                await channel.send("Afk removed!")
                i = self.data[user.guild.id].index(user.id)
                self.data[user.guild.id].remove(self.data[user.guild.id][i + 1])
                self.data[user.guild.id].remove(user.id)
                new_nick = user.display_name.split("[AFK]")
                await user.edit(nick=new_nick[1])

    @commands.Cog.listener()
    async def on_message(self, message):
        channels = [1212927204498087977, 1213089479879950376]
        bypass = [532631056856252436, 348694496114114564]
        mentions = []
        for i in message.mentions:
            mentions.append(i.id)
        if message.guild.id in self.data:
            for i in range(len(self.data[message.guild.id])):
                if self.data[message.guild.id][i] in mentions and not message.author.bot:
                    await message.channel.send(f"<@{self.data[message.guild.id][i]}> is away right now, they said {self.data[message.guild.id][i + 1]}")
        if message.guild.id in self.inf:
            for i in range(len(self.inf[message.guild.id])):
                if self.inf[message.guild.id][i] in mentions and not message.author.bot:
                    gojo = discord.utils.get(message.guild.members, id=self.inf[message.guild.id][i])
                    if message.author.top_role >= gojo.top_role:
                        await message.channel.send(f"You bypassed **{gojo.name}'s** passive application of limitless")
                    else:
                        await message.channel.send(f"You are unable to reach **{gojo.name}**")
                        newtime = datetime.timedelta(seconds=int(120))
                        await message.author.edit(timed_out_until=discord.utils.utcnow() + newtime)
        if message.guild.id in self.inf:
            if message.author.id in self.inf[message.guild.id]:
                if message.content != "g!inf":
                    self.inf[message.guild.id].remove(message.author.id)
                    await message.channel.send("Infinity Removed")
                    new_nick = message.author.display_name.split("[INF]")
                    try:
                        await message.author.edit(nick=new_nick[1])
                    except:
                        print("Owner Infinity")
        if message.guild.id in self.chimera:
            if message.author.id in self.chimera[message.guild.id]:
                await message.delete()
        if "best bot" in message.content:
            await message.reply("That'd be me")
        if message.guild.id in self.ai:
            if message.author.id == self.ai[message.guild.id]:
                if message.content != "quit":
                    response = self.client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": message.content,
                            }
                        ],
                        model="gpt-3.5-turbo",
                    )
                    async with message.channel.typing():
                        await asyncio.sleep(3)
                        await message.reply(response.choices[0].message.content.strip())
                    self.num += 1
                    if self.num == 10:
                        del self.ai[message.guild.id]
                        await message.channel.send("You have reached 10 inputs, your session has ended")
                else:
                    del self.ai[message.guild.id]
                    self.num = 0
                    await message.reply("The session has been ended")
        if message.guild.id in self.jogo:
            if message.author.id in self.jogo[message.guild.id]:
                choice = random.randint(1, 3)
                if choice == 2:
                    roles = message.author.roles[1:]
                    role_to_remove = random.choice(roles)
                    await message.author.remove_roles(role_to_remove)
        if message.guild.id in self.naoya:
            if message.author.id in self.naoya[message.guild.id]:
                newtime = datetime.timedelta(seconds=int(10*self.naoya[message.guild.id][message.author.id]))
                await message.author.edit(timed_out_until=discord.utils.utcnow() + newtime)
                self.naoya[message.guild.id][message.author.id] *= 2

        if 1034081315991080990 in mentions:
            role = discord.utils.get(message.guild.roles, id=1226241124444934304)
            member = discord.utils.get(message.guild.members, id=768074971213725706)
            if message.author.id == member.id:
                await member.add_roles(role)
                await message.reply("Deal")
        print(message.guild.id)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("I do not have any such command!\nType g!help to view available commands")

    @commands.command(help="Declares you are AFK")
    async def afk(self, ctx, *args):
        if ctx.guild.id not in self.data:
            self.data[ctx.guild.id] = []
        msg = " ".join(args)
        self.data[ctx.guild.id].append(ctx.author.id)
        self.data[ctx.guild.id].append(msg)
        await ctx.send("Afk set!")
        await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def inf(self, ctx):
        if ctx.guild.id not in self.inf:
            self.inf[ctx.guild.id] = []
        self.inf[ctx.guild.id].append(ctx.author.id)
        await ctx.send("You have now passively enabled infinity, you are now untouchable")
        await ctx.send("https://tenor.com/view/jujutsu-kaisen-gojo-satoru-vs-gif-21280734")
        try:
            await ctx.author.edit(nick=f"[INF] {ctx.author.display_name}")
        except:
            print("Owner Nickname")

    @commands.command()
    async def removeinf(self, ctx):
        self.inf[ctx.guild.id].remove(ctx.author.id)
        await ctx.send("Your infinity has been turned off manually")
        await ctx.send("Infinity Removed")
        new_nick = ctx.author.display_name.split("[INF]")
        await ctx.author.edit(nick=new_nick[1])

    @commands.command(aliases=['sd'])
    async def simpledomain(self, ctx):
        await ctx.send("You have activated your simple domain for the next 10min")
        await ctx.send("https://tenor.com/view/jujutsu-kaisen-domain-expansion-gif-21437690")
        if ctx.guild.id not in self.simple_domain:
            self.simple_domain[ctx.guild.id] = []
        self.simple_domain[ctx.guild.id].append(ctx.author.id)
        await asyncio.sleep(600)
        self.simple_domain[ctx.guild.id].remove(ctx.author.id)

    @inf.error
    async def inf_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have the permissions to use this command")

    @commands.command(help="DMs a user of your choice")
    async def message(self, ctx, member: discord.Member, *arg):
        msg = " ".join(arg)
        await member.send(f"{ctx.author.display_name} left a message for you \n > {msg}")
        await ctx.channel.purge(limit=1)
        await ctx.send("Message sent!")

    @message.error
    async def message_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"Cannot send messages to this user")

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member: discord.Member = None):
        sexy = [768074971213725706, 696704031023693914]
        if member is None:
            member = ctx.author
        embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)

        embed.set_author(name=f"{member}", icon_url=member.avatar.url)
        embed.add_field(name="Server Avatar", value="")
        embed.set_image(url=member.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        if member.id in sexy:
            await asyncio.sleep(1)
            await ctx.send("Sexy")

    @commands.command()
    async def dmall1(self, ctx):
        if ctx.author.display_name == "Prodigy":
            await ctx.send("doing")
            for member in ctx.guild.members:
                try:
                    await asyncio.sleep(0.25)
                    await member.send("__**Welcome to ACE Studios**__\n"
                                      "The staff of Aozora Studios has switched over to ACE Studios.\n"
                                      "We are working on games inspired by the anime Jujutsu Kaisen and are nearing a tester release\n"
                                      "We have an active community and we hold **nitro** and **robux** giveaways at milestones."
                                      "Join to get access to these benefits\n"
                                      "Our server invite link:\n"
                                      "https://discord.gg/5WW7JEt5Ak")
                except:
                    print("Couldnt DM")
            await ctx.send("Done")

    @commands.command()
    async def dmall2(self, ctx):
        if ctx.author.display_name == "Prodigy":
            await ctx.send("doing")
            for member in ctx.guild.members:
                try:
                    await asyncio.sleep(0.25)
                    await member.send("Welcome to Minoru Studios\n"
                                      "We are working on games inspired by the anime Jujutsu Kaisen and are nearing a tester release\n"
                                      "In lieu of that, we are hosting a **500 robux** giveaway in our server which you can join\n"
                                      "Our server invite link:\n"
                                      "https://discord.gg/Y9Wf7DDrvX")
                except:
                    print("Couldnt DM")
            await ctx.send("Done")

    @commands.command()
    async def fix(self, ctx, member: discord.Member):
        island_channel = discord.utils.get(ctx.guild.channels, id=1226849314735783956)
        for channel in ctx.guild.channels:
            await channel.set_permissions(member, overwrite=None)
        await island_channel.set_permissions(member, view_channel=False)

    @commands.command()
    async def snipe(self, ctx):
        print(self.snippet[ctx.guild.id])
        content = []
        for i in range(1, len(self.snippet[ctx.guild.id])):
            content.append(self.snippet[ctx.guild.id][i])
        print(content)
        member = discord.utils.get(ctx.guild.members, id=self.snippet[ctx.guild.id][0])
        embed = discord.Embed(title="Message Snipe", timestamp=ctx.message.created_at, colour=discord.Colour.blue())
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name=f"Deleted by {member.name}", value=f"{' '.join(content)}")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=["de", "domain"])
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def domainexpansion(self, ctx, member: discord.Member, *args):
        if ctx.guild.id in self.simple_domain:
            if member.id in self.simple_domain[ctx.guild.id]:
                await ctx.send("https://tenor.com/view/gojo-simple-domain-gif-2899725885283227519")
                await ctx.send(f"**{member.name}** has blocked the effects of the domain with their simple domain.")
                return
        print("b")
        domains = ["Infinite Void", "Malevolent Shrine", "Self Embodiment of Perfection", "Idle Death Gamble",
                   "Ceremonial Sea of Light", "Chimera Shadow Garden", "Horizon of the Captivating Skandha", "Coffin of the Iron Mountain", "Time Cell Moon Palace", "True Mutual Love",
                   "Kamehameha", "Talk No Jutsu", "Conquerors Haki", "Mist Breathing", "Infinite Tsukuyomi"]
        check = ""
        for i in range(len(args)):
            if i == 0:
                check += args[i]
            else:
                check += f" {args[i]}"
        print(check)
        global domain
        for i in domains:
            if check.lower() in i.lower():
                domain = i
        print(domain)
        if domain == domains[0]:
            await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
            await ctx.send("https://tenor.com/view/infinite-void-gojo-satoru-gojo-jjk-jujutsu-kaisen-gif-19219956")
            if member.top_role >= ctx.author.top_role:
                await asyncio.sleep(1)
                await ctx.send("The domain has crumbled")
            else:
                newtime = datetime.timedelta(seconds=600)
                await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                await asyncio.sleep(1)
                await ctx.send(f"Due to the effects of the domain **{member.name}** is unable to move for 10 minutes")

        elif domain == domains[1]:
            await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
            await ctx.send(
                f"https://tenor.com/view/sukuna-domain-expansion-jujustu-kaisen-shibuya-sukuna-vs-mahoraga-gif-3966585850028273519")
            if member.top_role >= ctx.author.top_role:
                await asyncio.sleep(1)
                await ctx.send("The domain has crumbled")
            else:
                await member.remove_roles(member.top_role)
                await asyncio.sleep(1)
                await ctx.send(f"Due to effects of the domain **{member.name}** has lost their greatest strength")

        elif domain == domains[2]:
            await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
            await ctx.send(
                "https://tenor.com/view/jjk-jujutsu-kaisen-mahito-jjk-fight-jujutsu-kaisen-fight-gif-693993311493234171")
            if member.top_role >= ctx.author.top_role:
                await asyncio.sleep(1)
                await ctx.send("The domain has crumbled")
            else:
                await asyncio.sleep(1)
                await member.edit(nick="Transfigured Human")
                await ctx.send(f"Due to the effects of the domain **{member.name}** has lost their humanity")

        elif domain == domains[3]:
            await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
            await ctx.send(
                f"https://tenor.com/view/hakari-kinji-kinji-hakari-hakari-kinji-kashimo-hajime-gif-15995875640514955845")
            if member.top_role >= ctx.author.top_role:
                await asyncio.sleep(1)
                await ctx.send("The domain has crumbled")
            elif ctx.author.id == 532631056856252436:
                async with ctx.typing():
                    await asyncio.sleep(3)
                await ctx.send("Jackpot has been attained")
                await ctx.send(
                    "https://tenor.com/view/hakari-hakari-kinji-kinji-hakari-kinji-jackpot-gif-12339332929838481118")
                await asyncio.sleep(1)
                await ctx.send(f"Due to the effects of the domain **{member.name}** has been banished from the server")
                await ctx.guild.ban(member)
            else:
                chance = random.randint(1, 10)
                await asyncio.sleep(1)
                await ctx.send("Attemping to attain Jackpot...")
                async with ctx.typing():
                    await asyncio.sleep(3)
                if chance == 5:
                    await ctx.send("Jackpot has been attained")
                    await ctx.send(
                        "https://tenor.com/view/hakari-hakari-kinji-kinji-hakari-kinji-jackpot-gif-12339332929838481118")
                    await asyncio.sleep(1)
                    await ctx.send(
                        f"Due to the effects of the domain **{member.name}** has been banished from the server")
                    await ctx.guild.ban(member)
                else:
                    await ctx.send("Failed to attain jackpot")

        elif domain == domains[4]:
            await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
            await ctx.send("https://tenor.com/view/jujutsu-kaisen-hanami-gif-20361654")
            if member.top_role >= ctx.author.top_role:
                await asyncio.sleep(1)
                await ctx.send("The domain has crumbled")
            else:
                await asyncio.sleep(1)
                name = member.display_name
                new_name = name[::-1]
                await member.edit(nick=f"🌳{new_name}🌳")
                await ctx.send(f"Due to the effects of the domain **{member.name}** has started sprouting")

        elif domain == domains[5]:
            await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
            await ctx.send("https://tenor.com/view/megumi-fushiguro-domain-expansion-ry%C5%8Diki-tenkai-chimera-shadow-garden-gif-25681375")
            if member.top_role >= ctx.author.top_role:
                await asyncio.sleep(1)
                await ctx.send("The domain has crumbled")
            else:
                await asyncio.sleep(1)
                if ctx.guild.id not in self.chimera:
                    self.chimera[ctx.guild.id] = []
                self.chimera[ctx.guild.id].append(member.id)
                await ctx.send(f"Due to the effects of the domain **{member.name}** has drowned in the shadows for the next 3 minutes")
                await asyncio.sleep(180)
                self.chimera[ctx.guild.id].remove(member.id)

        elif domain == domains[6]:
            dagon = {1209560942841434142: 1226849314735783956, 1221289127547244594: 1226849791900913726, 1030538747827208322: 1226263040962465904, 1122290976938016792: 1228693777279881369}
            await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
            await ctx.send("https://tenor.com/view/jjk-season-2-dagon-gif-65005131711436483")
            if member.top_role >= ctx.author.top_role:
                await asyncio.sleep(1)
                await ctx.send("The domain has crumbled")
            else:
                dagon_id = dagon[ctx.guild.id]
                island_channel = discord.utils.get(ctx.guild.channels, id=dagon_id)
                await asyncio.sleep(1)
                await ctx.send(f"Due to the effects of the domain **{member.name}** has now been locked up in Dagon's Island for the next 5 minutes.")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(member, view_channel=False)

                await island_channel.set_permissions(member, view_channel=True)

                await asyncio.sleep(300)

                for channel in ctx.guild.channels:
                    await channel.set_permissions(member, overwrite=None)
                await island_channel.set_permissions(member, view_channel=False)

        elif domain == domains[7]:
            await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
            await ctx.send("https://tenor.com/view/jogo-jjk-jogoat-jogo-jjk-jujutsu-kaisen-gif-8418099397022761053")
            if member.top_role >= ctx.author.top_role:
                await asyncio.sleep(1)
                await ctx.send("The domain has crumbled")
            else:
                await asyncio.sleep(1)
                if ctx.guild.id not in self.jogo:
                    self.jogo[ctx.guild.id] = []
                self.jogo[ctx.guild.id].append(member.id)
                await ctx.send(f"Due to the effects of the domain **{member.name}** has now been surrounded by Lava for the next 5 minutes.")
                await asyncio.sleep(300)
                self.jogo[ctx.guild.id].remove(member.id)

        elif domain == domains[8]:
            await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
            await ctx.send("https://tenor.com/view/zenin-naoya-naoya-zenin-zenin-naoya-jujutsu-kaisen-gif-9815175286766632495")
            if member.top_role >= ctx.author.top_role:
                await asyncio.sleep(1)
                await ctx.send("The domain has crumbled")
            else:
                await asyncio.sleep(1)
                if ctx.guild.id not in self.naoya:
                    self.naoya[ctx.guild.id] = {}
                self.naoya[ctx.guild.id][member.id] = 1
                await ctx.send(f"Due to the effects of the domain the rules of 24fps have been applied to **{member.name}** for the next 10 minutes")
                await asyncio.sleep(600)
                del self.naoya[ctx.guild.id][member.id]

        elif domain == domains[9]:
            copy = random.choice(domains[0:9])
            await ctx.send(f"With the power of Mimicry **{ctx.author}** is displaying the powers of **{copy}**")
            await asyncio.sleep(1)

            if copy == domains[0]:
                await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
                await ctx.send("https://tenor.com/view/infinite-void-gojo-satoru-gojo-jjk-jujutsu-kaisen-gif-19219956")
                if member.top_role >= ctx.author.top_role:
                    await asyncio.sleep(1)
                    await ctx.send("The domain has crumbled")
                else:
                    newtime = datetime.timedelta(seconds=600)
                    await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                    await asyncio.sleep(1)
                    await ctx.send(
                        f"Due to the effects of the domain **{member.name}** is unable to move for 10 minutes")

            elif copy == domains[1]:
                await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
                await ctx.send(
                    f"https://tenor.com/view/sukuna-domain-expansion-jujustu-kaisen-shibuya-sukuna-vs-mahoraga-gif-3966585850028273519")
                if member.top_role >= ctx.author.top_role:
                    await asyncio.sleep(1)
                    await ctx.send("The domain has crumbled")
                else:
                    await member.remove_roles(member.top_role)
                    await asyncio.sleep(1)
                    await ctx.send(f"Due to effects of the domain **{member.name}** has lost their greatest strength")

            elif copy == domains[2]:
                await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
                await ctx.send(
                    "https://tenor.com/view/jjk-jujutsu-kaisen-mahito-jjk-fight-jujutsu-kaisen-fight-gif-693993311493234171")
                if member.top_role >= ctx.author.top_role:
                    await asyncio.sleep(1)
                    await ctx.send("The domain has crumbled")
                else:
                    await asyncio.sleep(1)
                    await member.edit(nick=f"Transfigured Human")
                    await ctx.send(f"Due to the effects of the domain **{member.name}** has lost their humanity")

            elif copy == domains[3]:
                await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
                await ctx.send(
                    f"https://tenor.com/view/hakari-kinji-kinji-hakari-hakari-kinji-kashimo-hajime-gif-15995875640514955845")
                if member.top_role >= ctx.author.top_role:
                    await asyncio.sleep(1)
                    await ctx.send("The domain has crumbled")
                else:
                    chance = random.randint(1, 10)
                    await asyncio.sleep(1)
                    message = await ctx.send("Attemping to attain Jackpot...")
                    async with ctx.typing():
                        await asyncio.sleep(5)
                    if chance == 5:
                        await asyncio.sleep(5)
                        await message.edit("Jackpot has been attained")
                        await ctx.send(
                            "https://tenor.com/view/hakari-hakari-kinji-kinji-hakari-kinji-jackpot-gif-12339332929838481118")
                        await asyncio.sleep(1)
                        await ctx.send(
                            f"Due to the effects of the domain **{member.name}** has been banished from the server")
                        await ctx.guild.ban(member)
                    else:
                        await ctx.send("Failed to attain jackpot")
            elif copy == domains[4]:
                await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
                await ctx.send("https://tenor.com/view/jujutsu-kaisen-hanami-gif-20361654")
                if member.top_role >= ctx.author.top_role:
                    await asyncio.sleep(1)
                    await ctx.send("The domain has crumbled")
                else:
                    await asyncio.sleep(1)
                    name = member.display_name
                    new_name = name[::-1]
                    await member.edit(nick=f"🌳{new_name}🌳")
                    await ctx.send(f"Due to the effects of the domain **{member.name}** has started sprouting")
            elif copy == domains[5]:
                await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
                await ctx.send(
                    "https://tenor.com/view/megumi-fushiguro-domain-expansion-ry%C5%8Diki-tenkai-chimera-shadow-garden-gif-25681375")
                if member.top_role >= ctx.author.top_role:
                    await asyncio.sleep(1)
                    await ctx.send("The domain has crumbled")
                else:
                    await asyncio.sleep(1)
                    if ctx.guild.id not in self.chimera:
                        self.chimera[ctx.guild.id] = []
                    self.chimera[ctx.guild.id].append(member.id)
                    await ctx.send(
                        f"Due to the effects of the domain **{member.name}** has drowned in the shadows for the next 3 minutes")
                    await asyncio.sleep(180)
                    self.chimera[ctx.guild.id].remove(member.id)
            elif copy == domains[6]:
                dagon = {1209560942841434142: 1226849314735783956, 1221289127547244594: 1226849791900913726, 1030538747827208322: 1226263040962465904, 1122290976938016792: 1228693777279881369}
                await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
                await ctx.send("https://tenor.com/view/jjk-season-2-dagon-gif-65005131711436483")
                if member.top_role >= ctx.author.top_role:
                    await asyncio.sleep(1)
                    await ctx.send("The domain has crumbled")
                else:
                    dagon_id = dagon[ctx.guild.id]
                    island_channel = discord.utils.get(ctx.guild.channels, id=dagon_id)
                    await asyncio.sleep(1)
                    await ctx.send(
                        f"Due to the effects of the domain **{member.name}** has now been locked up in Dagon's Island for the next 5 minutes.")
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(member, view_channel=False)

                    await island_channel.set_permissions(member, view_channel=True)

                    await asyncio.sleep(300)

                    for channel in ctx.guild.channels:
                        await channel.set_permissions(member, overwrite=None)
                    await island_channel.set_permissions(member, view_channel=False)

            elif copy == domains[7]:
                await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
                await ctx.send("https://tenor.com/view/jogo-jjk-jogoat-jogo-jjk-jujutsu-kaisen-gif-8418099397022761053")
                if member.top_role >= ctx.author.top_role:
                    await asyncio.sleep(1)
                    await ctx.send("The domain has crumbled")
                else:
                    await asyncio.sleep(1)
                    if ctx.guild.id not in self.jogo:
                        self.jogo[ctx.guild.id] = []
                    self.jogo[ctx.guild.id].append(member.id)
                    await ctx.send(
                        f"Due to the effects of the domain **{member.name}** has now been surrounded by Lava for the next 5 minutes.")
                    await asyncio.sleep(300)
                    self.jogo[ctx.guild.id].remove(member.id)
            elif copy == domains[8]:
                await ctx.send(f"{ctx.author.mention} has expanded their domain on {member.mention}")
                await ctx.send(
                    "https://tenor.com/view/zenin-naoya-naoya-zenin-zenin-naoya-jujutsu-kaisen-gif-9815175286766632495")
                if member.top_role >= ctx.author.top_role:
                    await asyncio.sleep(1)
                    await ctx.send("The domain has crumbled")
                else:
                    await asyncio.sleep(1)
                    if ctx.guild.id not in self.naoya:
                        self.naoya[ctx.guild.id] = {}
                    self.naoya[ctx.guild.id][member.id] = 1
                    await ctx.send(
                        f"Due to the effects of the domain the rules of 24fps have been applied to **{member.name}** for the next 10 minutes")
                    await asyncio.sleep(600)
                    del self.naoya[ctx.guild.id][member.id]

        elif domain == domains[10]:
            if ctx.author.id == 532631056856252436:
                await ctx.send(f"**{ctx.author}** has attained power which transcends the realm of humanity")
                await ctx.send(f"https://tenor.com/view/dragon-ball-dragon-ball-super-anime-goku-son-goku-gif-17723848")
                await asyncio.sleep(1)
                await ctx.send(
                    f"{ctx.author.mention} unleashes the overwhelming force of their godly ki on {member.mention}")
                await asyncio.sleep(1)
                await ctx.send(f"# KA")
                await asyncio.sleep(1)
                await ctx.send(f"# ME")
                await asyncio.sleep(1)
                await ctx.send(f"# HA")
                await asyncio.sleep(1)
                await ctx.send(f"# ME")
                await asyncio.sleep(1)
                await ctx.send("https://tenor.com/view/dragon-ball-super-goku-kamehameha-wave-gif-14323063")
                await member.remove_roles(member.top_role)
                newtime = datetime.timedelta(seconds=3600)
                await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                await ctx.send(
                    f"Due to being unable to handle **{ctx.author}'s** godly presence, **{member}** has been crippled for 1 hour "
                    f"and lost their greatest strength")

            else:
                await ctx.send("You are incapable of attaining this power")

        elif domain == domains[11]:
            if ctx.author.id == 768074971213725706:
                await ctx.send(f"**{ctx.author}** opens their heart up to **{member}**")
                await ctx.send(f"https://tenor.com/view/naruto-naruto-shippuden-sihouette-obito-gif-21952328")
                await asyncio.sleep(1)
                view = Talk(ctx, ctx.author, member)
                await ctx.send("Will you hear out their heartfelt request?", view=view)
            else:
                await ctx.send("Only those that have accepted their own hatred are capable of accepting the hatred of others.")
                await ctx.send("https://tenor.com/view/naruto-cool-gif-21575460")

        elif domain == domains[12]:
            users = [768074971213725706, 667792981742321674, 602246192491135008]
            if ctx.author.id in users:
                await ctx.send(f"**{ctx.author}** unleashes the full force of their conqueror's haki on the chat")
                await ctx.send("https://tenor.com/view/luffy-luffy-smile-one-piece-luffy-haki-gif-23016302")
                await asyncio.sleep(1)
                messages = [message async for message in ctx.history(limit=25)]
                authors = {message.author for message in messages}
                for author in authors:
                    if ctx.author.id == author.id:
                        print("ok")
                    elif author.id == 1034081315991080990:
                        print("ok")
                    elif ctx.guild.id in self.simple_domain:
                        if author.id in self.simple_domain[ctx.guild.id]:
                            await ctx.send(f"**{author.name}** has blocked off the haki using their simple domain")
                        else:
                            try:
                                newtime = datetime.timedelta(seconds=600)
                                await author.edit(timed_out_until=discord.utils.utcnow() + newtime)
                                await ctx.send(f"**{author.name}** has succumbed to the overwhelming pressure")
                            except:
                                await ctx.send(f"**{author.name}** has withstood the conqueror's haki")
                                continue
                    elif ctx.author.top_role > author.top_role:
                        try:
                            newtime = datetime.timedelta(seconds=600)
                            await author.edit(timed_out_until=discord.utils.utcnow() + newtime)
                            await ctx.send(f"**{author.name}** has succumbed to the overwhelming pressure")
                        except:
                            await ctx.send(f"**{author.name}** has withstood the conqueror's haki")
                            continue
                    else:
                        await ctx.send(f"**{author.name}** has withstood the conqueror's haki")
            else:
                await ctx.send("Only one in a million people possess the Colour of a King")
        elif domain == domains[13]:
            users = [696704031023693914]
            if ctx.author.id in users:
                await ctx.send(f"**{ctx.author}** unleashes their masterful swordsmanship on the **{member}**")
                await ctx.send(f"https://tenor.com/view/muichiro-demon-slayer-gif-8980385408939188978")
                if member.top_role >= ctx.author.top_role:
                    await asyncio.sleep(1)
                    await ctx.send("The domain has crumbled")
                else:
                    await asyncio.sleep(1)
                    name = member.display_name
                    new_name = ""
                    for letter in name:
                        new_name += f"/{letter}"
                    await member.edit(nick=new_name)
                    await ctx.send(f"**{member.name}** has been sliced up into pieces")
            else:
                await ctx.send("Fuck off, only 13 can use this")
        elif domain == domains[14]:
            tsukuyomi = {1030538747827208322: 1244706746946293902}
            access = [602246192491135008, 768074971213725706]
            in_tsukuyomi = []
            if ctx.author.id not in access:
                await ctx.send("You lack the visual prowess to use a genjutsu of this calibre")
            else:
                await ctx.send(f"{ctx.author.mention} has expanded their domain on the chat")
                await ctx.send("https://tenor.com/view/madara-infinite-tsukuyomi-naruto-remake-studio-pierrot-gif-26867770")
                tsukuyomi_id = tsukuyomi[ctx.guild.id]
                tsukuyomi_channel = discord.utils.get(ctx.guild.channels, id=tsukuyomi_id)
                messages = [message async for message in ctx.history(limit=25)]
                authors = {message.author for message in messages}
                for author in authors:
                    if ctx.author.id == author.id:
                        print("ok")
                    elif author.id == 1034081315991080990:
                        print("ok")
                    elif ctx.author.top_role > author.top_role:
                        await ctx.send(f"Due to the effects of the domain **{author.name}** has been sent to a World of Dreams for the next 5 minutes.")
                        for channel in ctx.guild.channels:
                            await channel.set_permissions(author, view_channel=False)

                        in_tsukuyomi.append(author.id)
                        await tsukuyomi_channel.set_permissions(author, view_channel=True)
                    elif ctx.guild.id in self.simple_domain:
                        if author.id in self.simple_domain[ctx.guild.id]:
                            await ctx.send(f"**{author.name}** has blocked off the genjutsu using their simple domain")
                    else:
                        await ctx.send(f"Due to the effects of the domain **{author.name}** has been sent to a World of Dreams for the next 5 minutes.")
                        in_tsukuyomi.append(author.id)
                        for channel in ctx.guild.channels:
                            await channel.set_permissions(author, view_channel=False)

                            await tsukuyomi_channel.set_permissions(author, view_channel=True)

                await asyncio.sleep(10)
                for victimid in in_tsukuyomi:
                    victim = discord.utils.get(ctx.guild.members, id=victimid)
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(victim, overwrite=None)
                    await tsukuyomi_channel.set_permissions(victim, view_channel=False)
        else:
            await ctx.send("Enter the correct domain name")

    @domainexpansion.error
    async def domainexpansion_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"Enter information in the format:\n ```g!de [member mention] [domain name] \nAvailable Domains: Infinite Void, Malevolent Shrine,"
                f"Self Embodiment of Perfection, Idle Death Gamble, Ceremonial Sea of Light, Chimera Shadow Garden, Horizon of the Captivating Skandha, Coffin of the Iron Mountain, Time Cell Moon Palace,"
                f" True Mutual Love"
                f"\nSpecial Domains: Kamehameha, Talk No Jutsu, Conquerors Haki, Mist Breathing, Infinite Tsukuyomi```")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have the permissions to use this command")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Due to an exhaustion of cursed technique, your domain is on a cooldown."
                           "Your cursed technique will return in **{:.2f}s**".format(error.retry_after))

    @commands.command()
    @commands.cooldown(1, 400, commands.BucketType.user)
    async def ai(self, ctx):
        if ctx.guild.id in self.ai:
            await ctx.send("Someone else is currently using the bot, wait till their session ends")
        else:
            await ctx.send("The chatbot has been enabled, type 'quit' if you want the bot to stop responding to you")
            self.ai[ctx.guild.id] = ctx.author.id

    @ai.error
    async def ai_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("Your cooldown will end after **{:.2f}s**".format(error.retry_after))

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kickai(self, ctx):
        if ctx.guild.id in self.ai:
            del self.ai[ctx.guild.id]
            await ctx.send("AI has been cleared")
        else:
            await ctx.send("No one is using the AI")


async def setup(bot):
    await bot.add_cog(casual(bot))
