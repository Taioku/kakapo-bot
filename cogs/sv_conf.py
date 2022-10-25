from discord.ext import commands
import discord

class Config(commands.Cog):
    def __init__(self, kakapo):
        self.kakapo = kakapo



def setup(kakapo):
    kakapo.add_cog(Config(kakapo))