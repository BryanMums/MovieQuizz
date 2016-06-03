import asyncio
import json
import aiohttp
import random
import codecs
import operator

from api import api_call
from config import DEBUG, TOKEN


class Moviequizz:
    """Bot main class."""

    def __init__(self, token=TOKEN):
        """
        Constructor of bot class.
        The token is either passed in argument or read in the config file.

       :param TOKEN: the slack bot generated token
        """
        self.token = token # Slack bot token
        self.rtm = None # Real Time Messaging connection
        self.api = { # Dict of available bot commands
            "help": self.help, # For the help command
            "rank": self.rank, # For the rank command (will show playing user score)
            "ranking": self.ranking, # For the ranking command (will show full ranking)
            "ask" : self.question # For the question command (will ask a question)
        }
        self.currentAskedQuestions = {} # Asked questions during the game (not yet answered)

        # Codecs pour le format de texte (UTF-8)
        json_data = codecs.open("ressources/questions.json", "r", "utf-8")
        self.questions = json.load(json_data) # Read the json questions file and create a dict


    async def sendText(self, message, channel_id,user_infos, team_id):
        """
        Sends a message to the user.

       :param message: the sent message
       :param channel_id: id of channel
       :param user_infos: the receiver
       :param team_id: team id
        """
        # Return the message to send with every information
        return await api_call('chat.postMessage', {"type": "message",
                                                   "channel": channel_id,
                                                   "text": "<@{0}> {1}".format(user_infos["user"]["name"], message),
                                                   "team": team_id})

    async def reponse(self, user_id, answeredQuestionId, channel_id,user_infos, team_id):
        """
        Tests if the player answer is correct. Called when the bot receive an answer.
        Add points to ranking when correct and display a message (failure or success).

       :param user_id: user id
       :param answeredQuestionId: the answered id from the user
       :param channel_id: id of channel
       :param user_infos: the receiver
       :param team_id: team id
        """

        if self.currentAskedQuestions[user_id] == answeredQuestionId: # Test if the answered question id is correct
            data = {}
            with codecs.open("ressources/ranking.json", "r", "utf-8") as json_data: # Open the ranking file to update it (read mode)

                data = json.load(json_data) # Dict from json data ranking file

                user = "{}-{}".format(user_infos["user"]["name"], str(team_id)) # The user string name to get/write in the file

                pointsToAdd = 50 # Easy to change, could be a class property or question-specific (new field in JSON?)

                if data.get(user): # If user exists
                    data[user] = data.get(user) + pointsToAdd
                else: # If the user is new (first time good answer)
                    data[user] = pointsToAdd

            with open('ressources/ranking.json', 'w') as outfile: # Open ranking file (write mode)
                json.dump(data, outfile) # Save the modifications (new scores entry or update)

            # Success message
            message = "Felicitations ! Bonne reponse !\n\n" \
                      "Veuillez entrer une commande"
            return await self.sendText(message, channel_id,user_infos, team_id)
        else:
            # Failure message
            message = "Biiiip ! Mauvaise reponse ! \n\n" \
                      "Veuillez entrer une commande"
            return await self.sendText(message, channel_id,user_infos, team_id)

    async def question(self, channel_id,user_infos, user_id, team_id):
        """
        Asks a question and add it to the currentAskedQuestions

       :param message: the sent message
       :param channel_id: id of channel
       :param user_infos: the receiver
       :param team_id: team id
        """

        q = random.choice(self.questions) # Random question selection from list
        answers = q["badAnswers"] + [q["goodAnswer"]] # Save all possible answers
        goodAnswer = q["goodAnswer"] # Save the good answer
        random.shuffle(answers) # Shuffle everything

        choices = {} # Dict of choices

        for i in range(len(answers)): # For every possible answer
            choices[str(i + 1)] = answers[i]; # Fill the choices dict with normal people understandable indexes

        message = "{} \n".format(q["question"]) # Start the string question message

        for key in sorted(choices):
            message += ("Reponse {} : {} \n").format(key, choices[key]) # Add choices to question message

        id = 0
        for i in range(len(choices)):
            if choices[str(i + 1)] == goodAnswer: # Retrieve the good answer id (lol). Should probably do differently...
                id = i + 1

        self.currentAskedQuestions[user_id] = str(id) # Put the entry in the dict with good answer id
        return await self.sendText(message, channel_id,user_infos, team_id)


    async def rank(self, channel_id,user_infos, user_id, team_id):
        """
        Shows the rank and score of the current playing user

       :param channel_id: id of channel
       :param user_infos: the receiver
       :param user_id: user id
       :param team_id: team id
        """

        with codecs.open("ressources/ranking.json", "r", "utf-8") as json_data:
            data = json.load(json_data)

            user = "{}-{}".format(user_infos["user"]["name"], str(team_id)) # User string to write

            if data.get(user):
                # (Epic line to) get the position from ranking array revert sorted depending on the user
                rank = sorted(data.items(), key=operator.itemgetter(1))[::-1].index((user, data.get(user))) + 1
                # Score info message
                message = "Votre score est de : {} \n Place au classement : {}".format(str(data[user]), str(rank))
            else:
                message = "Vous n'avez pas encore de score. Veuillez jouer !" # Never played yet
        return await self.sendText(message, channel_id,user_infos, team_id)


    async def ranking(self, channel_id,user_infos, user_id, team_id):
        """
        Shows the top 10 ranking list with the best players ever.

       :param channel_id: id of channel
       :param user_infos: the receiver
       :param team_id: team id
        """
        message = "Top 10 du Quizz Movie : \n" # Begin the ranking message

        with codecs.open("ressources/ranking.json", "r", "utf-8") as json_data: # Open the ranking file read mode
            data = json.load(json_data)

            # Get the top ten players reverse score ordered
            l = sorted(data.items(), key=operator.itemgetter(1), reverse=True)[0:10]

            for i in range(len(l)): # For each top ten players
                message += "Numéro {} : {}, Score : {}\n".format(str(i+1), l[i][0], str(l[i][1]))
        return await self.sendText(message, channel_id,user_infos, team_id)


    async def help(self, channel_id,user_infos, user_id, team_id):
        """
        Shows help and commands for the moviequizz bot.

       :param channel_id: id of channel
       :param user_infos: the receiver
       :param team_id: team id
        """
        helpMessage = "Bienvenue dans l'aide du bot MovieQuizz ! \n" \
                      "Ce bot va tester vos connaissances cinématographiques ! \n" \
                      "Les commandes disponibles sont les suivantes : \n" \
                      " - ask : vous questionne à propos d'un film \n" \
                      " - rank : affiche votre position et score  \n" \
                      " - ranking : affiche les 10 meilleures joueurs  \n" \
                      " - help : Vous connaissez déjà celle-là. \n" \
                      "Amusez-vous bien les lapins !"
        return await self.sendText(helpMessage, channel_id,user_infos, team_id)

    async def error(self, channel_id,user_infos, user_id, team_id):
        """
        Shows the error message to the channel, in case of bad input

       :param channel_id: id of channel
       :param user_infos: the receiver
       :param team_id: team id
        """
        # Message de commande incorrecte
        error = "Commande invalide. Veuillez utiliser la commande [help] pour plus d'informations."
        return await self.sendText(error, channel_id,user_infos, team_id)

    async def process(self, message):
        """
        Processes input messages.

       :param channel_id: id of channel
       :param user_infos: the receiver
       :param team_id: team id
        """

        # If the message is a 'message' type (from player)
        if message.get('type') == 'message' and message.get('subtype') != 'bot_message':

            channel_id = message.get('channel') # Channel id
            team_id = self.rtm['team']['id']  # Get id of the active team
            user_id = message.get('user') # Get user id

            user_infos = await api_call('users.info', {'user': message.get('user')}) # all user infos

            message_text = message.get('text') # Message

            # Check if user has to answer a question
            if user_id in self.currentAskedQuestions:
                # Check if user gave a good answer
                print(await self.reponse(user_id, message_text, channel_id, user_infos, team_id))
                # Remove user from current asked questions
                del self.currentAskedQuestions[user_id]
            else:
                action = self.api.get(message_text.lower()) or self.error
                print(await action(channel_id, user_infos, user_id, team_id))

    async def connect(self):
        """
        Connects the bot to Slack
        """

        self.rtm = await api_call('rtm.start') # Start the connection
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
    bot = Moviequizz(TOKEN)
    loop.run_until_complete(bot.connect())
    loop.close()