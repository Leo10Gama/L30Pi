# L30Pi
I recently began learning Python, since I figured it would help me improve myself as a programmer, and now I think I am ready to take on my first "real" Python project!
This application uses the discord.py API to communicate with other Discord users and perform simple tasks. As time goes on, I will implement more and more features into the bot, not just to showcase the things I have learned, but also to continue learning what I can and can't do with this incredible language.

Please note that the Discord token is hidden in a .env file on my personal computer to prevent people from 'hacking into my bot' with malicious intent. The .env file simply contains the Discord Token that acts as the bot's password

The bot uses a few specific imports to operate the way that it does. Using the `os` and `dotenv` modules, the bot is able to sign in using a token saved in a .env file on my computer. Additionally, some of the extra modules I created make use of `requests` and `BeautifulSoup`, which are used together to webscrape from various sites. The information I pull from those sites are then formatted as I desire.
Primarily, the bot operates using the `discord.py` API provided by Discord. This API allows the bot to communicate with the user(s) in various ways. For instance, it is able to read messages, send messages, and prepare embeds, which can be used in tandom with other modules for things like simple games. 
