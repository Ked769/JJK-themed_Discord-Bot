import discord
from discord.ext import commands
import asyncio
from PIL import Image
import json
import random
import os
import passives

move = {}
fight_key = {}
domain = {}
active_domain = {}
black_flash = {}
black_flash_users = ["Yuji", "Yuji-awk"]
battles = {"11": "Ko-guy", "12": "Kechizu", "13": "Eso", "14": "Rika", "15": "Hanami"}

sets = open("characters.json", "r")
character_data = json.load(sets)

mindful = open("curse_data.json", "r")
curse_data = json.load(mindful)


def calculate_xp_for_next_level(level):
    return 2 ** (level - 1) * 100


async def fight2(ctx, char, bot, key):
    with open("profile_data.json", "r") as p:
        profile_data = json.load(p)

    global dmg1, dmg2
    members = list(move[key].keys())
    member1_id = members[0]
    data = profile_data[str(member1_id)]["Characters"][char[member1_id]]

    quest = str(profile_data[str(member1_id)]["Chapter"]) + str(profile_data[str(member1_id)]["Mission"])

    ability1 = character_data[char[member1_id]]["Moves"]
    ability2 = character_data[char["ai"]]["Moves"]

    hp1 = move[key][member1_id][1]
    hp2 = move[key]["ai"][1]

    member1 = discord.utils.get(ctx.guild.members, id=member1_id)

    name1 = move[key][member1.id][-1]
    name2 = move[key]["ai"][-1]

    print(fight_key[key])

    taken1 = random.randint(1, 10)
    taken2 = random.randint(1, 10)

    chance1 = []
    if name1 == "Ultimate":
        chance1 = [taken1]
    else:
        for i in range(ability1[name1][1]+1):
            chance1.append(i)
    chance2 = []
    if name2 == "Ultimate":
        chance2 = [taken2]
    else:
        for i in range(ability2[name2][1]+1):
            chance2.append(i)

    embed = discord.Embed(title=f"{member1.name} vs {char['ai']}", colour=discord.Colour.blue())
    if name1 == "Ultimate" and name2 == "Ultimate":
        active_domain[key] = True
        choose = random.randint(1, 2)
        if choose == 1:
            domain[key] = [member1.id, char[member1.id]]
            embed.add_field(name=f"{move[key][member1.id][0]} has used their Ultimate", value=f"The battlefield has now shifted in their favour")
            embed.add_field(name=f"{move[key]['ai'][0]} has used their Ultimate", value=f"They have lost the clash")
            await ctx.send(character_data[char[member1.id]]["Ultimate"][1])
        else:
            domain[key] = ['ai', char['ai']]
            embed.add_field(name=f"{move[key][member1.id][0]} has used their Ultimate", value=f"They have lost the clash")
            embed.add_field(name=f"{move[key]['ai'][0]} has used their Ultimate", value=f"The battlefield has now shifted in their favour")
            await ctx.send(character_data[char['ai']]["Ultimate"][1])
    elif name1 == "Ultimate":
        active_domain[key] = True
        domain[key] = [member1.id, char[member1.id]]
        embed.add_field(name=f"{move[key][member1.id][0]} has used their Ultimate", value=f"The battlefield has now shifted in their favour")
        await ctx.send(character_data[char[member1.id]]["Ultimate"][1])
        dmg2 = int(ability2[name2][0] * (1+curse_data[quest]["Stats"][1]*0.05) * character_data[char['ai']]["Stats"][1])
        value2 = f"{move[key]['ai'][-1]} has dealt {dmg2} damage!"
        if active_domain[key]:
            if domain[key][0] == 'ai':
                chance2 = [taken2]
                dmg2 = int(dmg2*1.2)
                value2 = f"{move[key]['ai'][-1]} has dealt {dmg2} damage!"
        if passives.flames_passive(char[member1.id]):
            value2 += f"\n{char['ai']} has been scorched for 40dmg"
            hp2 -= 40
        if taken2 in chance2:
            if char['ai'] == "Yuji":
                dmg2 = int(dmg2*black_flash[key]['ai'])
                value2 = f"{move[key]['ai'][-1]} has dealt {dmg2} damage!"
            if move[key]['ai'][-1] == "Black Flash":
                black_flash[key]['ai'] += 0.15
            print(passives.infinity_passive(char[member1.id]))
            if passives.infinity_passive(char[member1.id]):
                value2 = "The attack has been blocked by infinity"
                dmg2 = 0
            if passives.yata_passive(char[member1.id]):
                value2 = "The attack has been blocked by Yata no Kagami"
                dmg2 = 0
            if char['ai'] == "Sung-jin-woo":
                hp2 = int(hp2 + dmg2 * 0.2)
            if char[member1.id] == "Ichigo":
                dmg2 = int(dmg2-dmg2*0.2)
                value2 = f"{move[key]['ai'][-1]} has dealt {dmg2} damage!"
            embed.add_field(name=f"{move[key]['ai'][0]} has used {move[key]['ai'][-1]}", value=value2)
            hp1 = hp1-dmg2
        else:
            embed.add_field(name=f"{move[key]['ai'][0]} has used {move[key]['ai'][-1]}", value=f"The attack has missed")
    elif name2 == "Ultimate":
        active_domain[key] = True
        domain[key] = ['ai', char['ai']]
        embed.add_field(name=f"{move[key]['ai'][0]} has used their Ultimate", value=f"The battlefield has now shifted in their favour")
        await ctx.send(character_data[char['ai']]["Ultimate"][1])
        dmg1 = int(ability1[name1][0] * (1+data['Stats'][1]*0.05) * character_data[char[member1.id]]["Stats"][1])
        value1 = f"{move[key][member1.id][-1]} has dealt {dmg1} damage!"
        if active_domain[key]:
            if domain[key][0] == member1.id:
                chance1 = [taken1]
                dmg1 = int(dmg1*1.2)
                value1 = f"{move[key][member1.id][-1]} has dealt {dmg1} damage!"
        if passives.flames_passive(char['ai']):
            value1 += f"\n{char[member1.id]} has been scorched for 40dmg"
            hp1 -= 40
        if taken1 in chance1:
            if char[member1.id] in black_flash_users:
                dmg1 = int(dmg1*black_flash[key][member1.id])
                value1 = f"{move[key][member1.id][-1]} has dealt {dmg1} damage!"
            if move[key][member1.id][-1] == "Black Flash":
                black_flash[key][member1.id] += 0.15
            print(passives.infinity_passive(char['ai']))
            if passives.infinity_passive(char['ai']):
                value1 = "The attack has been blocked by infinity"
                dmg1 = 0
            if passives.yata_passive(char['ai']):
                value1 = "The attack has been blocked by Yata no Kagami"
                dmg1 = 0
            if char[member1.id] == "Sung-jin-woo":
                hp1 = int(hp1 + dmg1 * 0.2)
            if char['ai'] == "Ichigo":
                dmg1 = int(dmg1-dmg1*0.2)
                value1 = f"{move[key][member1.id][-1]} has dealt {dmg1} damage!"
            embed.add_field(name=f"{move[key][member1.id][0]} has used {move[key][member1.id][-1]}", value=value1)
            hp2 = hp2-dmg1
        else:
            embed.add_field(name=f"{move[key][member1.id][0]} has used {move[key][member1.id][-1]}", value=f"The attack has missed!")
    else:
        dmg1 = int(ability1[name1][0] * (1+data['Stats'][1]*0.05) * character_data[char[member1.id]]["Stats"][1])
        value1 = f"{move[key][member1.id][-1]} has dealt {dmg1} damage!"
        if active_domain[key]:
            if domain[key][0] == member1.id:
                chance1 = [taken1]
                dmg1 = int(dmg1*1.2)
                value1 = f"{move[key][member1.id][-1]} has dealt {dmg1} damage!"
        if passives.flames_passive(char['ai']):
            value1 += f"\n{char[member1.id]} has been scorched for 40dmg"
            hp1 -= 40
        if taken1 in chance1:
            if char[member1.id] in black_flash_users:
                dmg1 = int(dmg1*black_flash[key][member1.id])
                value1 = f"{move[key][member1.id][-1]} has dealt {dmg1} damage!"
            if move[key][member1.id][-1] == "Black Flash":
                black_flash[key][member1.id] += 0.15
            print(passives.infinity_passive(char['ai']))
            if passives.infinity_passive(char['ai']):
                value1 = "The attack has been blocked by infinity"
                dmg1 = 0
            if passives.yata_passive(char['ai']):
                value1 = "The attack has been blocked by Yata no Kagami"
                dmg1 = 0
            if char[member1.id] == "Sung-jin-woo":
                hp1 = int(hp1 + dmg1 * 0.2)
            if char['ai'] == "Ichigo":
                dmg1 = int(dmg1-dmg1*0.2)
                value1 = f"{move[key][member1.id][-1]} has dealt {dmg1} damage!"
            embed.add_field(name=f"{move[key][member1.id][0]} has used {move[key][member1.id][-1]}", value=value1)
            hp2 = hp2-dmg1
        else:
            embed.add_field(name=f"{move[key][member1.id][0]} has used {move[key][member1.id][-1]}", value=f"The attack has missed!")
        dmg2 = int(ability2[name2][0] * (1 + curse_data[quest]["Stats"][1]*0.05) * character_data[char['ai']]["Stats"][1])
        value2 = f"{move[key]['ai'][-1]} has dealt {dmg2} damage!"
        if active_domain[key]:
            if domain[key][0] == 'ai':
                chance2 = [taken2]
                dmg2 = int(dmg2*1.2)
                value2 = f"{move[key]['ai'][-1]} has dealt {dmg2} damage!"
        if passives.flames_passive(char[member1.id]):
            value2 += f"\n{char['ai']} has been scorched for 40dmg"
            hp2 -= 40
        if taken2 in chance2:
            if char['ai'] in black_flash_users:
                dmg2 = int(dmg2*black_flash[key]['ai'])
                value2 = f"{move[key]['ai'][-1]} has dealt {dmg2} damage!"
            if move[key]['ai'][-1] == "Black Flash":
                black_flash[key]['ai'] += 0.15
                print(black_flash[key]['ai'])
            print(passives.infinity_passive(char[member1.id]))
            if passives.infinity_passive(char[member1.id]):
                value2 = "The attack has been blocked by infinity"
                dmg2 = 0
            if passives.yata_passive(char[member1.id]):
                value2 = "The attack has been blocked by Yata no Kagami"
                dmg2 = 0
            if char['ai'] == "Sung-jin-woo":
                hp2 = int(hp2+dmg2*0.2)
            if char[member1.id] == "Ichigo":
                dmg2 = int(dmg2-dmg2*0.2)
                value2 = f"{move[key]['ai'][-1]} has dealt {dmg2} damage!"
            embed.add_field(name=f"{move[key]['ai'][0]} has used {move[key]['ai'][-1]}", value=value2)
            hp1 = hp1-dmg2
        else:
            embed.add_field(name=f"{move[key]['ai'][0]} has used {move[key]['ai'][-1]}", value=f"The attack has missed")

    member_win = False
    winner = discord.Embed(title=f"{member1.name} vs {char['ai']}", colour=discord.Colour.blue())
    if hp1 <= 0:
        if hp2 <= 0:
            speed1 = (1+data['Stats'][2]*0.05) * character_data[char[member1.id]]["Stats"][2]
            speed2 = character_data[char['ai']]["Stats"][2] * (1+curse_data[quest]['Stats'][2]*0.05)
            if speed1 > speed2:
                winner.add_field(name=f"{move[key][member1.id][0]} has used {move[key][member1.id][-1]}", value=f"{move[key][member1.id][-1]} has dealt {dmg1} damage")
                winner.add_field(name=f"{move[key]['ai'][0]} has fainted from the attack", value="They have lost")
                await ctx.send(embed=winner)
                await ctx.send(f"{member1.name} has won the battle")
                member_win = True
            elif speed2 > speed1:
                winner.add_field(name=f"{move[key][member1.id][0]} has fainted from the attack", value=f"They have lost")
                winner.add_field(name=f"{move[key]['ai'][0]} has used {move[key]['ai'][-1]}", value=f"{move[key]['ai'][-1]} has dealt {dmg2} damage")
                await ctx.send(embed=winner)
                await ctx.send(f"The Curse has won the battle")
            elif speed1 == speed2:
                anything = random.randint(1, 2)
                if anything == 1:
                    winner.add_field(name=f"{move[key][member1.id][0]} has used {move[key][member1.id][-1]}", value=f"{move[key][member1.id][-1]} has dealt {dmg1} damage")
                    winner.add_field(name=f"{move[key]['ai'][0]} has fainted from the attack", value="They have lost")
                    await ctx.send(embed=winner)
                    await ctx.send(f"{member1.name} has won the battle")
                    member_win = True
                else:
                    winner.add_field(name=f"{move[key][member1.id][0]} has fainted from the attack", value=f"They have lost")
                    winner.add_field(name=f"{move[key]['ai'][0]} has used {move[key]['ai'][-1]}", value=f"{move[key]['ai'][-1]} has dealt {dmg2} damage")
                    await ctx.send(embed=winner)
                    await ctx.send(f"The Curse has won the battle")
        else:
            winner.add_field(name=f"{move[key][member1.id][0]} has fainted from the attack", value=f"They have lost")
            winner.add_field(name=f"{move[key]['ai'][0]} has used {move[key]['ai'][-1]}", value=f"{move[key]['ai'][-1]} has dealt {dmg2} damage!")
            await ctx.send(embed=winner)
            await ctx.send(f"The Curse has won the battle")
        if member_win:
            await ctx.send(f"You have been awarded with {curse_data[quest]['Money']} coins for exorcising the cursed spirit :tada:")
            with open("profile_data.json", "w") as f:
                profile_data[str(member1.id)]["Money"] += curse_data[quest]["Money"]
                profile_data[str(member1.id)]["Characters"][char[member1.id]]['XP'] += curse_data[quest]["XP"]
                profile_data[str(member1.id)]["Mission"] += 1
                await ctx.send("You have advanced to the next stage")
                if profile_data[str(member1.id)]["Mission"] == 5:
                    await ctx.send("A boss awaits you in the next round")
                if profile_data[str(member1.id)]["Mission"] > 5:
                    profile_data[str(member1.id)]["Chapter"] += 1
                    profile_data[str(member1.id)]["Mission"] = 1
                current_level = profile_data[str(member1.id)]["Characters"][char[member1.id]]["Level"]
                next_level_xp = calculate_xp_for_next_level(current_level)

                if profile_data[str(member1.id)]["Characters"][char[member1.id]]['XP'] >= next_level_xp:
                    profile_data[str(member1.id)]["Characters"][char[member1.id]]['Level'] += 1
                    profile_data[str(member1.id)]["Characters"][char[member1.id]]['XP'] = 0
                    profile_data[str(member1.id)]["Characters"][char[member1.id]]['Points'] += 3
                    await ctx.send(f"Congratulations {member1.mention}, your **{char[member1.id]}** reached level {profile_data[str(member1.id)]['Characters'][char[member1.id]]['Level']}!")

                json.dump(profile_data, f)
        del move[key]
        del fight_key[key]
        del active_domain[key]
        del domain[key]
        del black_flash[key]
        os.remove(f"{key}.jpg")
    elif hp2 <= 0:
        if hp1 <= 0:
            speed1 = character_data[char[member1.id]]["Stats"][2] * (1+data['Stats'][2]*0.05)
            speed2 = character_data[char['ai']]["Stats"][2] * (1+curse_data[quest]['Stats'][2]*0.05)
            if speed1 > speed2:
                winner.add_field(name=f"{move[key][member1.id][0]} has used {move[key][member1.id][-1]}", value=f"{move[key][member1.id][-1]} has dealt {dmg1} damage")
                winner.add_field(name=f"{move[key]['ai'][0]} has fainted from the attack", value="They have lost")
                await ctx.send(embed=winner)
                await ctx.send(f"{member1.name} has won the battle")
                member_win = True
            elif speed2 > speed1:
                winner.add_field(name=f"{move[key][member1.id][0]} has fainted from the attack", value=f"They have lost")
                winner.add_field(name=f"{move[key]['ai'][0]} has used {move[key]['ai'][-1]}", value=f"{move[key]['ai'][-1]} has dealt {dmg2} damage")
                await ctx.send(embed=winner)
                await ctx.send(f"The Curse has won the battle")
            elif speed1 == speed2:
                anything = random.randint(1, 2)
                if anything == 1:
                    winner.add_field(name=f"{move[key][member1.id][0]} has used {move[key][member1.id][-1]}", value=f"{move[key][member1.id][-1]} has dealt {dmg1} damage")
                    winner.add_field(name=f"{move[key]['ai'][0]} has fainted from the attack", value="They have lost")
                    await ctx.send(embed=winner)
                    await ctx.send(f"{member1.name} has won the battle")
                    member_win = True
                else:
                    winner.add_field(name=f"{move[key][member1.id][0]} has fainted from the attack", value=f"They have lost")
                    winner.add_field(name=f"{move[key]['ai'][0]} has used {move[key]['ai'][-1]}", value=f"{move[key]['ai'][-1]} has dealt {dmg2} damage")
                    await ctx.send(embed=winner)
                    await ctx.send(f"The Curse has won the battle")
        else:
            winner.add_field(name=f"{move[key][member1.id][0]} has used {move[key][member1.id][-1]}", value=f"{move[key][member1.id][-1]} has dealt {dmg1} damage")
            winner.add_field(name=f"{move[key]['ai'][0]} has fainted from the attack", value="They have lost")
            await ctx.send(embed=winner)
            await ctx.send(f"{member1.name} has won the battle")
            member_win = True

        if member_win:
            await ctx.send(f"You have been awarded with {curse_data[quest]['Money']} coins for exorcising the cursed spirit :tada:")
            with open("profile_data.json", "w") as f:
                profile_data[str(member1.id)]["Money"] += curse_data[quest]["Money"]
                profile_data[str(member1.id)]["Characters"][char[member1.id]]['XP'] += curse_data[quest]["XP"]
                profile_data[str(member1.id)]["Mission"] += 1
                await ctx.send("You have advanced to the next stage")
                if profile_data[str(member1.id)]["Mission"] == 5:
                    await ctx.send("A boss awaits you in the next round")
                if profile_data[str(member1.id)]["Mission"] > 5:
                    profile_data[str(member1.id)]["Chapter"] += 1
                    profile_data[str(member1.id)]["Mission"] = 1
                    await ctx.send("You have advanced to the next Chapter")
                current_level = profile_data[str(member1.id)]["Characters"][char[member1.id]]["Level"]
                next_level_xp = calculate_xp_for_next_level(current_level)

                if profile_data[str(member1.id)]["Characters"][char[member1.id]]['XP'] >= next_level_xp:
                    profile_data[str(member1.id)]["Characters"][char[member1.id]]['Level'] += 1
                    profile_data[str(member1.id)]["Characters"][char[member1.id]]['XP'] = 0
                    profile_data[str(member1.id)]["Characters"][char[member1.id]]['Points'] += 3
                    await ctx.send(f"Congratulations {member1.mention}, your **{char[member1.id]}** reached level {profile_data[str(member1.id)]['Characters'][char[member1.id]]['Level']}!")

                json.dump(profile_data, f)
        del move[key]
        del fight_key[key]
        del active_domain[key]
        del domain[key]
        del black_flash[key]
        os.remove(f"{key}.jpg")
    else:
        move[key].clear()
        await ctx.send(embed=embed)
        await fight(ctx, member1, char, bot, hp1, hp2)


