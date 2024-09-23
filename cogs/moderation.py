import discord
from discord.ext import commands
import asyncio
import json
import datetime
import time


async def reporter(ctx, author, member, reason, intensity):
    with open("reports.json", "w+") as f:
        data = json.load(f)
        data[str(member.id)] = [reason, author.id, f"<t:{int(time.time())}:R>", intensity]
        json.dump(data, f)
    await ctx.send("Good")


class Report(discord.ui.View):
    def __init__(self, ctx, author: discord.Member, member: discord.Member, reason):
        super().__init__(timeout=30)
        self.value = None
        self.ctx = ctx
        self.member = member
        self.author = author
        self.reason = reason

    @discord.ui.button(label="Light", style=discord.ButtonStyle.green)
    async def light(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.author.id != interaction.user.id:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f"You are not {self.member.name}", ephemeral=True)

    @discord.ui.button(label="Medium", style=discord.ButtonStyle.blurple)
    async def medium(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.author.id != interaction.user.id:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f"You are not {self.member.name}", ephemeral=True)

    @discord.ui.button(label="Hard", style=discord.ButtonStyle.red)
    async def hard(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.author.id != interaction.user.id:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f"You are not {self.member.name}", ephemeral=True)
        else:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message("You have denied it", ephemeral=True)
            await interaction.message.delete()


