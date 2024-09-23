import discord
from discord.ext import commands
import random


async def determine_winner(interaction, chosen, pick):
    user1_choice = pick[0]
    user2_choice = pick[1]
    mem1 = discord.utils.get(interaction.guild.members, id=chosen[0])
    mem2 = discord.utils.get(interaction.guild.members, id=chosen[1])
    if user1_choice == user2_choice:
        await interaction.followup.send(f"It is a tie")
    elif (user1_choice == 'rock' and user2_choice == 'scissors') or \
         (user1_choice == 'paper' and user2_choice == 'rock') or \
         (user1_choice == 'scissors' and user2_choice == 'paper'):
        await interaction.followup.send(f"**{mem1.name}** has won")
    elif (user2_choice == 'rock' and user1_choice == 'scissors') or \
         (user2_choice == 'paper' and user1_choice == 'rock') or \
         (user2_choice == 'scissors' and user1_choice == 'paper'):
        await interaction.followup.send(f"**{mem2.name}** has won")
    else:
        return "Computer wins!"


# noinspection PyUnresolvedReferences
class Choice(discord.ui.View):
    def __init__(self, author: discord.Member, member: discord.Member):
        super().__init__(timeout=30)
        self.author = author
        self.member = member
        self.chosen = []
        self.pick = []

    @discord.ui.button(label="Rock", style=discord.ButtonStyle.primary)
    async def rock(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.chosen:
            await interaction.response.send_message("You can't choose again", ephemeral=True)
        else:
            if self.author.id == interaction.user.id:
                self.chosen.append(self.author.id)
                self.pick.append("rock")
                await interaction.response.send_message("You chose Rock!", ephemeral=True)
            elif self.member.id == interaction.user.id:
                self.chosen.append(self.member.id)
                self.pick.append("rock")
                await interaction.response.send_message("You chose Rock!", ephemeral=True)
            else:
                await interaction.response.send_message("You cannot interact with this", ephemeral=True)
        if self.author.id in self.chosen and self.member.id in self.chosen:
            await determine_winner(interaction, self.chosen, self.pick)

    @discord.ui.button(label="Paper", style=discord.ButtonStyle.primary)
    async def paper(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.chosen:
            await interaction.response.send_message("You can't choose again", ephemeral=True)
        else:
            if self.author.id == interaction.user.id:
                self.chosen.append(self.author.id)
                self.pick.append("paper")
                await interaction.response.send_message("You chose Paper!", ephemeral=True)
            elif self.member.id == interaction.user.id:
                self.chosen.append(self.member.id)
                self.pick.append("paper")
                await interaction.response.send_message("You chose Paper!", ephemeral=True)
            else:
                await interaction.response.send_message("You cannot interact with this", ephemeral=True)
        if self.author.id in self.chosen and self.member.id in self.chosen:
            await determine_winner(interaction, self.chosen, self.pick)

    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.primary)
    async def scissors(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.chosen:
            await interaction.response.send_message("You can't choose again", ephemeral=True)
        else:
            if self.author.id == interaction.user.id:
                self.chosen.append(self.author.id)
                self.pick.append("scissors")
                await interaction.response.send_message("You chose Scissors!", ephemeral=True)
            elif self.member.id == interaction.user.id:
                self.chosen.append(self.member.id)
                self.pick.append("scissors")
                await interaction.response.send_message("You chose Scissors!", ephemeral=True)
            else:
                await interaction.response.send_message("You cannot interact with this", ephemeral=True)
        if self.author.id in self.chosen and self.member.id in self.chosen:
            await determine_winner(interaction, self.chosen, self.pick)


class RPS(discord.ui.View):
    def __init__(self, author: discord.Member, member: discord.Member):
        super().__init__(timeout=30)
        self.value = None
        self.member = member
        self.author = author

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id != interaction.user.id:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f"You are not {self.member.name}", ephemeral=True)
        else:
            option = Choice(self.author, self.member)
            embed = discord.Embed(title="Rock Paper Scissors", colour=discord.Colour.blurple())
            embed.add_field(name="Choose your option", value=f"Rock: 🪨\nPaper: 📄\nScissors: ✂️")
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(embed=embed, view=option)
            await interaction.message.delete()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.id != interaction.user.id:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f"You are not {self.member.name}", ephemeral=True)
        else:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message("You have denied it", ephemeral=True)
            await interaction.message.delete()


class games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gay(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
        chance = random.randint(0, 199)
        if chance == 100:
            await ctx.send("https://tenor.com/view/vegeta-dragon-ball-z-unlimited-power-over9000-power-level-gif-12316102")
        else:
            per = random.randint(0, 100)
            embed = discord.Embed(title="Gay Rate", colour=discord.Colour.blue())
            embed.add_field(name="", value=f"{member.mention} is {per}% gay 🌈")
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx):
        responses = ["It is certain.", "It is decidedly so.", "Without a doubt", "Definitely", "Yes",
                     "You may rely on it",
                     "As I see it, yes", "Most likely", "Outlook good", "Signs point to yes.",
                     "Ask again later", "Better not tell you now", "Concentrate and ask again.",
                     "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.",
                     "Very doubtful."]

        await ctx.send(f"{random.choice(responses)}")

    @commands.command()
    async def flip(self, ctx):
        flip = random.choice(['Heads', 'Tails'])
        await ctx.send(flip)

    @commands.command()
    async def poll(self, ctx, *args):
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        poll = ''
        for i in args:
            poll += f" {i}"
        print(poll)
        poll_data = poll.split("'")
        print(poll_data)
        fresh_data = [poll_data[0]]
        for i in range(1, len(poll_data), 2):
            fresh_data.append(poll_data[i])
        print(fresh_data)
        embed = discord.Embed(title=f"{poll_data[0]}", colour=discord.Colour.blue(), timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        for i in range(1, len(fresh_data)):
            embed.add_field(name="", value=f"{emojis[i-1]} {fresh_data[i]}\n", inline=False)
        message = await ctx.send(embed=embed)
        for i in range(len(fresh_data)-1):
            await message.add_reaction(emojis[i])

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Enter information in the format:\n ```g!poll [title] '[option 1]' '[option 2]'...```")

    @commands.command()
    async def rps(self, ctx, member: discord.Member):
        if member == ctx.author:
            await ctx.send("You can't play with yourself")
        view = RPS(ctx.author, member)
        await ctx.send(f"{member.mention} has been challenged to a game of rock-paper-scissors by {ctx.author.mention}"
                       f"\nDo you accept?", view=view)

    @rps.error
    async def rps_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please enter the data correctly")


async def setup(bot):
    await bot.add_cog(games(bot))
