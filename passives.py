import discord
import random
import asyncio


def infinity_passive(character):
    chances = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    roll = 5
    if character == "Gojo":
        if roll == random.choice(chances):
            return True
        else:
            return False
    else:
        return False


def flames_passive(character):
    chances = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    roll = 5
    if character == "Jogo":
        if roll == random.choice(chances):
            return True
        else:
            return False
    else:
        return False

def yata_passive(character):
    chances = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    roll = 5
    if character == "Itachi":
        if roll == random.choice(chances):
            return True
        else:
            return False
    else:
        return False


