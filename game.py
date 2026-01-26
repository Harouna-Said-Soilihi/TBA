# Description: Game class
# Import modules

DEBUG = True # À mettre à False pour la version finale

from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Beamer
from character import Character
from quest import Quest

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
        check = Command("check", " : afficher l'inventaire du joueur", Actions.check, 0)
        self.commands["check"] = check
        look = Command("look", " : regarder autour de soi dans la pièce actuelle", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <nom_objet> : prendre un objet dans la pièce actuelle", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <nom_objet> : déposer un objet de l'inventaire dans la pièce actuelle", Actions.drop, 1)
        self.commands["drop"] = drop
        use = Command("use", " <nom_objet> : utiliser un objet de l'inventaire", Actions.use, 1)
        self.commands["use"] = use
        charge = Command("charge", " <objet> : charger un objet magique", Actions.charge, 1)
        self.commands["charge"] = charge
        talk = Command("talk", " <nom_pnj> : parler à un personnage", Actions.talk, 1)
        self.commands["talk"] = talk
        rest = Command("rest", "permet de récupérer de l'endurance", Actions.rest, 0)
        self.commands["rest"] = rest
        self.commands["quests"] = Command("quests", " : afficher la liste des quêtes", Actions.quests, 0)
        self.commands["quest"] = Command("quest", " <titre> : détails d'une quête", Actions.quest, 1)
        self.commands["activate"] = Command("activate", " <titre> : activer une quête", Actions.activate, 1)
        self.commands["rewards"] = Command("rewards", " : afficher vos récompenses", Actions.rewards, 0)
        
        # Setup rooms

        forest = Room("Forest", "une forêt enchantée. Vous entendez une brise légère à travers la cime des arbres.")
        self.rooms.append(forest)
        tower = Room("Tower", "une immense tour en pierre qui s'élève au dessus des nuages.")
        self.rooms.append(tower)
        cave = Room("Cave", "une grotte profonde et sombre. Des voix semblent provenir des profondeurs.")
        self.rooms.append(cave)
        cottage = Room("Cottage", "un petit chalet pittoresque avec un toit de chaume. Une épaisse fumée verte sort de la cheminée.")
        self.rooms.append(cottage)
        swamp = Room("Swamp", "un marécage sombre et ténébreux. L'eau bouillonne, les abords sont vaseux.")
        self.rooms.append(swamp)
        castle = Room("Castle", "un énorme château fort avec des douves et un pont levis. Sur les tours, des flèches en or massif.")
        self.rooms.append(castle)

        # New vertical rooms
        basement = Room("Sous_sol", "un sous-sol humide et sombre. Une odeur inquiétante flotte dans l'air.")
        self.rooms.append(basement)
        tower_top = Room("Tower-Top", "au sommet de la tour, vue à couper le souffle sur le royaume.")
        self.rooms.append(tower_top)

        # Create exits for rooms

        forest.exits = {"N" : cave, "E" : None, "S" : castle, "O" : None, "U": None, "D": None}
        tower.exits = {"N" : cottage, "E" : None, "S" : None, "O" : forest, "U": tower_top, "D": None}
        cave.exits = {"N" : None, "E" : cottage, "S" : forest, "O" : None, "U": None, "D": None}
        cottage.exits = {"N" : None, "E" : None, "S" : tower, "O" : cave, "U": None, "D": basement}
        swamp.exits = {"N" : tower, "E" : None, "S" : None, "O" : castle, "U": None, "D": None}
        castle.exits = {"N" : forest, "E" : swamp, "S" : None, "O" : None, "U": None, "D": None}
        basement.exits = {"N": None, "E": None, "S": None, "O": None, "U": cottage, "D": None}
        tower_top.exits = {"N": None, "E": None, "S": None, "O": None, "U": None, "D": tower}

        # Place some items in rooms
        forest.inventory["Décoction de souci"] = {"description": "Guérit de 60PV en une minute","weight": 0.5}
        forest.inventory["Potion de sang de chevreuil"] = {"description":"Accroît l'endurance et sa régénération","weight":0.3}
        cave.inventory["kit de crochetage"] = {"description": "vous permettra d'ouvrir tout un tas de coffres et de vous incruster dans des reserves d'équipement ou de nourriture","weight": 0.1}
        tower_top.inventory["beamer"] = Beamer()

        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = swamp
        #Initialize the game with quests
        self._setup_quests()
        # Construire l'ensemble des directions valides présentes dans la map 
        self.valid_directions = set().union(*(room.exits.keys() for room in self.rooms))

        # Setup 'back' command
        back = Command("back", " : revenir à la pièce précédente visitée", Actions.back, 0)
        self.commands["back"] = back

        # Création d'un PNJ 
        gandalf = Character("Gandalf", "un magicien blanc", forest, ["Je suis Gandalf", "Abracadabra !"])
        # Ajout du PNJ dans la pièce
        forest.characters[gandalf.name] = gandalf

    def _setup_quests(self):
            """Initialize all quests."""

            # Add quests to player's quest manager
            self.player.quest_manager.add_quest(exploration_quest)
            self.player.quest_manager.add_quest(travel_quest)
            self.player.quest_manager.add_quest(discovery_quest)

    # Play the game
    def play(self):
        self.setup()
        self.print_welcome() 
        # Loop until the game is finished
        while not self.finished:
            # Get the command from the player
            self.process_command(input("> "))
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:
        # ignore None inputs (defensive)
        if command_string is None:
            return None
        command_string = command_string.strip()
        if command_string == "":
            # Ne rien afficher — on ignore la commande vide.
            return None
        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande '{command_word}' non reconnue. Entrez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            success = command.action(self, list_of_words, command.number_of_parameters)
            
            if success and command_word != "talk":
                # Ton bloc de mouvement tel quel :
                all_characters = []
                for room in self.rooms:
                    for char in room.characters.values():
                        all_characters.append(char)

                for char in all_characters:
                    old_room_name = char.current_room.name
                    if char.move():
                        if DEBUG:
                            print(f"DEBUG: {char.name} s'est déplacé de {old_room_name} vers {char.current_room.name}")
        
    # Print the welcome message
    def print_welcome(self):
        print(f"\nBienvenue {self.player.name} dans ce jeu d'aventure !")
        print("Entrez 'help' si vous avez besoin d'aide.")
        #
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()  
