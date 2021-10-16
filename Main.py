from KeyboardListener import *
from CrimeInference import *
import numpy
import time
import tts

# Cette fonction retourne le format d'une expression logique de premier ordre


def results_as_string(results):
    res = ''
    for result in results:
        # synrep = syntactic representation
        # semrep = semantic representation
        for (synrep, semrep) in result:
            res += str(semrep)
    return res

# Cette fonction transforme une phrase en fraçais dans une expression logique du premier ordre


def to_fol(fact, grammar):
    sent = results_as_string(nltk.interpret_sents(fact, grammar))
    print(sent)
    return sent

# Cette fonction demande une question qui doit être répondu par texte


def askTextQuestion(question):
    print(question)
    tts.playText(question)
    response = input()
    return response

# Cette fonction demande une question qui doit être répondu vocalement


def askVocalQuestion(question):
    print(question)
    tts.playText(question)
    response = tts.recordText()
    return response

# Cette fonction demande une question qui doit être répondu par Oui(1) ou Non(2)


def askYesNoQuestion(question):
    print(question + " (1=Oui, 2=Non)")
    tts.playText(question)
    response = k.press()
    return response


def verifyRoom(room):
    # On détermine une heure apres le crime = quelle heure
    uneHeureApres = agent.get_crime_hour() + 1
    agent.add_clause(
        'UneHeureApresCrime({})'.format(uneHeureApres))

    response = ""
    # Dans la Cuisine
    if room == "Cuisine":
        # Détection du poignard
        print("Je vois le poignard dans la " + str(room))
        tts.playText("Je vois le poignard dans la " + str(room))
        fact = ['Le poignard est dans la ' + str(room)]
        agent.add_clause(to_fol(fact, 'grammars/arme_piece.fcfg'))
    # Dans la Salle_de_bain
    elif room == "Salle_de_bain":
        # On demande si il y a des personnes dans la piece tant que la réponse n'est pas "Non"
        while response != "Non":
            response = askYesNoQuestion(
                "Est-ce qu'il y a des personnes dans la pièce?")
            input()
            if response == "Oui":
                # On demande le nom de la personne si la réponse précédente est "Oui"
                response = askTextQuestion("Qui est dans la pièce?")
                personnePiece = response
                fact = [response + " est dans la " + str(room)]
                agent.add_clause(
                    to_fol(fact, 'grammars/personne_piece.fcfg'))
                # On demande dans quelle piece était la personne une heure après le crime
                response = askVocalQuestion(
                    "Dans quelle pièce était " + str(personnePiece) + " à " + str(uneHeureApres) + "h ?")
                fact = [str(personnePiece) + " se trouvait dans la " +
                        response + " à " + str(uneHeureApres) + "h"]

                agent.add_clause(
                    to_fol(fact, 'grammars/personne_piece_heure.fcfg'))
    # Dans le Salon
    if room == "Salon":
        # On demande si il y a des armes dans la piece tant que la réponse n'est pas "Non"
        while response != "Non":
            response = askYesNoQuestion(
                "Est-ce qu'il y a une arme dans le " + str(room) + "?")
            input()
            if response == "Oui":
                # On demande le type d'arme si la réponse précédente est "Oui"
                response = askTextQuestion("De quel type d'arme s'agit-il?")
                personnePiece = response
                fact = ["Le " + response + " est dans la " + str(room)]
                agent.add_clause(
                    to_fol(fact, 'grammars/arme_piece.fcfg'))
    # Dans la Cave
    elif room == "Cave":
        # Détection d'une corde
        print("Je vois la corde dans la " + str(room))
        tts.playText("Je vois la corde dans la " + str(room))
        fact = ['La corde est dans la ' + str(room)]
        agent.add_clause(to_fol(fact, 'grammars/arme_piece.fcfg'))
    # Dans le Bureau
    elif room == "Bureau":
        # Détection de Violet
        print("Je vois Violet dans le " + str(room))
        tts.playText("Je vois Violet dans le " + str(room))
        fact = ['Violet est dans le ' + str(room)]
        agent.add_clause(to_fol(fact, 'grammars/personne_piece.fcfg'))
        # On demande dans quelle piece était Violet une heure après le crime
        response = askVocalQuestion(
            "Dans quelle pièce était Violet à " + str(uneHeureApres) + "h ?")
        fact = ["Violet se trouvait dans la " +
                response + " à " + str(uneHeureApres) + "h"]
        agent.add_clause(
            to_fol(fact, 'grammars/personne_piece_heure.fcfg'))
    # Dans la Bibliotheque
    elif room == "Bibliotheque":
        # Détection du Chandelier
        print("Je vois le chandelier dans la " + str(room))
        tts.playText("Je vois le chandelier dans la " + str(room))
        fact = ['Le chandelier est dans la ' + str(room)]
        agent.add_clause(to_fol(fact, 'grammars/arme_piece.fcfg'))

    # Dans le Hall
    elif room == "Hall":
        # On demande si le corps de la Victime possède des marques de blessure
        response = askVocalQuestion(
            "Japperçois le corps de " + str(agent.get_victim()) + " dans cette pièce. Possède-t-il des marques de blessure particulières?")
        fact = [response]
        agent.add_clause(to_fol(fact, 'grammars/personne_marque.fcfg'))
        # Détection de la Victime dans la pièce
        fact = [str(agent.get_victim()) + ' est dans le ' + str(room)]
        agent.add_clause(to_fol(fact, 'grammars/personne_piece.fcfg'))
        # On demande si il y a d'autres personnes dans la piece tant que la réponse n'est pas "Non"
        while response != "Non":
            response = askYesNoQuestion(
                "Est-ce qu'il y a d'autres personnes dans la pièce?")
            input()
            if response == "Oui":
                # On demande le nom de la personne si la réponse précédente est "Oui"
                response = askTextQuestion("Qui d'autre est dans la pièce?")
                personnePiece = response
                fact = [response + " est dans la " + str(room)]
                agent.add_clause(
                    to_fol(fact, 'grammars/personne_piece.fcfg'))
                # On demande dans quelle piece était la personne une heure après le crime
                response = askTextQuestion(
                    "Dans quelle pièce était " + str(personnePiece) + " à " + str(uneHeureApres) + "h ?")
                fact = [str(personnePiece) + " se trouvait dans la " +
                        response + " à " + str(uneHeureApres) + "h"]

                agent.add_clause(
                    to_fol(fact, 'grammars/personne_piece_heure.fcfg'))


