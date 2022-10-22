from discord.ext import commands, tasks
import discord
import sqlite3
import asyncio
import os.path

class Alarm(commands.Cog):
    def __init__(self, kakapo):
        self.kakapo = kakapo
        
    @tasks.loop(seconds=1)
    async def tsk_loop(): 
        pass

    tsk_loop.start()

    @commands.group(name="alarm")
    async def alarm(self, ctx):
        pass

    @alarm.command(name="set")
    async def alarm_set(self, ctx, channel:discord.TextChannel, message="", hour=""):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "kakapo_database.db")
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM alarm WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            sql = ("INSERT INTO alarm (guild_id, channel_id, message, hour) VALUES(?,?,?,?)")
            val = (ctx.guild.id, channel.id, message, hour)
            await ctx.send(f"Alarms channel has been set to {channel.mention} with the message {message} at {hour}hs!")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @alarm.command(name="remove")
    async def alarm_remove(self, ctx):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "kakapo_database.db")
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            sql = (f"DELETE FROM alarm WHERE channel_id = {ctx.channel.id}")
        cursor.execute(sql)
        cursor.close()
        db.close()
        message = await ctx.send("Alarm removed!")
        message_id = message.id
        msg = await ctx.channel.fetch_message(message_id)
        await asyncio.sleep(1)
        await msg.delete()
        await ctx.channel.purge(limit=1)
        pass



def setup(kakapo):
    kakapo.add_cog(Alarm(kakapo))
    