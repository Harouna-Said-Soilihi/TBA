# Define the Room class.

class Room:
    """
    Classe représentant une pièce dans un jeu d'aventure textuel.

    Cette classe permet de définir un lieu contenant un nom, une
    description et des sorties menant vers d'autres pièces. Elle fournit
    également des méthodes facilitant l’affichage des informations
    concernant la pièce et la navigation entre les lieux.

    Attributs :
    name : str
        Le nom de la pièce.
    description : str
        La description textuelle de la pièce.
    exits : dict
        Un dictionnaire associant une direction (str) à une autre pièce (Room).

    Méthodes :
    get_exit(direction)
        Renvoie la pièce située dans la direction donnée, ou None si
        la sortie n’existe pas.
    get_exit_string()
        Retourne une chaîne listant les sorties disponibles depuis la pièce.
    get_long_description()
        Retourne une description complète de la pièce, incluant les sorties.

    Exceptions :
    Aucune exception spécifique n’est levée par cette classe.

    Exemples :
    >>> r1 = Room("Cuisine", "dans une cuisine lumineuse")
    >>> r2 = Room("Salon", "dans un salon confortable")
    >>> r1.exits["est"] = r2
    >>> r1.get_exit("est") is r2
    True
    >>> r1.get_exit("ouest") is None
    True
    >>> "est" in r1.get_exit_string()
    True
    """

    # Define the constructor.
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}

    # Define the get_exit method.
    def get_exit(self, direction):
        # Return the room in the given direction if it exists.
        if direction in self.exits.keys():
            return self.exits[direction]
        else:
            return None

    # Return a string describing the room's exits.
    def get_exit_string(self):
        exit_string = "Sorties: "
        for exit in self.exits.keys():
            if self.exits.get(exit) is not None:
                exit_string += exit + ", "
        exit_string = exit_string.strip(", ")
        return exit_string

    # Return a long description of this room including exits.
    def get_long_description(self):
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        if not self.inventory:
            return "Il n'y a rien ici."

        result = "La pièce contient :\n"

        for name, infos in self.inventory.items():
            result += f"    - {name} : {infos['description']} ({infos['weight']} kg)\n"

        return result
    def look(self):
        msg = f"\n{self.description}\n"
        msg += self.get_inventory()
        return msg