# Création d'une instance de CrimeInference
agent = CrimeInference()
print("\n\n ======== Faits de base ======== \n")
# Ouverture du fichier "facts" qui contient les faits de départ
with open("facts") as fileF:
    facts = [line.split('\n') for line in fileF]

# Ajout d'une clause "Personne_Morte" correspondant à la première ligne du fichier
agent.add_clause(to_fol(facts[0], 'grammars/personne_morte.fcfg'))
facts.pop(0)

# Ajout de clauses "Personne_Vivante" correspondant au reste des lignes du fichier
for fact in facts:
    agent.add_clause(to_fol(fact, 'grammars/personne_vivant.fcfg'))

# Définition des différentes pièces disponibles dans le jeu
list_piece = ["Cuisine", "Salle_de_bain", "Salon",
              "Cave", "Bureau", "Bibliotheque", "Hall"]

# Création d'une instance de Keyboard listener pour se déplacer entre les pièces
k = KeyboardListener(list_piece)

print("\n ======== Début de l'enquête ======== \n")
# On demande à quelle heure le meurtre à eu lieu
response = askTextQuestion(
    "À quelle heure " + str(agent.get_victim()) + " est-elle morte?")
fact = [str(agent.get_victim()) + ' est morte à ' + response]
agent.add_clause(
    to_fol(fact, 'grammars/personne_morte_heure.fcfg'))

room = k.getCurrentRoom()
keepGoing = True
# On continue tant qu'on appui pas sur Escape pour terminer l'enquête
while keepGoing:
    tts.playText("Je rentre dans le " + str(room))
    # Vérification de la pièce dans laquelle on entre
    verifyRoom(room)
    time.sleep(1)
    # Gestion de la touche de déplacement
    room = k.press()
    if(room == "esc"):
        keepGoing = False

print("\n ======== Déduction du coupable ======== \n")
# Conclusions
print("\n\nPièce du crime : ", agent.get_crime_room())
print("Arme du crime : ", agent.get_crime_weapon())
print("Personne victime : ", agent.get_victim())
print("Heure du crime : ", agent.get_crime_hour())
print("Meurtrier : ", agent.get_suspect())
print("Personnes innocentes : ", agent.get_innocent())
print("\n\n")
