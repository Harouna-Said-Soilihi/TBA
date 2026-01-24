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

class Actions:

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
            'o': 'O', 'west': 'O', 'ouest': 'O'}

        key = direction.lower()
        dir_normalize = dir_map.get(key)

        # If not in map, check if user provided single-letter uppercase already.
        if dir_normalize is None:
            if direction.upper() in ('N', 'E', 'S', 'O'):
                dir_normalize = direction.upper()
            else:
                print(f"\nDirection '{direction}' inconnue. Utilisez N/E/S/O (ou nord/est/sud/ouest).\n")
                return False

        # Move the player using the canonical single-letter direction.
        player.move(dir_normalize)
        return True

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

    def look(game, list_of_words, number_of_parameters):

        l = len(list_of_words)

        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False

        room = game.player.current_room
        print(room.look())
        return True

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
        return True

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