# Description: The actions module.

# The actions module contains the functions that are called when a command is executed.
# Each function takes 3 parameters:
# - game: the game object
# - list_of_words: the list of words in the command
# - number_of_parameters: the number of parameters expected by the command
# The functions return True if the command was executed successfully, False otherwise.
# The functions print an error message if the number of parameters is incorrect.
# The error message is different depending on the number of parameters expected by the command.


# The error message is stored in the MSG0 and MSG1 variables and formatted with the command_word variable, the first word in the command.
# The MSG0 variable is used when the command does not take any parameter.
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The MSG1 variable is used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

from item import Beamer

class Actions:
    @staticmethod
    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified by the parameter.
        The parameter must be a cardinal direction (N, E, S, O).

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:
        
        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> go(game, ["go", "N"], 1)
        True
        >>> go(game, ["go", "N", "E"], 1)
        False
        >>> go(game, ["go"], 1)
        False

        """
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get direction from list_of_words
        direction = list_of_words[1].strip()

        # direction ignore case and full names
        dir_map = {'n': 'N', 'north': 'N', 'nord': 'N',
            'e': 'E', 'east': 'E', 'est': 'E',
            's': 'S', 'south': 'S', 'sud': 'S',
            'o': 'O', 'west': 'O', 'ouest': 'O',
            'u': 'U', 'up':'u', 
            'd': 'D', 'down':'d'}

        key = direction.lower()
        dir_normalize = dir_map.get(key)

        # If not in map, check if user provided single-letter uppercase already.
        if dir_normalize is None:
            if direction.upper() in ('N', 'E', 'S', 'O','U','D'):
                dir_normalize = direction.upper()
            else:
                print(f"\nDirection '{direction}' non reconnue.\n")
                return False

        next_room = player.current_room.exits.get(dir_normalize)
        
        if next_room and getattr(next_room, 'locked', False):
            print(f"\nLa porte vers {next_room.name} est verrouillée. Il vous faut une clé ou utiliser 'picklock'.\n")
            return False

        # Move the player using the canonical single-letter direction.
        player.move(dir_normalize)
        return True

    @staticmethod
    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> quit(game, ["quit"], 0)
        True
        >>> quit(game, ["quit", "N"], 0)
        False
        >>> quit(game, ["quit", "N", "E"], 0)
        False

        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    @staticmethod
    def help(game, list_of_words, number_of_parameters):
        """
        Print the list of available commands.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup()
        >>> help(game, ["help"], 0)
        True
        >>> help(game, ["help", "N"], 0)
        False
        >>> help(game, ["help", "N", "E"], 0)
        False

        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True
        
    @staticmethod
    def back(game, list_of_words, number_of_parameters):
        """
        Retourne à la pièce précédente visitée par le joueur.


        Si l'historique des pièces visitées est vide, affiche un message
        d'erreur et renvoie False. Sinon, met à jour la pièce actuelle
        du joueur avec la dernière pièce de l'historique et affiche sa
        description complète.
        """
        if len(list_of_words) != number_of_parameters + 1:
            print("\nCommande incorrecte.\n")
            return False

        # verifie si un historique des pièces visitées existe
        player = game.player
        if not player.history:
            print("\nAucune pièce précédente dans l'historique !\n")
            return False

        # Récupère la dernière pièce visitée depuis l'historique.
        previous_room = player.history.pop()
        
        # Met à jour la pièce actuelle du joueur.
        player.current_room = previous_room
        print(player.current_room.get_long_description())

        return True

    @staticmethod
    def check(game, list_of_words, number_of_parameters):
        """
        Display the player's inventory.

        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        """

        l = len(list_of_words)

        # Vérification du nombre de paramètres
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Affichage de l'inventaire
        player = game.player
        print(player.get_inventory())
        return True

    @staticmethod
    def look(game, list_of_words, number_of_parameters):

        l = len(list_of_words)

        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        room = game.player.current_room
        print(room.look())
        return True

    @staticmethod
    def take(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de prendre un item de la pièce et de le mettre dans son inventaire.
        """

        l = len(list_of_words)

        # accepter au moins le nombre requis de paramètres 
        if l < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Récupérer le nom de l'objet à prendre 
        item_name = " ".join(list_of_words[1:]).strip()

        room = game.player.current_room
        player = game.player

        # Vérifier si l'objet est dans la pièce
        if item_name not in room.inventory:
            print(f"\nIl n'y a pas d'objet '{item_name}' ici.\n")
            return False

        # Ajouter l'objet au joueur
        player.inventory[item_name] = room.inventory[item_name]

        # Retirer l'objet de la pièce
        del room.inventory[item_name]

        print(f"\nVous avez pris '{item_name}'.\n")
        player.quest_manager.check_action_objectives("prendre", item_name)
        return True

    @staticmethod
    def drop(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de déposer un item dans la pièce où il se trouve.
        """

        l = len(list_of_words)

        # accepter au moins le nombre requis de paramètres 
        if l < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Récupérer le nom de l'objet à déposer 
        item_name = " ".join(list_of_words[1:]).strip()

        player = game.player
        room = player.current_room

        # Vérifier si l'objet est dans l'inventaire du joueur
        if item_name not in player.inventory:
            print(f"\nVous n'avez pas '{item_name}' dans votre inventaire.\n")
            return False

        # Déposer l'objet dans la pièce
        room.inventory[item_name] = player.inventory[item_name]

        # Retirer l'objet de l'inventaire du joueur
        del player.inventory[item_name]

        print(f"\nVous avez déposé '{item_name}' dans la pièce.\n")
        return True

    @staticmethod
    def use(game, list_of_words, number_of_parameters):
        l = len(list_of_words)

        # Vérifie si le joueur a précisé un objet
        if l < number_of_parameters + 1:
            print(MSG1.format(command_word=list_of_words[0]))
            return False

        # Récupére le nom de l'objet
        item_name = " ".join(list_of_words[1:]).strip()
        player = game.player

        # Vérifie si l'objet est dans l'inventaire
        if item_name not in player.inventory:
            print(f"\nVous n'avez pas de '{item_name}' sur vous.\n")
            return False

        # Gérer l'utilisation de l'objet
        if item_name == "Potion de sang de chevreuil":
            # On regagne 60 points d'endurance
            gain = 100
            player.stamina = min(100, player.stamina + gain)
            
            # Retirer l'objet après usage 
            del player.inventory[item_name]
            
            print(f"\nVous buvez la {item_name}. Vous vous sentez beaucoup mieux !")
            print(f"Endurance actuelle : {round(player.stamina, 1)}%\n")
            return True
        
        elif item_name == "beamer":
            item = player.inventory[item_name]
            if isinstance(item, Beamer):
                resultat = item.use(player)
                print(resultat)
                return True
            else:
                print("\nCet objet ressemble à un beamer mais ne fonctionne pas.\n")
                return False

        # Si l'objet n'est pas utilisable
        else:
            print(f"\nL'objet '{item_name}' ne peut pas être utilisé de cette façon.\n")
            return False

    @staticmethod
    def charge(game, list_of_words, number_of_parameters):
        # ... (vérification standard des paramètres) ...
        item_name = list_of_words[1].lower()
        player = game.player

        # On cherche l'objet 'beamer' dans l'inventaire
        item = player.inventory.get("beamer") # On suppose que la clé est 'beamer'
        
        if isinstance(item, Beamer):
            print(item.charge(player.current_room))
            return True
        else:
            print("\nVous n'avez aucun objet pouvant être chargé.\n")
            return False

    @staticmethod
    def talk(game, list_of_words, number_of_parameters):
        if len(list_of_words) < 2:
            print("\nÀ qui voulez-vous parler ?\n")
            return False

        pnj_name = list_of_words[1]
        room = game.player.current_room

        # On cherche le PNJ dans la pièce actuelle
        target = None
        for name in room.characters:
            if name.lower() == pnj_name.lower():
                target = room.characters[name]
                break

        if target:
            print(f"\n{target.name} vous dit : '{target.get_msg(game.player)}'\n")
            return True
        else:
            print(f"\nIl n'y a personne nommé '{pnj_name}' ici.\n")
            return False
        


    @staticmethod
    def rest(game, list_of_words, number_of_parameters):
        player = game.player
        recovery = 5
        
        if player.stamina >= 100:
            print("\nVous êtes déjà en pleine forme ! Pas besoin de vous reposer.\n")
            return False 
        
        player.stamina += recovery
        if player.stamina > 100:
            player.stamina = 100
            
        print(f"\nVous vous reposez un instant... Votre endurance est maintenant à {player.stamina}%.\n")
        return True

    @staticmethod
    def quests(game, list_of_words, number_of_parameters):
        """
        Show all quests and their status.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quests(game, ["quests"], 0)
        <BLANKLINE>
        📋 Liste des quêtes:
          ❓ Grand Explorateur (Non activée)
          ❓ Grand Voyageur (Non activée)
          ❓ Découvreur de Secrets (Non activée)
        <BLANKLINE>
        True
        >>> Actions.quests(game, ["quests", "param"], 0)
        <BLANKLINE>
        La commande 'quests' ne prend pas de paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all quests
        game.player.quest_manager.show_quests()
        return True


    @staticmethod
    def quest(game, list_of_words, number_of_parameters):
        """
        Show details about a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.quest(game, ["quest", "Grand", "Voyageur"], 1)
        <BLANKLINE>
        📋 Quête: Grand Voyageur
        📖 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        Objectifs:
          ⬜ Se déplacer 10 fois (Progression: 0/10)
        <BLANKLINE>
        🎁 Récompense: Bottes de voyageur
        <BLANKLINE>
        True
        >>> Actions.quest(game, ["quest"], 1)
        <BLANKLINE>
        La commande 'quest' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Prepare current counter values to show progress
        current_counts = {
            "Se déplacer": game.player.move_count
        }

        # Show quest details
        game.player.quest_manager.show_quest_details(quest_title, current_counts)
        return True


    @staticmethod
    def activate(game, list_of_words, number_of_parameters):
        """
        Activate a specific quest.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.activate(game, ["activate", "Grand", "Voyageur"], 1) # doctest: +ELLIPSIS
        <BLANKLINE>
        🗡️  Nouvelle quête activée: Grand Voyageur
        📝 Déplacez-vous 10 fois entre les lieux.
        <BLANKLINE>
        True
        >>> Actions.activate(game, ["activate"], 1)
        <BLANKLINE>
        La commande 'activate' prend 1 seul paramètre.
        <BLANKLINE>
        False

        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n < number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the quest title from the list of words (join all words after command)
        quest_title = " ".join(list_of_words[1:])

        # Try to activate the quest
        if game.player.quest_manager.activate_quest(quest_title):
            return True

        msg1 = f"\nImpossible d'activer la quête '{quest_title}'. "
        msg2 = "Vérifiez le nom ou si elle n'est pas déjà active.\n"
        print(msg1 + msg2)
        # print(f"\nImpossible d'activer la quête '{quest_title}'. \
        #             Vérifiez le nom ou si elle n'est pas déjà active.\n")
        return False


    @staticmethod
    def rewards(game, list_of_words, number_of_parameters):
        """
        Display all rewards earned by the player.
        
        Args:
            game (Game): The game object.
            list_of_words (list): The list of words in the command.
            number_of_parameters (int): The number of parameters expected by the command.

        Returns:
            bool: True if the command was executed successfully, False otherwise.

        Examples:

        >>> from game import Game
        >>> game = Game()
        >>> game.setup("TestPlayer")
        >>> Actions.rewards(game, ["rewards"], 0)
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        True
        >>> Actions.rewards(game, ["rewards", "param"], 0)
        <BLANKLINE>
        La commande 'rewards' ne prend pas de paramètre.
        <BLANKLINE>
        False
        """
        # If the number of parameters is incorrect, print an error message and return False.
        n = len(list_of_words)
        if n != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        # Show all rewards
        game.player.show_rewards()
        return True

    @staticmethod
    def picklock(game, list_of_words, number_of_parameters):
        target = list_of_words[1] # "porte" ou "coffre"
        player = game.player
        room = player.current_room
        
        # Simulation d'un mini-jeu de crochetage
        difficulty = 5 # Exemple pour Beikovetz
        if player.lockpicking_level >= difficulty:
            print(f"Succès ! Vous avez ouvert le {target}.")
            # Déverrouiller la pièce ou le coffre
            return True
        else:
            print("Votre niveau est trop faible. Vous cassez un crochet.")
            return False

    @staticmethod
    def steal(game, list_of_words, number_of_parameters):
        player = game.player
        if len(list_of_words) < 2:
            print("\nQui voulez-vous détrousser ?\n")
            return False

        target_name = list_of_words[1].lower()
        room = player.current_room
        
        target = room.characters.get(target_name) 
        if not target:
            print(f"\nIl n'y a pas de '{target_name}' ici.\n")
            return False

        if player.stamina < 10:
            print("\nVous êtes trop fatigué pour tenter un vol.\n")
            return False
        
        player.stamina -= 10
        
        # Calcul de réussite (Agilité vs Difficulté du PNJ)
        import random
        success_chance = player.agility * 10 # 5 d'agilité = 50% de chance
        
        if random.randint(1, 100) <= success_chance:
            loot = 20 
            player.groschens += loot
            print(f"\n[SUCCÈS] Vous subtilisez discrètement {loot} groschens à {target.name} !")
            print(f"Endurance restante : {player.stamina}%\n")
            return True
        else:
            print(f"\n[ÉCHEC] {target.name} vous a repéré ! 'Au voleur !'\n")
            return False