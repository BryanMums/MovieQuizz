import json
import random
import codecs
import threading, msvcrt
import sys


# Codecs pour le format de texte (UTF-8)
json_data= codecs.open("ressources/questions.json", "r", "utf-8")
data=json.load(json_data)

# Récupération aléatoire d'un élément de la liste de question
q = random.choice(data)

# Enregistre tableau de réponse et bonne réponse
answers = q["answers"]
goodAnswer = q["answers"][0]

#print(goodAnswer)

# Mélange l'ordre des réponses
random.shuffle(answers)

#print(q["answers"][0])

# Crée un tableau de choix
choices = {}

for i in range(len(answers)):
    # Possibilities start at 1
    choices[str(i+1)] = answers[i];

# EMOJIS 1 / 2 / 3 Use reactions Images pas par websocket

# Affiche question et réponses (et temps disponible)
print(q["question"])
print("Vous avez 10 secondes pour répondre !")

for key in sorted(choices):
    print("Réponse %s : %s" % (key, choices[key]))

# Time and answer test
userAnswer = input("Quelle est votre réponse ?")

if choices.get(userAnswer) == goodAnswer:
    print("It's a success")
else:
    print("It's a failure")

