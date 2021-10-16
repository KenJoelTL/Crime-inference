import keyboard


class KeyboardListener:

    def __init__(self, list_piece):
        self.current_piece_index = 0
        self.list_piece = list_piece
    # Cette fonction gère l'action a effectuer en fonction de la touche appuyée

    def press(self):
        key = ""
        # Mapping entre touches de clavier et fonctions
        print("\nAppuyez sur une touche pour vous déplacer ou continuer")
        while True:
            if keyboard.is_pressed("left"):
                key = self.handleLeftKey()
                break
            elif keyboard.is_pressed("right"):
                key = self.handleRightKey()
                break
            elif keyboard.is_pressed("up"):
                key = self.handleUpKey()
                break
            elif keyboard.is_pressed("down"):
                key = self.handleDownKey()
                break
            elif keyboard.is_pressed("1"):
                key = self.handleKeyOne()
                break
            elif keyboard.is_pressed("2"):
                key = self.handleKeyTwo()
                break
            elif keyboard.is_pressed("esc"):
                # le programme se termine automatiquement lorsqu'on appuie sur la touche esc / échap
                key = "esc"
                break
        return key

    # Cette fonction gère la touche Fleche Gauche
    def handleLeftKey(self):
        print("\r\nPièce précédente")
        if self.current_piece_index > 0:
            self.current_piece_index = self.current_piece_index - 1
        else:
            self.current_piece_index = len(self.list_piece)-1
        return self.getCurrentRoom()
    # Cette fonction gère la touche Fleche Droite

    def handleRightKey(self):
        print("\r\nPièce suivante")
        if self.current_piece_index < len(self.list_piece)-1:
            self.current_piece_index = self.current_piece_index + 1
        else:
            self.current_piece_index = 0
        return self.getCurrentRoom()
    # Cette fonction gère la touche Fleche Haut

    def handleUpKey(self):
        print("\r\nPremière pièce")
        self.current_piece_index = 0
        return self.getCurrentRoom()
    # Cette fonction gère la touche Fleche Down

    def handleDownKey(self):
        if not keyboard.is_pressed("2"):
            print("\r\nDernière pièce")
            self.current_piece_index = len(self.list_piece)-1
            return self.getCurrentRoom()
    # Cette fonction gère la touche 1

    def handleKeyOne(self):
        if keyboard.is_pressed("1"):
            print("\r\nOui")
            return "Oui"
    # Cette fonction gère la touche 2

    def handleKeyTwo(self):
        if keyboard.is_pressed("2"):
            print("\r\nNon")
            return "Non"
    # Cette fonction retourne la piece dans laquelle on se trouve présentement

    def getCurrentRoom(self):
        print("\nPièce courrante: " +
              self.list_piece[self.current_piece_index] + "\n")
        return self.list_piece[self.current_piece_index]
