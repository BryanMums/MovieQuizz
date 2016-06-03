import moviequizz
import asyncio
DEBUG = True

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.set_debug(DEBUG)

	bot = moviequizz.Moviequizz()
	loop.run_until_complete(bot.connect())
	loop.close()