import discord
import json
import openai
import random
from youtube_transcript_api import YouTubeTranscriptApi
import os
import requests
from io import BytesIO
from discord.ext import commands
from summa import summarizer
import engine


commands = ["/glimpse "]
# Intent Declaration
client = discord.Client(intents=discord.Intents.all())
tkn = "MTA3MDgwMzUwNzI0ODEwNzUyMA.GsWRmT.cvJjYqmk_hnvKkhVvI_CfEX-gM8xz8akTkgofQ"

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    print("GLIMPSE OPEN")

@client.event
async def on_message(message):
    if message.content.startswith(commands[0]):
        video_id = message.content[len(commands[0]):].strip()
        result = glimpse.glimpse(video_id)
        if type(result) == str:
            with open("output.md", "w") as file:
                file.write(result)
            await message.channel.send(file=discord.File("output.md"))
        elif result == 400:
            await message.channel.send("ERROR 400: Video not Found")
        elif result == 401:
            await message.channel.send("ERROR 401: Transcript not found")
        elif result == 402:
            await message.channel.send("ERROR 402: OpenAI could not generate a blog")

client.run(tkn)
