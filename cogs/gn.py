from discord.ext import commands, tasks
import discord
import sqlite3
import asyncio
import os.path
from datetime import datetime
import re

class Alarm(commands.Cog):
    def __init__(self, kakapo):
        self.kakapo = kakapo

    @tasks.loop(minutes=1)
    async def time_check(self):
        rn = re.sub('[^0-9]', '', str(datetime.utcnow().time()))
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
                hour = int(hour_row[0])
                
                if time == hour:
                    cursor.execute(f"SELECT channel_id FROM alarm WHERE hour = '{hour}'")
                    channel_id_result = [row[0] for row in cursor.fetchall()]
                    print(f"Hour: {hour_row[0]}, Channels:{channel_id_result}")

                    for channel_id_row in channel_id_result:
                        channel_id = channel_id_row

                        cursor.execute(f"SELECT message FROM alarm WHERE channel_id = '{channel_id}'")
                        message = cursor.fetchone()

                        channel = self.kakapo.get_channel(int(channel_id))
                        await channel.send(message[0])
        db.commit()
        cursor.close()
        db.close()
        await asyncio.sleep(60)

    @commands.Cog.listener()
    async def on_ready(self):
        rn = 1
        while rn > 0:
            rn = re.sub('[^0-9]', '', str(datetime.utcnow().time()))
            rn = int(rn[4:6])
            print("")
            print(rn)
            if rn < 59:
                await asyncio.sleep(1)
        else:
            await self.time_check.start()

    @commands.command(name="tcstop")
    async def tcstop(self, ctx):
        self.time_check.cancel()
        print("Time check stopped")

    @commands.command(name="tcstart")
    async def tcstart(self, ctx):
        rn = 1
        while rn > 0:
            rn = re.sub('[^0-9]', '', str(datetime.utcnow().time()))
            rn = int(rn[4:6])
            print("")
            print(rn)
            if rn < 59:
                await asyncio.sleep(1)
        else:
            await self.time_check.start()
            print("Time check started")

    @commands.group(name="alarm")
    async def alarm(self, ctx):
        pass

    @alarm.command(name="set")
    async def alarm_set(self, ctx, channel:discord.TextChannel, message="", hour=""):
        hour = re.sub('[^0-9]', '', hour)
        if hour != "":
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "kakapo_database.db")
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                sql = ("INSERT INTO alarm (channel_id, message, hour) VALUES(?,?,?)")
                val = (channel.id, message, hour)
                cursor.execute(sql, val)
                await ctx.send(f"Alarms channel has been set to {channel.mention} with the message '{message}' at {hour[:2]}:{hour[2:]}hs!")
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.send("That is not a valid hour!")

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

async def setup(kakapo):
    await kakapo.add_cog(Alarm(kakapo))