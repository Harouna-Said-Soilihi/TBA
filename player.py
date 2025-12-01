# Define the Player class.
class Player():
:
    """
    Classe représentant un joueur dans un jeu d'aventure textuel.

    Cette classe gère l’état du joueur, notamment son nom et la pièce
    dans laquelle il se trouve. Elle permet également de déplacer le
    joueur dans une direction donnée, en fonction des sorties disponibles
    de la pièce actuelle.

    Attributs :
     
    name : str
        Le nom du joueur.
    current_room : Room or None
        La pièce dans laquelle le joueur se trouve actuellement.

    Méthodes :
    
    move(direction)
        Déplace le joueur dans la direction indiquée si une sortie existe
        depuis la pièce actuelle. Affiche la description de la nouvelle
        pièce et renvoie True en cas de succès, False sinon.

    Exceptions : 
    
    KeyError
        Levée si la direction demandée n’existe pas dans les sorties de la pièce.
        (Cela arrive si l’appelant ne vérifie pas au préalable l’existence de la sortie.)

    Exemples :
   
    >>> from Room import Room
    >>> r1 = Room("Hall", "dans un grand hall d'entrée")
    >>> r2 = Room("Jardin", "dans un jardin fleuri")
    >>> r1.exits["sud"] = r2
    >>> p = Player("Alice")
    >>> p.current_room = r1
    >>> p.move("sud")
    True
    >>> p.current_room is r2
    True
    >>> p.move("nord")
    Traceback (most recent call last):
        ...
    KeyError: 'nord'
    """
    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        next_room = self.current_room.exits[direction]

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Set the current room to the next room.
        self.current_room = next_room
        print(self.current_room.get_long_description())
        return True

    
