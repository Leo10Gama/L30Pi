import os
import discord
import piglatin
import ninsheetmusic as nsm
import fibonacci as fib
import flag
import smashu
import trivia
import coin as numista
import cat
import vgmost as khi
import cards
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
    "nsm": "Searches for video game sheet music on the site https://www.ninsheetmusic.org\n`p.nsm`\n`p.nsm series`\nFind video game sheet music based on the game series (default)\n`p.nsm console`\nFind video game sheet music based on the console that game was on\n`p.nsm update`\nRetrieve the most recently added sheets from the site",
    "fibonacci": "`p.fibonacci [integer]`\nGet a term of the fibonacci sequence",
    "flag": "A fun game! Guess what country the flag belongs to in 30 seconds (or 3 tries)\n`p.flag`\nStart the game with country flags from around the world\n`p.flag america`\nStart the game with flags from the states of USA\n`p.flag canada`\nStart the game with flags of the provinces and territories of Canada\n`p.flag arms`\nStart the game with country's coats of arms instead of flags",
    "smashu": "`p.smashu [character]`\nSee the hitboxes of a character from Super Smash Bros. Ultimate",
    "percent": "`p.percent [number]/[number]`\nGet the percentage of a given fraction",
    "coin": "`p.coin`\nSearch for a coin based on its country, face value, year, and description\n`p.coin random (modifier)`\nFind and display a random coin (note: may sometimes fail if I find a bad link, apologies in advance)\nNote that modifiers include countries or years",
    "cat": "`p.cat`\nShow a picture of a cat!\n`p.cat list`\nShow a list of cats you can see\n`p.cat [cat name]`\nShow one of the cats in the list",
    "soundtrack": "`p.soundtrack [game]`\nRetrieve the soundtrack of a given video game",
    "blackjack": "`p.blackjack`\nStart a game of blackjack against me"
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
                await message.channel.send("Here are some commands I am capable of:\n`" + "`\n`".join(command_list) + "`\nIf you'd like more information about a given command, just type `p.help [command]`")
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
        # Ninsheetmusic (NSM) command
        elif command[:3] == command_list[5]:
            search_sheets = True
            # Search by console
            if command[3:].strip().lower() == "console":
                search_dict = nsm.get_list("console")
            # Check update
            elif command[3:].strip().lower() == "update":
                await message.channel.send("Getting update information (this may take a while)...")
                try:
                    update = nsm.get_update()
                    embed = discord.Embed(title=update["title"], description=update["text"])
                    for song in update["songs"]:
                        embed.add_field(name=song.title + " (from {})".format(song.game), value="Arranged by *{}*\n{}".format(song.arranger, song.links["pdf"]))
                    await message.channel.send(embed=embed)
                except:
                    await message.channel.send("Something went wrong, but you can see the most recent update for yourself at https://www.ninsheetmusic.org")
                search_sheets = False
            # Search by series
            else:
                search_dict = nsm.get_list()
            if search_sheets:
                search_list = list(search_dict.keys())
                await message.channel.send("Which would you like to see the sheets for? (Or type `list` to see all available options)")
                want2exit = False
                while not want2exit:
                    search_item = await client.wait_for("message", check=lambda m : m.author == message.author and m.channel == message.channel, timeout=60)
                    search_item = search_item.content.lower().strip()
                    # List options to search from
                    if search_item == "list":
                        embed = discord.Embed(title="Options")
                        desc = ""
                        for s in search_list:
                            desc += s + "\n"
                        if len(desc) < 2048:
                            embed.description = desc
                            await message.channel.send(embed=embed)
                            await message.channel.send("Which of these would you like sheets for?")
                        else:
                            await message.channel.send("Which game would you like sheets for?")
                    # An item has been selected
                    elif search_item in search_list:
                        games = nsm.get_sheets_from_page(search_dict[search_item])
                        embed = discord.Embed(title="Games")
                        desc = ""
                        for game in games.keys():
                            desc += game.lower() + " ({} sheets)\n".format(len(games[game]))
                        if len(desc) < 2048:
                            embed.description = desc
                            await message.channel.send(embed=embed)
                            await message.channel.send("Which of these would you like sheets for?")
                        else:
                            await message.channel.send("Which game would you like sheets for?")
                        # Figure out which game to see sheets from
                        game = await client.wait_for("message", check=lambda m : m.author == message.author and m.channel == message.channel, timeout=60)
                        game = game.content.lower().strip()
                        if game in list(i.lower() for i in games.keys()):
                            songlist = {}
                            game_title = ""
                            for i in games.keys():
                                if game == i.lower():
                                    songlist = games[i]
                                    game_title = i
                                    break
                            # This chunk is to make sure the embed character limit is not exceeded
                            embeds = []
                            new_embed = discord.Embed(title=game_title)
                            for i in range(0, len(songlist)):
                                if i % 25 == 0 and i != 0:
                                    embeds.append(new_embed)
                                    new_embed = discord.Embed(title=game_title)
                                new_embed.add_field(name=songlist[i].title, value="Arranged by *{}*\n{}".format(songlist[i].arranger, songlist[i].links["pdf"]))
                            else:
                                embeds.append(new_embed)
                            for embed in embeds:
                                await message.channel.send(embed=embed)
                        else:
                            await message.channel.send("Game not found. Cancelling action")
                        want2exit = True
                    # Unknown command
                    else:
                        await message.channel.send("Unknown command. Cancelling action")
                        want2exit = True
        # Fibonacci command
        elif command[:9] == command_list[6]:
            await message.channel.send(str(fib.get_fib(int(command[9:].strip()))))
        # Trivia game commands
        elif command[:4] == command_list[7]:
            if command.strip().lower() == "flag america":
                question = trivia.get_question("flag america")
                await message.channel.send("What state is this flag from?", embed=discord.Embed().set_image(url=question.image))
            elif command.strip().lower() == "flag arms":
                question = trivia.get_question("flag arms")
                await message.channel.send("What country is this coat of arms from?", embed=discord.Embed().set_image(url="http:" + question.image))
            elif command.strip().lower() == "flag canada":
                question = trivia.get_question("flag canada")
                await message.channel.send("What province/territory is this flag from?", embed=discord.Embed().set_image(url=question.image))
            elif command.strip().lower() == "flag":
                question = trivia.get_question("flag")
                await message.channel.send("What country is this flag from?", embed=discord.Embed().set_image(url=question.image))
            strikes = 3
            game_in_progress = True
            while game_in_progress:
                try:
                    msg = await client.wait_for("message", check=lambda m : m.channel == message.channel and m.author != client.user, timeout=30)
                    if msg.content.lower() in [question.name.lower(), question.name.lower().replace("&", "and"), 
                        question.name.lower().replace("and","&"), question.name.lower().replace("the", "").strip(), 
                        question.name.lower().replace("-", ""), question.name.lower().replace("ã", "a").replace("é", "e").replace("í", "i"),
                        question.name.lower().replace("ã", "a").replace("é", "e").replace("í", "i").replace("and", "&")]:
                            await message.channel.send("You got it! The answer was {}!".format(question.name))
                            game_in_progress = False
                    else:
                        strikes -= 1
                        if strikes == 0:
                            await message.channel.send("Game over! The answer was {}!".format(question.name))
                            game_in_progress = False
                except:
                    await message.channel.send("Game over! The answer was {}!".format(question.name))
                    game_in_progress = False
        # Smashu command
        elif command[:6] == command_list[8]:
            character_moveset = smashu.get_moveset(command[6:].strip())
            move_names = list(move.name for move in character_moveset)
            move_types = ["ground", "aerial", "special", "grab"]
            want2exit = False
            move_formatting = {
                "f tilt": "forward tilt",
                "d tilt": "down tilt",
                "f smash": "forward smash",
                "d smash": "down smash",
                "nair": "neutral air",
                "fair": "forward air",
                "bair": "back air",
                "dair": "down air",
                "neutral b": [],
                "side b": [],
                "up b": [],
                "down b": [],
                "back b": []
            }
            for move in character_moveset:
                if "neutral b" in move.name:
                    move_formatting["neutral b"].append(move.name)
                elif "side b" in move.name:
                    move_formatting["side b"].append(move.name)
                elif "up b" in move.name:
                    move_formatting["up b"].append(move.name)
                elif "down b" in move.name:
                    move_formatting["down b"].append(move.name)
                elif "back b" in move.name:
                    move_formatting["back b"].append(move.name)
            await message.channel.send("What move would you like to see? (or type `ground`, `aerial`, `special`, `grab` to see lists of moves)")
            while not want2exit:
                msg = await client.wait_for("message", check=lambda m : m.channel == message.channel and m.author == message.author, timeout=60)
                msg = msg.content.strip().lower()
                # List types of moves
                if msg in move_types:
                    return_val = []
                    for move in character_moveset:
                        if move.move_type == msg:
                            return_val.append(move.name)
                    await message.channel.send("`" + "`\n`".join(return_val) + "`\nWhich of these would you like to see?")
                # Show move
                elif msg in move_formatting or msg in move_names:
                    move_name = move_formatting[msg] if msg in move_formatting else msg
                    for i in character_moveset:
                        if i.name == move_name:
                            move = i
                            break
                    else:
                        move = []
                        for i in character_moveset:
                            if i.name in list(move_formatting[msg]):
                                move.append(i)
                    if type(move) is not list:
                        move = [move]
                    for move_part in list(move):
                        embed = discord.Embed()
                        # Single-image move
                        embed.title = move_part.name.title()
                        for detail in move_part.details:
                            embed.add_field(name=detail, value=move_part.details[detail])
                        # Multi-image move
                        if len(list(move_part.animation)) > 1:
                            for i in range(0, len(list(move_part.animation)) - 1):
                                await message.channel.send(embed=discord.Embed().set_image(url=move_part.animation[i]))
                            else:
                                await message.channel.send(embed=embed.set_image(url=move_part.animation[len(list(move_part.animation)) - 1]))
                        else:
                            if move_part.animation:
                                await message.channel.send(embed=embed.set_image(url=move_part.animation[0]))
                            else:
                                await message.channel.send(embed=embed)
                    want2exit = True
                else:
                    await message.channel.send("Invalid input. Cancelling...")
                    want2exit = True
        # Percent command
        elif command[:7] == command_list[9]:
            try:
                numbers = command[7:].strip().split("/")
                percentage = float(numbers[0]) / float(numbers[1]) * 100
                await message.channel.send("{}%".format(percentage))
            except:
                await message.channel.send("Invalid input")
        # Coin command
        elif command[:4] == command_list[10]:
            def make_coin_embed(coin):
                embed = discord.Embed(title=coin.name, url=coin.link).set_image(url=coin.reverse).set_thumbnail(url=coin.obverse)
                for coin_property in coin.properties.keys():
                    embed.add_field(name=coin_property, value=coin.properties[coin_property])
                return embed
            if "random" in command:
                try:
                    if command[12:].strip() == "":
                        await message.channel.send(embed=make_coin_embed(numista.get_random_coin()))
                    else:
                        await message.channel.send(embed=make_coin_embed(numista.get_random_coin(command[12:].strip())))
                except:
                    await message.channel.send("Hmm... pulled a bad link. Try again?")
            else:
                search_topics = ["country", "year", "face value", "any additional search terms"]
                search_items = []
                for search_item in search_topics:
                    await message.channel.send("Enter {} (or type `-`)".format(search_item))
                    msg = await client.wait_for("message", check=lambda m : m.author == message.author and m.channel == message.channel, timeout=60)
                    msg = msg.content
                    if msg is None:
                        await message.channel.send("Timeout reached. Cancelling request...")
                        break
                    elif msg == "-":
                        search_items.append("")
                    else:
                        search_items.append(msg.strip())
                else:
                    coin = None
                    coin_or_coins = numista.get_coins(search_items[0], search_items[1], search_items[2], search_items[3])
                    if type(coin_or_coins) == list:
                        coins = coin_or_coins
                        message_to_send = ""
                        for i in range(0, len(coins)):
                            message_to_send += "`<{}> {}`\n".format(i, coins[i]["name"])
                        await message.channel.send(message_to_send + "Enter the number of the coin you'd like to see")
                        msg = await client.wait_for("message", check=lambda m : m.author == message.author and m.channel == message.channel, timeout=60)
                        msg = msg.content
                        if msg is None:
                            await message.channel.send("Timeout reached. Cancelling request...")
                        elif msg in map(lambda x: str(x), range(0, len(coins))):
                            coin = numista.get_coin_by_link(coins[int(msg.strip())]["link"])
                        else:
                            await message.channel.send("Invalid range. Cancelling request...")
                    elif coin_or_coins == False:
                        await message.channel.send("No coins found. Maybe you were *toooo* specific?")
                    else:
                        coin = coin_or_coins
                if coin:
                    await message.channel.send(embed=make_coin_embed(coin))
        # Cat command
        elif command[:3] == command_list[11]:
            if command[3:].strip() == "list":
                await message.channel.send("Here's the list of cats available to see:\n`{}`".format("`\n`".join(cat.list_cats())))  
            else:
                my_cat = cat.get_cat_image(command[3:].strip())
                await message.channel.send("Presenting... {}!".format(my_cat[0]), file=discord.File(my_cat[1], filename=my_cat[1]))
        # Soundtrack command
        elif command[:10] == command_list[12]:
            async def send_album(_album):
                embeds = []
                for disk in _album.songlist:
                    new_embed = discord.Embed(title=_album.title + " (Disk {})".format(str(disk[0].disk_number)), url=_album.link)
                    try: new_embed.set_thumbnail(url=_album.art)
                    except: pass
                    for i in range(0, len(disk)):
                        if i % 25 == 0 and i != 0:
                            embeds.append(new_embed)
                            new_embed = discord.Embed(title=_album.title + " (Disk {})".format(str(disk[0].disk_number)), url=_album.link)
                            try: new_embed.set_thumbnail(url=_album.art)
                            except: pass
                        new_embed.add_field(name=str(disk[i].track_number) + " - " + disk[i].title, value=disk[i].link)
                    else:
                        embeds.append(new_embed)
                return embeds
            search_term = command[10:].strip()
            message_to_send = ""
            albums = khi.search_albums(search_term)
            flag = True
            if len(albums) == 1:
                album = khi.get_album_by_link(albums[0]["link"])
            elif albums == []:
                await message.channel.send("No results found. Try being a little less specific?")
                flag = False
            else:
                for i in range(0, min(20, len(albums))):
                    message_to_send = message_to_send + "`<{}> {}`\n".format(i, albums[i]["title"])
                await message.channel.send(message_to_send + "Enter the number of the album you'd like to see")
                msg = await client.wait_for("message", check=lambda m : m.author == message.author and m.channel == message.channel, timeout=60)
                msg = msg.content
                if msg is None:
                    await message.channel.send("Timeout reached. Cancelling request...")
                elif msg in map(lambda x: str(x), range(0, len(albums))):
                    album = khi.get_album_by_link(albums[int(msg)]["link"])
                else:
                    await message.channel.send("Invalid range. Cancelling request...")
                    flag = False
            if flag:
                embeds = []
                total_songs = 0
                for disk in album.songlist:
                    total_songs += len(disk)
                if total_songs > 50:
                    await message.channel.send("There's a lot of songs in this album, are you sure you want me to list them all? (Otherwise I'll just get you the main link)")
                    response = await client.wait_for("message", check=lambda m : m.author == message.author and m.channel == message.channel, timeout=60)
                    if response.content.lower().strip() in ["yes", "y", "ye"]:
                        embeds = await send_album(album)
                        for embed in embeds:
                            await message.channel.send(embed=embed)
                    else:
                        try: embed = discord.Embed(title=album.title, url=album.link).set_thumbnail(url=album.art)
                        except: embed = discord.Embed(title=album.title, url=album.link)
                        await message.channel.send(embed=embed)
                else:
                    embeds = await send_album(album)
                    for embed in embeds:
                        await message.channel.send(embed=embed)
        # Blackjack command
        elif command[:9] == command_list[13]:
            # Take either player or computer hand and write out its contents in a specific format
            def display_hand(hand):
                return_value = ""
                for card in hand:
                    return_value = return_value + "`{}` ".format(card)
                return return_value
            def get_hand_value(hand):
                high_val_aces = 0
                total_value = 0
                for card in hand:
                    value = card[:-1]
                    if value == "A":
                        high_val_aces += 1
                        total_value += 11
                    elif value in ["J", "Q", "K"]:
                        total_value += 10
                    else:
                        total_value += int(value)
                if total_value > 21:
                    for i in range(0, high_val_aces):
                        total_value -= 10
                        if total_value <= 21:
                            break
                return total_value
            deck = cards.get_shuffled_deck()
            player_hand = [deck[0], deck[1]]
            computer_hand = [deck[2], deck[3]]
            deck_index = 4      # Deck index will point to the next value to return
            # Player's turn
            player_turn = True
            await message.channel.send("Your cards:\n{}\nWhat will you do?\n[`Hit`] [`Stand`] [`Cancel`]".format(display_hand(player_hand)))
            while player_turn:
                response = await client.wait_for("message", check=lambda m : m.author == message.author and m.channel == message.channel, timeout=30)
                try: response = response.content.lower().strip()
                except: 
                    await message.channel.send("Timeout reached. Cancelling game...")
                    break
                # Player wants to hit
                if response in ["hit", "h"]:
                    player_hand.append(deck[deck_index])
                    deck_index += 1
                    await message.channel.send("Your cards:\n{}".format(display_hand(player_hand)))
                    if get_hand_value(player_hand) > 21: 
                        await message.channel.send("Bust!")
                        player_turn = False
                    else:
                        await message.channel.send("What will you do?\n[`Hit`] [`Stand`] [`Cancel`]")
                # Player wants to stand
                elif response in ["stand", "s"]:
                    await message.channel.send("You decide to stand")
                    player_turn = False
                # Player wants to cancel game
                elif response in ["cancel", "c"]:
                    await message.channel.send("Cancelling game...")
                    break
                # Invalid response
                else:
                    await message.channel.send("Invalid response. Please respond with `Hit`, `Stand`, or `Cancel`")
            # Computer turn
            else:
                computer_turn = True
                computer_reply = ["My cards are:\n{}".format(display_hand(computer_hand))]
                player_score = get_hand_value(player_hand)
                computer_score = get_hand_value(computer_hand)
                while computer_turn:
                    # Computer always stands if player busts
                    if player_score > 21:
                        computer_reply.append("I decide to stand")
                        computer_turn = False
                    # Computer always hits if it's losing
                    elif computer_score < player_score:
                        computer_reply.append("I decide to hit")
                        computer_hand.append(deck[deck_index])
                        deck_index += 1
                        computer_reply.append("My cards:\n{}".format(display_hand(computer_hand)))
                        if get_hand_value(computer_hand) > 21:
                            computer_reply.append("Bust!")
                            computer_turn = False
                    # Stand if the computer is tied or will win
                    else:
                        computer_reply.append("I decide to stand")
                        computer_turn = False
                # See who won
                else:
                    computer_score = get_hand_value(computer_hand)
                    await message.channel.send("\n".join(computer_reply))
                    game_outcome = ""
                    if player_score > 21 and computer_score > 21:
                        game_outcome = "draw"
                    elif player_score > 21:
                        game_outcome = "lose"
                    elif computer_score > 21:
                        game_outcome = "win"
                    elif computer_score > player_score:
                        game_outcome = "lose"
                    elif player_score > computer_score:
                        game_outcome = "win"
                    else:
                        game_outcome = "draw"
                    if game_outcome == "win":
                        await message.channel.send("You win! Congratulations!!")
                    elif game_outcome == "lose":
                        await message.channel.send("You lose! Better luck next time")
                    else:
                        await message.channel.send("It's a draw!")
        #TODO: Add more commands here
        else:
            await message.channel.send("Command not found. Try typing `p.help` to see a list of all commands")

client.run(TOKEN)