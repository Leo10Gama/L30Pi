import os
import discord
import piglatin
import ninsheetmusic as nsm
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client()
PREFIX = "p."
command_help = {
    "ping": "`p.ping`\nA simple debug command where I respond with 'pong'",
    "help": "`p.help`\nList all available commands\n`p.help [command]`\nGet further details on a specific command",
    "palindrome": "`p.palindrome [word]`\nFigure out if a word is spelt the same forwards and backwards",
    "math": "`p.math [number] [operation] [number]`\nPerform a mathematical operation using either {+, -, *, /, %, \\}",
    "piglatin": "`p.piglatin [phrase]`\nConvert a phrase or expression into pig latin",
    "ninsheetmusic": "`p.ninsheetmusic series`\nFind video game sheet music based on the game series (default)\n`p.ninsheetmusic console`\nFind video game sheet music based on the console that game was on"
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
        # Pig latin command
        elif command[:8] == command_list[4]:
            await message.channel.send(piglatin.to_piglatin(command[8:].strip()))
        # Ninsheetmusic command
        elif command[:13] == command_list[5]:
            search_page = ""
            # Search by console
            if command[13:].strip().lower() == "console":
                consoles = nsm.get_console_list()
                console_list = list(consoles.keys())
                await message.channel.send("Which console would you like to see the sheets for? (Or type `list` to see all available consoles)")
                want2exit = False
                while not want2exit:
                    console = await client.wait_for("message", check=lambda m : m.author == message.author and m.channel == message.channel, timeout=60)
                    # List consoles to search from
                    if console.content.lower().strip() == "list":
                        embed = discord.Embed(title="Consoles")
                        desc = ""
                        for c in console_list:
                            desc += c + "\n"
                        embed.description = desc
                        await message.channel.send(embed=embed)
                        await message.channel.send("Which of these would you like sheets for?")
                    # A console has been selected
                    elif console.content.lower().strip() in console_list:
                        games = nsm.get_sheets_from_page(consoles[console.content.lower().strip()])
                        embed = discord.Embed(title="Games")
                        desc = ""
                        for game in games.keys():
                            desc += game.lower() + "\n"
                        embed.description = desc
                        await message.channel.send(embed=embed)
                        await message.channel.send("Which game would you like to see sheets from?")
                        # Figure out which game to see sheets from
                        game = await client.wait_for("message", check=lambda m : m.author == message.author and m.channel == message.channel, timeout=60)
                        await get_sheets(game.content, games, message.channel)
                        want2exit = True
                    # Unknown command
                    else:
                        await message.channel.send("Unknown command. Cancelling action")
                        want2exit = True
            # Search by series
            else:
                serieses = nsm.get_series_list()
                series_list = list(serieses.keys())
                await message.channel.send("Which series would you like to see the sheets for? (Or type `list` to see all available consoles)")
                want2exit = False
                while not want2exit:
                    series = await client.wait_for("message", check=lambda m : m.author == message.author and m.channel == message.channel, timeout=60)
                    # List series to search from
                    if series.content.lower().strip() == "list":
                        embed = discord.Embed(title="Series")
                        desc = ""
                        for s in series_list:
                            desc += s + "\n"
                        embed.description = desc
                        await message.channel.send(embed=embed)
                        await message.channel.send("Which of these would you like sheets for?")
                    # A series has been selected
                    elif series.content.lower().strip() in series_list:
                        games = nsm.get_sheets_from_page(serieses[series.content.lower().strip()])
                        embed = discord.Embed(title="Games")
                        desc = ""
                        for game in games.keys():
                            desc += game.lower() + "\n"
                        embed.description = desc
                        await message.channel.send(embed=embed)
                        await message.channel.send("Which game would you like to see sheets from?")
                        # Figure out which game to see sheets from
                        game = await client.wait_for("message", check=lambda m : m.author == message.author and m.channel == message.channel, timeout=60)
                        await get_sheets(game.content, games, message.channel)
                        want2exit = True
                    # Unknown command
                    else:
                        await message.channel.send("Unknown command. Cancelling action")
                        want2exit = True    
        #TODO: Add more commands here
        else:
            await message.channel.send("Command not found. Try typing `p.help` to see a list of all commands")

async def get_sheets(game, games, channel):
    if game.lower().strip() in list(i.lower() for i in games.keys()):
        songlist = {}
        game_title = ""
        for i in games.keys():
            if game.lower().strip() == i.lower():
                songlist = games[i]
                game_title = i
                break
        embed = discord.Embed(title=game_title)
        char_sum = len(game_title)
        for song in songlist:
            embed.add_field(name=song["title"], value="Arranged by " + song["arranger"] + "\n" + song["link"], inline=True)
            char_sum += len(song["title"]) + len(song["arranger"]) + len(song["link"])
        # This chunk is to make sure the embed character limit is not exceeded
        if char_sum <= 6000:
            await channel.send(embed=embed)
        else:
            async with channel.typing():
                await channel.send("**" + game_title + "**")
                for song in songlist:
                    await channel.send(song["title"] + " (Arranged by " + song["arranger"] + "): " + song["link"])
    else:
        await channel.send("Game not found. Cancelling action")

client.run(TOKEN)