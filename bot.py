# bot.py
import os
import json
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#Determina quais prefixos iremos utilizar
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes [str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#Manipula os dados do prefix.json
@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes [str(guild.id)] = 'o!'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes [str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

import discord

import youtube_dl

from discord.ext import commands

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}   

def endSong(guild, path):
    os.remove(path)                                   

@client.command(pass_context=True)
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send('you are not connected to a voice channel')
        return

    else:
        channel = ctx.message.author.voice.channel

    voice_client = await channel.connect()

    guild = ctx.message.guild

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info(url, download=True)
        path = str(file['title']) + "-" + str(file['id'] + ".mp3")

    voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)

    await ctx.send(f'**Music: **{url}')

client.run()