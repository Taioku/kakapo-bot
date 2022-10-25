from discord.ext import commands, tasks
import discord
import sqlite3
import asyncio
import os.path
import datetime
import re
from discord.utils import get

class Alarm(commands.Cog):
    def __init__(self, kakapo):
        self.kakapo = kakapo

    @tasks.loop(minutes=1)
    async def time_check(self, ctx: commands.Context):
        rn = re.sub('[^0-9]', '', str(datetime.datetime.now().time()))
        time = str(rn[:4])
        print("")
        print("Actual time: " + time)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "kakapo_database.db")
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT DISTINCT hour FROM alarm")
            hour_result = cursor.fetchall()
            for hour_row in hour_result:
                hour = hour_row[0]
                print(hour)

                #if time == hour:
                cursor.execute(f"SELECT channel_id FROM alarm WHERE hour = '{hour}'")
                channel_id_result = [row[0] for row in cursor.fetchall()]
                print(f"Hour: {hour_row[0]}, Channels:{channel_id_result}")
                for channel_id_row in channel_id_result:
                    channel_id = channel_id_row
                    print(channel_id)

                    cursor.execute(f"SELECT message FROM alarm WHERE channel_id = '{channel_id}'")
                    message = cursor.fetchone()

                    channel = self.kakapo.get_channel(int(channel_id))
                    await channel.send(message[0])
        db.commit()
        cursor.close()
        db.close()

    @commands.command(name="start")
    async def start_clock(self, ctx):
        self.time_check.start(ctx)

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