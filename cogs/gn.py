from doctest import REPORTING_FLAGS
from unittest import result
from discord.ext import commands, tasks
import discord
import sqlite3
import asyncio
import os.path
import datetime

from pyparsing import restOfLine

badchars = {32: 0, 40: 0, 41: 0, 44: 0, 58: 0}

class Alarm(commands.Cog):
    def __init__(self, kakapo):
        self.kakapo = kakapo
        
    guild_id = "666417376627261451"



    @tasks.loop(minutes=1)
    async def tsk_loop(): 
        rn = str(datetime.datetime.now().time()).strip(":") 
        time = str(rn[:5])
        time = time.translate(badchars)
        print("")
        print("")
        print(time)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "kakapo_database.db")
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT hour FROM alarm")
            # result = cursor.fetchall
            # print(result)
            for row in cursor:
                hour = str(row).translate(badchars)
                print(row)
                if time == 0:
                    pass
                else:
                    pass
        db.commit()
        cursor.close()
        db.close()
                

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
            cursor.execute(f"SELECT channel_id FROM alarm")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO alarm (channel_id, message, hour) VALUES(?,?,?)")
                val = (channel.id, message, hour)
                cursor.execute(sql, val)
                await ctx.send(f"Alarms channel has been set to {channel.mention} with the message {message} at {hour}hs!")
            else:
                pass
                await ctx.send(f"Alarm!")
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
        db.commit()
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
    