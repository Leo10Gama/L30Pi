import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()
PREFIX = "p."
command_help = {
    "ping": "`p.ping`\nA simple debug command where I respond with 'pong'",
    "help": "`p.help`\nList all available commands\n`p.help [command]`\nGet further details on a specific command"
}
command_list = list(command_help.keys())

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
        command = message.content[2:].lower().strip()
        # Ping command
        if command[:4] == command_list[0]:
            await message.channel.send('Pong!')
        # Help command
        elif command[:4] == command_list[1]:
            command = command[4:].strip()
            # Get information on a specific command
            if command in command_help:
                await message.channel.send(command_help[command])
            # View list of all commands
            else:
                await message.channel.send("Here are some commands I am capable of:\n`" + "`\n`".join(command_list) + "`")

client.run(TOKEN)