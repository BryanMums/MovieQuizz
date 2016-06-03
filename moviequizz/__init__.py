def joke():
    return (u'Wenn ist das Nunst\u00fcck git und Slotermeyer? Ja! ... '
            u'Beiherhund das Oder die Flipperwaldt gersput.')
			
def run():
	import moviequizz
	import asyncio
	DEBUG = True

	loop = asyncio.get_event_loop()
	loop.set_debug(DEBUG)
	bot = moviequizz.Moviequizz()
	loop.run_until_complete(bot.connect())
	loop.close()