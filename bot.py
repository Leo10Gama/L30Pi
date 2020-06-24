import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()
PREFIX = "p."

# This event will execute when the bot goes online
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

# This event executes when a message is sent
@client.event
async def on_message(message):
    # Ignore messages from bot
    if message.author == client.user:
        return

    # Determine if the message sent is something the bot should respond to
    if message.content.startswith(PREFIX):
        commands = message.content[2:]
        if commands == "ping":
            await message.channel.send('Pong!')

client.run(TOKEN)