class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Deleted {amount} messages!")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please specify the amount of messages to delete")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have the permissions to use this command")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason=None):
        if member == self.bot.user:
            await ctx.send(f"You cannot kick me")
        elif member == ctx.author:
            await ctx.send(f"You cannot kick yourself")
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(f"This person's role is equal or higher than yours.")
        else:
            await ctx.guild.kick(member, reason=reason)
            await ctx.send(f"Kicked {member}")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please specify who to kick")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have the permissions to use this command")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
        if member == self.bot.user:
            await ctx.send(f"https://tenor.com/view/jjk-gif-20669871")
        elif member == ctx.author:
            await ctx.send(f"You cannot ban yourself")
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(f"This person's role is equal or higher than yours.")
        else:
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f"Banned {member}")

    @ban.error
    async def ban_error(self, ctx, error):
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

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: commands.MemberConverter, *, duration: DurationConverter):
        if member == self.bot.user:
            await ctx.send(f"You cannot ban me")
        elif member == ctx.author:
            await ctx.send(f"You cannot ban yourself")
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(f"This person's role is equal or higher than yours.")
        else:
            multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400}
            amount, unit = duration
            await member.send(f"You have been banned in **{ctx.guild.name}** for **{amount}{unit}**")
            await ctx.guild.ban(member)
            await ctx.send(f"Banned **{member}** for **{amount}{unit}**")
            await asyncio.sleep(amount * multiplier[unit])
            await ctx.guild.unban(member)
            await member.send("You have been unbanned")

    @tempban.error
    async def tempban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please specify who to temporarily ban")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have the permissions to use this command")

    @commands.command(help="Enter the discord id of who you want to unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        if member == self.bot.user.id:
            await ctx.send(f"You cannot unban me")
        elif member == ctx.author.id:
            await ctx.send(f"You cannot unban yourself")
        else:
            banned_users = ctx.guild.bans()
            async for ban_entry in banned_users:
                user = ban_entry.user
                print(user.id)
                print(member)
                if str(user.id) == str(member):
                    print(1)
                    await ctx.guild.unban(user)
                    await ctx.send(f"Unbanned {user.mention}")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please specify the id of who to unban")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have the permissions to use this command")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, duration, *reason):
        if member == self.bot.user:
            await ctx.send(f"You cannot mute me")
        elif member == ctx.author:
            await ctx.send(f"You cannot mute yourself")
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(f"This person's role is equal or higher than yours.")
        else:
            multiplier = {"s": 1, "m": 60, "h": 3600, "d": 86400}
            amount = duration[:-1]
            unit = duration[-1]

            if amount.isdigit() and unit in ["s", "m", "h", "d"]:
                amount = int(amount)
                print(unit, amount)
                print(int(amount*multiplier[unit]))
                newtime = datetime.timedelta(seconds=int(amount * multiplier[unit]))
                await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                if reason == ():
                    embed = discord.Embed(description=f"🔇 {member.name} has been muted for **{amount}{unit}** | No reason specified", colour=discord.Colour.blue())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(description=f"🔇 {member.name} has been muted for **{amount}{unit}** | {' '.join(reason)}", colour=discord.Colour.blue())
                    await ctx.send(embed=embed)
            else:
                await ctx.send("Specify the duration appropriately.")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Enter information in the format:\n ```g!mute [duration] [reason]```")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have the permissions to use this command")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        if member == self.bot.user:
            await ctx.send(f"You cannot unmute me")
        elif member == ctx.author:
            await ctx.send(f"You cannot unmute yourself")
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(f"This person's role is equal or higher than yours.")
        else:
            newtime = datetime.timedelta(seconds=1)
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
            await ctx.send(f"{member} was Unmuted")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please specify who to unmute")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have the permissions to use this command")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def giverole(self, ctx, member: discord.Member, role=None):
        give_role = discord.utils.get(ctx.guild.roles, name=role)
        if member == self.bot.user:
            await ctx.send(f"You cannot give a role to me")
        elif role is None:
            await ctx.send("Specify which role to give")
        elif give_role > ctx.author.top_role:
            await ctx.send(f"You cannot give someone a higher role than yourself")
        elif member.top_role > ctx.author.top_role:
            await ctx.send(f"This person's role is higher than yours.")
        else:

            await member.add_roles(give_role)
            await ctx.send("Role given")

    @giverole.error
    async def giverole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please specify who to give roles to")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have the permissions to use this command")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removerole(self, ctx, member: discord.Member, role=None):
        give_role = discord.utils.get(ctx.guild.roles, name=role)
        if member == self.bot.user:
            await ctx.send(f"You cannot remove my roles")
        elif role is None:
            await ctx.send("Specify which role to remove")
        elif give_role not in member.roles:
            await ctx.send(f"You cannot remove a role you don't have")
        elif member.top_role >= ctx.author.top_role:
            await ctx.send(f"This person's role is equal or higher than yours.")
        else:
            await member.remove_roles(give_role)
            await ctx.send("Role Removed")

    @removerole.error
    async def removerole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please specify whose role to remove")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have the permissions to use this command")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def createrole(self, ctx, role):
        await ctx.guild.create_role(name=role)
        await ctx.send("Role created")

    @createrole.error
    async def createrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please specify the name of the role you wish to create")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have the permissions to use this command")

    @commands.command(aliases=["inrole"])
    async def members(self, ctx, *, role1: discord.Role):
        role = discord.utils.get(ctx.guild.roles, name=f"{role1.name}")
        l = []
        if role is None:
            await ctx.send(f'There is no "{role1}" role on this server!')
            return
        for member in ctx.guild.members:
            if role1 in member.roles:
                l.append(f"{member.mention}({member})")
        if len(l) == 0:
            await ctx.send(f"Nobody has the role {role1}")
        else:
            res2 = "\n".join(l)
            embed = discord.Embed(title=f"Members in {role1.name}", description=f"{res2}", colour=discord.Colour.blue())
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['warn'])
    @commands.has_permissions(kick_members=True)
    async def report(self, ctx, member: discord.Member, *reason):
        channel = discord.utils.get(ctx.guild.channels, id=1227717178564939886)
        role = discord.utils.get(ctx.guild.roles, id=1213088016709591101)
        if reason == ():
            await ctx.send("Enter a valid reason for the report")
        else:
            if role in member.roles:
                await ctx.send("They are already muted")
            else:
                if member.top_role >= ctx.author.top_role:
                    await ctx.send("You cannot report yourself or someone higher than yourself")
                else:
                    if member.guild_permissions >= ctx.author.guild_permissions:
                        await ctx.send("You cannot report another administrator or yourself")
                    else:
                        id = str(member.id)
                        reason = " ".join(reason)
                        with open('report.json', 'r') as f:
                            data = json.load(f)
                        if id in data:
                            print("a")
                            data[id].append([reason, ctx.author.id])
                            with open('report.json', 'w') as p:
                                json.dump(data, p)
                        else:
                            print("b")
                            data[id] = {}
                            data[id] = [[reason, ctx.author.id]]
                            with open('report.json', 'w') as p:
                                json.dump(data, p)
                        with open('report.json', 'r+') as f:
                            data = json.load(f)
                        reports = len(data[id])

                        if reports == 1:
                            newtime = datetime.timedelta(seconds=3600)
                            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                            await ctx.send(f"{member.mention} has 1 report against them, they have been muted for **1 hour**. Another report will result in a **24 hour** mute")
                            embed = discord.Embed(title="Report Log", colour=discord.Colour.red(), timestamp=ctx.message.created_at)
                            embed.set_thumbnail(url=member.avatar.url)
                            embed.set_author(name=f"{member}")
                            embed.add_field(name=f"Report {reports}/5", value=f"{member} has been muted for 1 hour", inline=False)
                            embed.add_field(name=f"", value=f"Reason: '{reason}' by {ctx.author.mention}", inline=False)
                            # noinspection PyArgumentList
                            await channel.send(embed=embed)
                        elif reports == 2:
                            newtime = datetime.timedelta(seconds=86400)
                            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                            await ctx.send(
                                f"{member.mention} has 2 reports against them, they have been muted for **6 hours**. Another report will result in a **3 day** mute")
                            embed = discord.Embed(title="Report Log", colour=discord.Colour.red(), timestamp=ctx.message.created_at)
                            embed.set_thumbnail(url=member.avatar.url)
                            embed.set_author(name=f"{member}")
                            embed.add_field(name=f"Report {reports}/5", value=f"{member} has been muted for 6 hours",
                                            inline=False)
                            embed.add_field(name=f"", value=f"Reason: '{reason}' by {ctx.author.mention}", inline=False)
                            # noinspection PyArgumentList
                            await channel.send(embed=embed)
                        elif reports == 3:
                            newtime = datetime.timedelta(seconds=259200)
                            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                            await ctx.send(
                                f"{member.mention} has 3 reports against them, they have been muted for **24 hours**. Another report will result in a **1 week** mute")
                            embed = discord.Embed(title="Report Log", colour=discord.Colour.red(), timestamp=ctx.message.created_at)
                            embed.set_thumbnail(url=member.avatar.url)
                            embed.set_author(name=f"{member}")
                            embed.add_field(name=f"Report {reports}/5", value=f"{member} has been muted for 24 hours",
                                            inline=False)
                            embed.add_field(name=f"", value=f"Reason: '{reason}' by {ctx.author.mention}", inline=False)
                            # noinspection PyArgumentList
                            await channel.send(embed=embed)
                        elif reports == 4:
                            newtime = datetime.timedelta(seconds=604800)
                            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
                            await ctx.send(
                                f"{member.mention} has 4 reports against them, they have been muted for **1 week**. Another report will result in a **permanent** ban")
                            embed = discord.Embed(title="Report Log", colour=discord.Colour.red(),
                                                  timestamp=ctx.message.created_at)
                            embed.set_thumbnail(url=member.avatar.url)
                            embed.set_author(name=f"{member}")
                            embed.add_field(name=f"Report {reports}/5", value=f"{member} has been muted for 1 week",
                                            inline=False)
                            embed.add_field(name=f"", value=f"Reason: '{reason}' by {ctx.author.mention}", inline=False)
                            # noinspection PyArgumentList
                            await channel.send(embed=embed)
                        elif reports >= 5:
                            await member.send("You have been permanently banned for reaching 5 reports")
                            await ctx.guild.ban(member)
                            await ctx.send(f"{member.mention} has 5 reports against them, they have been permanently banned")
                            embed = discord.Embed(title="Report Log", colour=discord.Colour.red(), timestamp=ctx.message.created_at)
                            embed.set_thumbnail(url=member.avatar.url)
                            embed.set_author(name=f"{member}")
                            embed.add_field(name=f"Report {reports}/5", value=f"{member} has been muted for permanently banned",
                                            inline=False)
                            embed.add_field(name=f"", value=f"Reason: '{reason}' by {ctx.author.mention}", inline=False)
                            # noinspection PyArgumentList
                            await channel.send(embed=embed)
                        else:
                            await ctx.send("Error!")

    @report.error
    async def report_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Enter information in the format:\n ```g!report [member mention] [reason]```")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have the permissions to use this command")

    @commands.command(aliases=['reports'])
    async def profile(self, ctx, member: discord.Member = None, member_id: int = None):
        if member is None and member_id is None:
            member = ctx.author

        target_member = self.bot.get_user(member_id) if member_id else member

        if target_member is None:
            await ctx.send("Member not found.")
            return
        with open("report.json", "r") as f:
            data = json.load(f)
        id = str(member.id)
        embed = discord.Embed(colour=member.colour, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_author(name=f"{member}")
        if id not in data or data[id] == []:
            embed.add_field(name=f"Profile", value=f"Reports: 0", inline=False)
            embed.add_field(name=f"Reports History:", value="None", inline=False)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            reasons = []
            for i in range(len(data[id])):
                reasons.append([i, data[id][i]])
            print(reasons)
            embed.add_field(name=f"Profile", value=f"Reports: {len(data[id])}", inline=False)
            reports = []
            for i in range(len(reasons)):
                reports.append(f"{i+1}. Reason: '{reasons[i][1][0]}'\n by **<@{reasons[i][1][1]}>**")
            embed.add_field(name=f"Reports History:", value="\n".join(reports), inline=False)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def delete(self, ctx, member: discord.Member, number):
        channel = discord.utils.get(ctx.guild.channels, id=1227717178564939886)
        id = str(member.id)
        with open("report.json", "r") as f:
            data = json.load(f)
        if len(data[id]) == 0:
            await ctx.send("This person has no reports against them")
        else:
            if number == "all":
                reasons = []
                for i in range(len(data[id])):
                    reporter = discord.utils.get(ctx.guild.members, id=data[id][i][1])
                    if reporter.top_role > ctx.author.top_role:
                        await ctx.send(f"Failed to delete Report No. {i+1} since it was done by someone ranked higher than you")
                        pass
                    else:
                        reasons.append([i, data[id][i]])
                print(reasons)
                embed = discord.Embed(colour=discord.Colour.red(), timestamp=ctx.message.created_at)
                embed.set_thumbnail(url=member.avatar.url)
                embed.set_author(name=f"{member}")
                reports = []
                for i in range(len(reasons)):
                    reports.append(f"{i + 1}. Reason: '{reasons[i][1][0]}'\n by **<@{reasons[i][1][1]}>**")
                embed.add_field(name=f"Reports Deleted:", value="\n".join(reports), inline=False)
                embed.set_footer(text=f"Deleted by {ctx.author}", icon_url=ctx.author.avatar.url)
                # noinspection PyArgumentList
                await channel.send(embed=embed)
                for i in range(len(reasons)):
                    data[id].remove(reasons[i][1])
                with open("report.json", "w") as f:
                    json.dump(data, f)
                await ctx.send("All their possible reports were deleted")
            elif len(data[id]) < int(number)-1:
                await ctx.send("This report number isn't in their reports")
            else:
                print(len(data[id]))
                number = int(number)-1
                print(number)
                reporter = discord.utils.get(ctx.guild.members, id=data[id][number][1])
                if reporter.top_role > ctx.author.top_role:
                    await ctx.send("This report was done by someone of a higher rank than you, you cannot delete their report")
                else:
                    embed = discord.Embed(colour=discord.Colour.red(), timestamp=ctx.message.created_at)
                    embed.set_thumbnail(url=member.avatar.url)
                    embed.set_author(name=f"{member}")
                    embed.add_field(name=f"Reports Deleted:", value=f"{number + 1}. Reason: '{data[id][number][0]}'\n by **<@{data[id][number][1]}>**", inline=False)
                    embed.set_footer(text=f"Deleted by {ctx.author}", icon_url=ctx.author.avatar.url)
                    # noinspection PyArgumentList
                    await channel.send(embed=embed)
                    del data[id][number]
                    with open("report.json", "w") as f:
                        json.dump(data, f)
                    await ctx.send("Report deleted")

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Enter information in the format:\n ```g!delete [member mention/id] [number of report]\nor\ng!delete [member mention/id] [all]```")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You do not have the permissions to use this command")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def nr(self, ctx, member: discord.Member, *reason):
        channel = discord.utils.get(ctx.guild.channels, id=1227717178564939886)
        if reason == ():
            await ctx.send("Enter a valid reason for the report")
            return
        if member.top_role >= ctx.author.top_role:
            await ctx.send("You cannt report yourself or someone higher than yourself")
            return
        if member.guild_permissions >= ctx.author.guild_permissions:
            await ctx.send("You cannot report another administrator or yourself")
            return
        id = str(member.id)
        reason = " ".join(reason)
        with open('report.json', 'r') as f:
            data = json.load(f)
        if id not in data:
            print("a")
            data[id] = {}
            with open('report.json', 'w') as p:
                json.dump(data, p)
        view = Report(ctx, ctx.author, member, reason)
        embed = discord.Embed(title=f"Report: {member.name}", colour=discord.Colour.red(), timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name=f"Reason:", value=f"{reason}", inline=False)
        embed.add_field(name=f"Reported by:", value=f"{ctx.author.mention}", inline=False)
        await ctx.send("Choose the intensity of the report", embed=embed, view=view)
        await ctx.send(f"<t:{int(time.time())}:R>")


async def setup(bot):
    await bot.add_cog(moderation(bot))
