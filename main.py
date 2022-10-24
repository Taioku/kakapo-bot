from discord.ext import commands
import discord
import os

intents = discord.Intents.default()
intents.members = True

#token = os.environ["DISCORD_TOKEN"]
token = "MTAzMjg1NDkwMTQ1OTUyNTY3Mg.GzSNE8.-StVJKHoAIeu-_KNI845NC-UmkStqZ83qOxStM"

kakapo = commands.Bot(command_prefix = "k!", intents=intents)

extensions = ["cogs.gn"]

@kakapo.event
async def on_ready():
    await kakapo.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="k!help"))
    print(kakapo.user.name, "has woke up!")
    print("User id:", kakapo.user.id)

@kakapo.command()
async def load(ctx, extension):
    if ctx.message.author.id == 272429170363990016:
        try:
            cogs = "cogs."
            kakapo.load_extension(cogs + extension)
            print("Loaded {}".format(extension))
            print('')
            await ctx.send("Loaded {}!".format(extension))
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(extension, error))
            print('')
            await ctx.send("{} cannot be loaded. [{}]!".format(extension, error))
    else:
        pass

@kakapo.command()
async def unload(ctx, extension):
    if ctx.message.author.id == 272429170363990016:
        try:
            cogs = "cogs."
            kakapo.unload_extension(cogs + extension)
            print("Unloaded {}".format(extension))
            print('')
            await ctx.send("Unloaded {}!".format(extension))
        except Exception as error:
            print("{} cannot be unloaded. [{}]".format(extension, error))
            print('')
            await ctx.send("{} cannot be unloaded. [{}]!".format(extension, error))
    else:
        pass

@kakapo.command()
async def reload(ctx, extension):
    if ctx.message.author.id == 272429170363990016:
        try:
            cogs = "cogs."
            kakapo.reload_extension(cogs + extension)
            print("Reloaded {}".format(extension))
            print('')
            await ctx.send("Reloaded {}!".format( extension))
        except Exception as error:
            print("{} cannot be reloaded. [{}]".format(extension, error))
            print('')
            await ctx.send("{} cannot be reloaded. [{}]!".format(extension, error))
    else:
        pass

if __name__ == "__main__":
    for extension in extensions:
        try:
            kakapo.load_extension(extension)
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(extension, error))

kakapo.run(token)
