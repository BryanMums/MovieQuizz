import asyncio
import json
import aiohttp
import random
import codecs
import operator

from api import api_call
from config import DEBUG, TOKEN

class moviequizz:
    def __init__(self, token=TOKEN):
        self.token = token
        self.rtm = None
        self.api = {
            "help": self.help,
            "rank": self.rank,
            "ranking": self.ranking,
            "ask" : self.question
        }
        self.party = {}

        # Codecs pour le format de texte (UTF-8)
        json_data = codecs.open("ressources/questions.json", "r", "utf-8")
        self.questions = json.load(json_data)

    async def sendText(self, message, channel_id, user_name, team_id):
        """Sends a text message to the channel"""
        return await api_call('chat.postMessage', {"type": "message",
                                                   "channel": channel_id,
                                                   "text": "<@{0}> {1}".format(user_name["user"]["name"], message),
                                                   "team": team_id})

    # Retourne si la reponse donnee a la question est juste.
    async def reponse(self, user_id, text, channel_id, user_name, team_id ):
        if self.party[user_id] == text: # Il a entre la bonne reponse.
            json_data = codecs.open("ressources/ranking.json", "r", "utf-8")
            data = json.load(json_data)

            if data.get(str(user_id)):
                data[str(user_id)] = data.get(str(user_id)) + 50
            else:
                data[str(user_id)] = 50

            with open('ressources/ranking.json', 'w') as outfile:
                json.dump(data, outfile)

            # Affichage d'un message de reussite !
            message = "Felicitations ! Bonne reponse !\n\n" \
                      "Veuillez entrer une commande"
            return await self.sendText(message, channel_id, user_name, team_id)
        else:
            # Affichage d'un message d'echec.
            message = "Biiiip ! Mauvaise reponse ! \n\n" \
                      "Veuillez entrer une commande"
            return await self.sendText(message, channel_id, user_name, team_id)

    # Permet de poser la question et l'ajoute a party
    async def question(self, channel_id,user_name, user_id, team_id):
        # Recuperation aleatoire d'un element de la liste de question
        q = random.choice(self.questions)

        # Enregistre tableau de reponse et bonne reponse
        answers = q["badAnswers"] + [q["goodAnswer"]]
        goodAnswer = q["goodAnswer"]

        # Melange l'ordre des reponses
        random.shuffle(answers)

        # Cree un tableau de choix
        choices = {}

        for i in range(len(answers)):
            # Possibilities start at 1
            choices[str(i + 1)] = answers[i];

        message = q["question"]
        message += "\n"

        for key in sorted(choices):
            message += "Reponse %s : %s" % (key, choices[key])
            message += "\n"

        # On recupere l'id de la bonne reponse
        id = 0
        for i in range(len(choices)):
            if choices[str(i + 1)] == goodAnswer:
                id = i + 1

        self.party[user_id] = str(id)
        return await self.sendText(message, channel_id,user_name, team_id)

    async def rank(self, channel_id,user_name, user_id, team_id):
        json_data = codecs.open("ressources/ranking.json", "r", "utf-8")
        data = json.load(json_data)
        message = ""
        if data.get(str(user_id)):
            message += "Votre score est de : " + str(data[str(user_id)])
            l = sorted(data.items(), key=operator.itemgetter(1))
            l = l[::-1]
            rank = l.index((str(user_id), data.get(str(user_id)))) + 1

            message += "\n Place au classement : " + str(rank)

        else:
            message += "Vous n'avez pas encore de score. Veuillez jouer !"

        return await self.sendText(message, channel_id, user_name, team_id)

    async def ranking(self, channel_id, user_name, user_id, team_id):
        json_data = codecs.open("ressources/ranking.json", "r", "utf-8")
        data = json.load(json_data)
        message = "Top 10 du Quizz Movie : \n"
        l = sorted(data.items(), key=operator.itemgetter(1))
        l = l[::-1]
        l = l[0:10]
        for i in range(len(l)):
            message += "Number "+str(i+1)+ " : "+ l[i][0] + str(l[i][1]) + "\n"
        return await self.sendText(message, channel_id, user_name, team_id)

    async def help(self, channel_id,user_name, user_id, team_id):
        """Displays the help message to the channel"""
        helpMessage = "Welcome to our MovieQuizz bot ! \n" \
                      "This bot is here to test your film knowledge. \n" \
                      "Here are the commands : \n" \
                      " - ask : question you about a movie. \n" \
                      " - rank : display your ranking  \n" \
                      " - help : You already know this one, don't you. \n" \
                      "Have fun !"
        return await self.sendText(helpMessage, channel_id, user_name, team_id)

    async def error(self, channel_id,user_name, user_id, team_id):
        """displays the error message to the channel, in case of bad input"""
        error = "Command not found. Type 'help' for a list of valid commands."
        return await self.sendText(error, channel_id, user_name, team_id)

    async def process(self, message):
        """Processes input messages."""

        if message.get('type') == 'message' and message.get('username') != 'bot':

            # Un-comment this next line if your bot should be active in all channels he's invited in
            channel_id = message.get('channel')

            # Team-related entries
            team_id = self.rtm['team']['id']  # gets id of the active team

            # User-related entries
            user_id = message.get('user')
            user_name = await api_call('users.info',  # gets user name based on id
                                       {'user': message.get('user')})

            # message related entries
            message_text = message.get('text')

            # On regarde si l'utilisateur doit repondre a une question.
            if user_id in self.party:
                # On regarde si l'utilisateur a donnee une bonne reponse
                print(await self.reponse(user_id,message_text,channel_id,user_name,team_id))
                # Enlever l'utilisateur des questions en cours.
                del self.party[user_id]
            else:
                action = self.api.get(message_text) or self.error
                print(await action(channel_id,user_name, user_id, team_id))

    async def connect(self):
        """Connects the bot to Slack"""

        self.rtm = await api_call('rtm.start')
        assert self.rtm['ok'], self.rtm['error']

        with aiohttp.ClientSession() as client:
            async with client.ws_connect(self.rtm["url"]) as ws:
                async for msg in ws:
                    assert msg.tp == aiohttp.MsgType.text
                    message = json.loads(msg.data)
                    asyncio.ensure_future(self.process(message))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_debug(DEBUG)
    bot = moviequizz(TOKEN)
    loop.run_until_complete(bot.connect())
    loop.close()