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
        self.client = OpenAI(api_key=open("openai_token.txt", "r").read().strip())
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

    @commands.command(help="🏓 Pong! Check if I'm alive and kicking with my response time!")
    async def ping(self, ctx):
        await ctx.send(f"The ping is {round(self.bot.latency * 1000)}ms")

    @commands.command(help="🎭 Get the lowdown on any user! Shows their roles, join date, and more fun facts! 📊")
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

    @commands.command(help="🏰 Server stats at your fingertips! Get all the juicy details about our awesome community! 📈")
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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("I do not have any such command!\nType g!help to view available commands")

    @commands.command(help="💤 Going AFK? Let everyone know! I'll tell them you're away when they mention you 🌙")
    async def afk(self, ctx, *, reason=None):
        if ctx.guild.id not in self.data:
            self.data[ctx.guild.id] = []
        msg = " ".join(args)
        self.data[ctx.guild.id].append(ctx.author.id)
        self.data[ctx.guild.id].append(msg)
        await ctx.send("Afk set!")
        await ctx.author.edit(nick=f"[AFK] {ctx.author.display_name}")

    @commands.command(help="ℹ️ Add some cool info to your profile! Make yourself stand out from the crowd! ✨")
    async def inf(self, ctx, *, information):
        if ctx.guild.id not in self.inf:
            self.inf[ctx.guild.id] = []
        self.inf[ctx.guild.id].append(ctx.author.id)
        await ctx.send("You have now passively enabled infinity, you are now untouchable")
        await ctx.send("https://tenor.com/view/jujutsu-kaisen-gojo-satoru-vs-gif-21280734")
        try:
            await ctx.author.edit(nick=f"[INF] {ctx.author.display_name}")
        except:
            print("Owner Nickname")

    @commands.command(help="🗑️ Want to remove your profile info? No problemo! Clean slate coming right up! 🧹")
    async def removeinf(self, ctx):
        self.inf[ctx.guild.id].remove(ctx.author.id)
        await ctx.send("Your infinity has been turned off manually")
        await ctx.send("Infinity Removed")
        new_nick = ctx.author.display_name.split("[INF]")
        await ctx.author.edit(nick=new_nick[1])

    @commands.command(help="🎯 Set your simple domain! Show off your specialty in style! 🌟")
    async def simpledomain(self, ctx, *, domain):
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

    @commands.command(help="💌 Send a message through me! I'm your friendly neighborhood messenger bot! 📨")
    async def message(self, ctx, member: discord.Member, *, message):
        msg = " ".join(arg)
        await member.send(f"{ctx.author.display_name} left a message for you \n > {msg}")
        await ctx.channel.purge(limit=1)
        await ctx.send("Message sent!")

    @message.error
    async def message_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"Cannot send messages to this user")

    @commands.command(help="🖼️ Want to see someone's avatar in all its glory? I'll make it bigger and better! 🔍")
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

    @commands.command(help="📬 Send a DM to all members! Use with caution - it's super powerful! 💫")
    async def dmall1(self, ctx, *, message):
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

    @commands.command(help="📫 Another way to DM all members! Different style, same awesome power! 🌠")
    async def dmall2(self, ctx, *, message):
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

    @commands.command(help="🔧 Need something fixed? I'm your bot! Let me help you sort things out! 🛠️")
    async def fix(self, ctx):
        island_channel = discord.utils.get(ctx.guild.channels, id=1226849314735783956)
        for channel in ctx.guild.channels:
            await channel.set_permissions(member, overwrite=None)
        await island_channel.set_permissions(member, view_channel=False)

    @commands.command(help="👀 Catch those deleted messages! I remember what others try to forget! 🕵️")
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

    @commands.command(help="⚔️ Domain Expansion! Channel your inner Jujutsu Kaisen sorcerer! 🔮")
    async def domainexpansion(self, ctx):
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
            await ctx.send("https://tenor.com/view/megumi-fushiguro-