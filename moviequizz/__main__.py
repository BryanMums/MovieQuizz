import asyncio
import os

from . import moviequizz

if __name__ == "__main__":
	token = os.environ.get('TOKEN')
	loop = asyncio.get_event_loop()
	bot = moviequizz.Moviequizz(token)
	loop.run_until_complete(bot.connect())
	loop.close()