async def curseai(ctx, char, bot, key, quest):

    members = list(move[key].keys())
    member1_id = members[0]

    hp = move[key][member1_id][1]

    options = []
    for attack in character_data[battles[quest]]["Moves"]:
        options.append(attack)
    print(options)

    if fight_key[key] == 3:
        move[key]["ai"].append("Ultimate")
    elif hp > 100:
        choice = random.choice(options[0:2])
        print(choice)
        move[key]["ai"].append(f"{choice}")
    else:
        choice = random.choice(options[2:4])
        print(choice)
        move[key]["ai"].append(f"{choice}")
    await fight2(ctx, char, bot, key)


# noinspection PyUnresolvedReferences
class Moves(discord.ui.View):
    def __init__(self, ctx, member, character, char, hp, bot, quest):
        super().__init__()
        self.member = member
        self.character = character
        self.ctx = ctx
        self.char = char
        self.hp = hp
        self.bot = bot
        self.quest = quest
        self.create_attack()

    def create_attack(self):
        for attack in character_data[self.character]["Moves"]:
            async def button_callback(interaction: discord.Interaction):
                for item in self.children:
                    item.disabled = True
                await interaction.message.edit(view=self)
                key = ""
                for i in fight_key:
                    print(i)
                    if str(interaction.user.id) in i.split(","):
                        print(i.split(","))
                        key = i
                        print(key)
                        break
                await interaction.response.send_message("You have selected a move")
                selected_label = interaction.data["custom_id"]
                move[key][interaction.user.id].append(selected_label)
                print(selected_label)
                print(move[key])
                move_check = 0
                for i in move[key]:
                    try:
                        print(move[key][i][2])
                        move_check += 1
                    except:
                        print("a")
                await curseai(self.ctx, self.char, self.bot, key, self.quest)

            button = discord.ui.Button(label=attack, style=discord.ButtonStyle.primary, custom_id=attack)
            self.add_item(button)
            button.callback = button_callback

    @discord.ui.button(label="Ultimate", style=discord.ButtonStyle.red)
    async def ult(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        key = ""
        for i in fight_key:
            print(i)
            if str(interaction.user.id) in i.split(","):
                print(i.split(","))
                key = i
                print(key)
        if active_domain[key]:
            await interaction.response.send_message(
                "You cannot use your ultimate when another ultimate is already in play")
        if fight_key[key] >= 3:
            await interaction.response.send_message("You have selected your move")
            move[key][interaction.user.id].append("Ultimate")
            move_check = 0
            for i in move[key]:
                try:
                    print(move[key][i][2])
                    move_check += 1
                except:
                    print("a")
            await curseai(self.ctx, self.char, self.bot, key, self.quest)
        else:
            await interaction.response.send_message(
                f"You cannot use this yet, you will be able to use this in {3 - fight_key[key]} turns")


async def fight(ctx, member1: discord.Member, char, bot, hp1=None, hp2=None):
    with open("profile_data.json", "r") as p:
        profile_data = json.load(p)

    quest = str(profile_data[str(member1.id)]["Chapter"])+str(profile_data[str(member1.id)]["Mission"])

    data = profile_data[str(member1.id)]["Characters"][char[member1.id]]
    if hp1 is None and hp2 is None:
        hp1 = int(260 * (1 + data['Stats'][0] * 0.05) * character_data[char[member1.id]]["Stats"][0])
        hp2 = int(260 * (1 + curse_data[quest]['Stats'][0]*0.05) * character_data[battles[quest]]["Stats"][0])

    in_fight = False
    key = ""
    for i in fight_key:
        if str(member1.id) == i:
            in_fight = True
            key = i
    if not in_fight:
        key = str(member1.id)
        fight_key[key] = 0
        move[key] = {}
        active_domain[key] = False

    current_directory = os.path.dirname(__file__)
    characters_folder = os.path.join(current_directory, "characters")
    backgrounds_folder = os.path.join(current_directory, "backgrounds")
    if key in domain:
        file_path = os.path.join(backgrounds_folder, f"{character_data[domain[key][1]]['Ultimate'][0]}.jpg")
        background = Image.open(file_path)
    else:
        file_path = os.path.join(backgrounds_folder, "background.jpg")
        background = Image.open(file_path)

    # Open the overlay image
    character1 = os.path.join(characters_folder, f"{char[member1.id]}.png")
    character2 = os.path.join(characters_folder, f"{battles[quest]}.png")
    overlay1 = Image.open(character1)
    overlay2 = Image.open(character2)

    overlay2 = overlay2.transpose(Image.FLIP_LEFT_RIGHT)

    # Specify the coordinates where you want to place the overlay image
    x1 = 0
    y1 = 100

    # Paste the overlay image onto the background image at the specified coordinates
    background.paste(overlay1, (x1, y1), overlay1)

    x2 = background.width - 750  # Place the overlay at the extreme right
    y2 = 100  # Adjust the y-coordinate as needed

    # Paste the resized overlay image onto the background image at the specified coordinates
    background.paste(overlay2, (x2, y2), overlay2)

    # Save the resulting image
    background.save(f"{key}.jpg")

    with open(f'{key}.jpg', 'rb') as f:
        # noinspection PyTypeChecker
        file = discord.File(f, filename="result.jpg")

    max_hp1 = int(260 * (1+data['Stats'][0]*0.05) * character_data[char[member1.id]]["Stats"][0])
    max_hp2 = int(260 * (1+curse_data[quest]['Stats'][0]*0.05) * character_data[battles[quest]]["Stats"][0])

    embed = discord.Embed(title=f"Battle between {member1.name} and {battles[quest]}", colour=discord.Colour.blue())
    embed.add_field(name="",
                    value="Choose your moves in DMs. After both players have chosen, the move will be executed",
                    inline=False)
    embed.add_field(name=f"{member1.name}", value=f"{char[member1.id]}: {hp1}/{max_hp1} HP")
    embed.add_field(name=f"{battles[quest]}", value=f"{battles[quest]}: {hp2}/{max_hp2} HP")
    embed.set_image(url=f"attachment://result.jpg")
    await ctx.send(embed=embed, file=file)

    fight_key[key] += 1
    move[key][member1.id] = [char[member1.id], hp1]
    move[key]["ai"] = [battles[quest], hp2]

    if fight_key[key] == 1:
        if char[member1.id] in black_flash_users:
            black_flash[key] = {}
            black_flash[key][member1.id] = 1

    member1_view = Moves(ctx, member1, char[member1.id], char, hp1, bot, quest)
    await member1.send(view=member1_view)

    member1_button_selected = False
    member2_button_selected = False

    while True:
        # Wait for the author and mentioned member to select a button
        try:
            author_interaction = await bot.wait_for('button_click', timeout=60, check=member1_view.interaction_check)
        except asyncio.TimeoutError:
            return

        if author_interaction.user == member1:
            await author_interaction.response.send_message('You selected a button.', ephemeral=True)
            member1_button_selected = True

        if member1.id in move:
            await ctx.send("You have chosen your move")
            break


class CharacterDropdown(discord.ui.Select):
    def __init__(self, ctx, author: discord.Member, bot):
        self.ctx = ctx
        self.author = author
        self.bot = bot
        self.char = {}
        options = [
            discord.SelectOption(label="Yuji", description="The One with an Unbreakable Will"),
            discord.SelectOption(label="Gojo", description="The Honoured One"),
            discord.SelectOption(label="Megumi", description="The One with the Shadows"),
            discord.SelectOption(label="Toji", description="The Sorcerer Killer"),
            discord.SelectOption(label="Geto", description="The Curse User"),
            discord.SelectOption(label="Sukuna", description="The King of Curses"),
            discord.SelectOption(label="Jogo", description="The Flames of Disaster"),
            discord.SelectOption(label="Naruto", description="The Seventh Hokage"),
            discord.SelectOption(label="Madara", description="The Ghost of the Uchiha"),
            discord.SelectOption(label="Sasuke", description="The Last Uchiha"),
            discord.SelectOption(label="Meliodas", description="The Minor Chaser"),
            discord.SelectOption(label="Yuji-awk", description="The Prince of the Flashes"),
            discord.SelectOption(label="Ichigo", description="Substitute Soul Reaper"),
            discord.SelectOption(label="Sung-jin-woo", description="The Monarch of the Shadows"),
            discord.SelectOption(label="Itachi", description="The Clan Killer"),
            discord.SelectOption(label="Hitler", description="The Jew Killer")
        ]
        super().__init__(placeholder="Choose", options=options, min_values=1, max_values=1)

    # noinspection PyUnresolvedReferences
    async def callback(self, interaction: discord.Interaction):
        naruto_access = [768074971213725706]
        madara_access = [782828284286337044, 768074971213725706, 667792981742321674, 751131698342789332,
                         1174422891765444628]
        sasuke_access = [768074971213725706, 920290328811012096, 800305971132891166]
        meliodas_access = [751131698342789332]
        yujiawk_access = [782828284286337044]
        ichigo_access = [833928945082302495]
        jinwoo_access = [1174422891765444628]
        itachi_access = [914136372951023617]
        hitler_access = [628254382282244097, 1188831623907647613]
        with open("profile_data.json", "r") as f:
            profile_data = json.load(f)
        quest = str(profile_data[str(self.author.id)]["Chapter"]) + str(profile_data[str(self.author.id)]["Mission"])

        if interaction.user.id == self.author.id:
            if self.values[0] not in profile_data[str(self.author.id)]["Characters"]:
                await interaction.response.send_message("You do not possess this character", ephemeral=True)
            if self.values[0] == "Naruto" and interaction.user.id not in naruto_access:
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message(f"You cannot choose this character", ephemeral=True)
            if self.values[0] == "Madara" and interaction.user.id not in madara_access:
                await interaction.response.send_message(f"You cannot choose this character", ephemeral=True)
            if self.values[0] == "Sasuke" and interaction.user.id not in sasuke_access:
                await interaction.response.send_message(f"You cannot choose this character", ephemeral=True)
            if self.values[0] == "Meliodas" and interaction.user.id not in meliodas_access:
                await interaction.response.send_message(f"You cannot choose this character", ephemeral=True)
            if self.values[0] == "Yuji-awk" and interaction.user.id not in yujiawk_access:
                await interaction.response.send_message(f"You cannot choose this character", ephemeral=True)
            if self.values[0] == "Ichigo" and interaction.user.id not in ichigo_access:
                await interaction.response.send_message(f"You cannot choose this character", ephemeral=True)
            if self.values[0] == "Sung-jin-woo" and interaction.user.id not in jinwoo_access:
                await interaction.response.send_message(f"You cannot choose this character", ephemeral=True)
            if self.values[0] == "Itachi" and interaction.user.id not in itachi_access:
                await interaction.response.send_message(f"You cannot choose this character", ephemeral=True)
            if self.values[0] == "Hitler" and interaction.user.id not in hitler_access:
                await interaction.response.send_message(f"You cannot choose this character", ephemeral=True)
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f"{interaction.user.name} has chosen {self.values[0]}")
            self.char[interaction.user.id] = self.values[0]
        else:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f"You are not a part of the battle", ephemeral=True)
        if self.author.id in self.char:
            self.char["ai"] = battles[quest]
            await interaction.message.delete()
            await self.ctx.send("The fight is about to begin")
            await fight(self.ctx, self.author, self.char, self.bot)


