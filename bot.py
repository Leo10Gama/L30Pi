import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()
PREFIX = "p."
command_help = {
    "ping": "`p.ping`\nA simple debug command where I respond with 'pong'",
    "help": "`p.help`\nList all available commands\n`p.help [command]`\nGet further details on a specific command",
    "palindrome": "`p.palindrome [word]`\nFigure out if a word is spelt the same forwards and backwards",
    "math": "`p.math [number] [operation] [number]`\nPerform a mathematical operation using either {+, -, *, /, %, \\}"
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
        # Palindrome command
        elif command[:10] == command_list[2]:
            word = command[10:].strip()
            if word == word[::-1]:
                await message.channel.send("This word **is** a palindrome")
            else:
                await message.channel.send("This word **is not** a palindrome")
        # Math command
        elif command[:4] == command_list[3]:
            maths = command[4:].strip().split()
            if len(maths) == 3:
                try:
                    if maths[1] == "+":
                        await message.channel.send(maths[0] + " " + maths[1] + " " + maths[2] +
                              " = " + str(float(maths[0]) + float(maths[2])))
                    elif maths[1] == "-":
                        await message.channel.send(maths[0] + " " + maths[1] + " " + maths[2] +
                              " = " + str(float(maths[0]) - float(maths[2])))
                    elif maths[1] == "*":
                        await message.channel.send(maths[0] + " " + maths[1] + " " + maths[2] +
                              " = " + str(float(maths[0]) * float(maths[2])))
                    elif maths[1] == "/":
                        await message.channel.send(maths[0] + " " + maths[1] + " " + maths[2] +
                              " = " + str(float(maths[0]) / float(maths[2])))
                    elif maths[1] == "%":
                        await message.channel.send(maths[0] + " " + maths[1] + " " + maths[2] +
                              " = " + str(float(maths[0]) % float(maths[2])))
                    elif maths[1] == "\\":
                        await message.channel.send(maths[0] + " " + maths[1] + " " + maths[2] +
                              " = " + str(float(maths[0]) // float(maths[2])))
                    else:
                        await message.channel.send("Invalid input")
                except:
                    await message.channel.send("Invalid input")
            else:
                await message.channel.send("Invalid operation")
        #TODO: Add more commands here
        else:
            await message.channel.send("Command not found. Try typing `p.help` to see a list of all commands")

client.run(TOKEN)