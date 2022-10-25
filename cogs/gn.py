from discord.ext import commands
import discord
import sqlite3
import asyncio
import os.path
import datetime
import re

class Alarm(commands.Cog):
    def __init__(self, kakapo):
        self.kakapo = kakapo
    
    async def time_check():
        while True:
            rn = re.sub('[^0-9]', '', str(datetime.datetime.now().time()))
            time = str(rn[:4])
            print("")
            print("Actual time: " + time)
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "kakapo_database.db")
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                cursor.execute(f"SELECT hour FROM alarm")
                # result = cursor.fetchall
                # print(result)
                for row in cursor:
                    hour = re.sub('[^0-9]', '', str(row))
                    print("Saved hour: " + hour)
                    if time == hour:
                        cursor.execute(f"SELECT guild_id FROM alarm WHERE hour = {hour}")
                        result = cursor.fetchall
                        for row in cursor:
                            cursor.execute(f"SELECT channel_id FROM alarm WHERE guild_id = {result}")
                    else:
                        pass
            db.commit()
            cursor.close()
            db.close()
            await asyncio.sleep(60)
    
    @commands.command(name="test")
    async def test_command(self, ctx):
        pass

    @commands.group(name="alarm")
    async def alarm(self, ctx):
        pass

    @alarm.command(name="set")
    async def alarm_set(self, ctx, channel:discord.TextChannel, message="", hour=""):
        hour = re.sub('[^0-9]', '', hour)

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
    