class RPS(discord.ui.View):
    def __init__(self, ctx, author: discord.Member, bot):
        super().__init__(timeout=30)
        self.value = None
        self.author = author
        self.ctx = ctx
        self.bot = bot

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.author.id != interaction.user.id:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f"You are not {self.author.name}", ephemeral=True)
        else:
            fight_view = discord.ui.View()
            fight_view.add_item(CharacterDropdown(self.ctx, self.author, self.bot))
            embed = discord.Embed(title=f"The battle will begin once you choose your character",
                                  colour=discord.Colour.blue())
            embed.add_field(name="Choose your character",
                            value="Choose one of the characters from the given below to use in the fight")
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(embed=embed, view=fight_view)
            await interaction.message.delete()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.author.id != interaction.user.id:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message(f"You are not {self.author.name}", ephemeral=True)
        else:
            # noinspection PyUnresolvedReferences
            await interaction.response.send_message("You have turned down the mission", ephemeral=True)
            await interaction.message.delete()


class story(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def story(self, ctx):
        with open("profile_data.json", "r") as f:
            profile_data = json.load(f)
        id = str(ctx.author.id)

        if str(ctx.author.id) in fight_key:
            await ctx.send("You're already in a quest")
            return

        if str(ctx.author.id) not in profile_data:
            profile_data[id] = {}
            profile_data[id]["Money"] = 0
            profile_data[id]["Chapter"] = 1
            profile_data[id]["Mission"] = 1
            profile_data[id]["Characters"] = {}
            profile_data[id]["Characters"]["Yuji"] = {"Level": 1, "XP": 0, "Stats": [0, 0, 0], "Points": 0}
            with open('report.json', 'w') as p:
                json.dump(profile_data, p)

        view = RPS(ctx, ctx.author, self.bot)
        await ctx.send(f"Do you wish to begin the story?", view=view)


async def setup(bot):
    await bot.add_cog(story(bot))
