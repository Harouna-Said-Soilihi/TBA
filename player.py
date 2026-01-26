from quest import QuestManager
# Define the Player class.
class Player():
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
    Aucune : la méthode utilise `dict.get()` pour tester l'existence de la sortie
    et renvoie False si elle est absente (aucun KeyError levé).

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
    False
    """
    # Define the constructor.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.quest_manager = QuestManager()
        self.rewards = []  # List to store earned rewards

        # historique des pièces visitées
        self.history = []
        self.inventory = {}
        self.max_weight = 20.0 
        self.stamina = 100.0
        self.groschens = 15  # système monétaire
        # Caractéristiques du joueur
        self.lockpicking_level = 1
        self.agility = 3
        self.has_lockpick = True
        
    
    # Define the move method.
    def move(self, direction):
        # Get the next room from the exits dictionary of the current room.
        # Use get() to avoid KeyError for non-canonical keys.
        next_room = self.current_room.exits.get(direction)

        # If the next room is None, print an error message and return False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False

        #Logique de fatigue en fonction du poids transporté
        weight = self.get_current_weight()
        cost = 10 + (weight * 2)
        
        if self.stamina < cost:
            print(f"\n[FATIGUE] Vous êtes trop épuisé pour vous déplacer vers {direction}.")
            print(f"Endurance actuelle : {round(self.stamina, 1)} | Coût requis : {round(cost, 1)}")
            print("Essayez de 'drop' (déposer) des objets ou de vous reposer.\n")
            return False

        self.stamina -= cost

        # sauvegarde la pièce actuelle dans l'historique avant de se déplacer
        self.history.append(self.current_room)
        
        # Set the current room to the next room.
        self.current_room = next_room
        print(f"\n(Endurance restante : {round(self.stamina, 1)}%)")
        print(self.current_room.get_long_description())
        return True
    
    def add_item(self, name, description, weight):
        self.inventory[name] = {"description": description,"weight": weight}

    def get_inventory(self):
        if not self.inventory:
            return f"Votre inventaire vide | Charge : 0/{self.max_weight} kg | Endurance : {self.stamina}%"

        result = f"Vous disposez des items suivant (Charge : {self.get_current_weight()}/{self.max_weight} kg | Endurance : {self.stamina}%)\n"

        for name, infos in self.inventory.items():
            result += f"    - {name} : {infos['description']} ({infos['weight']} kg)\n"

        return result
    
    def get_current_weight(self):
        total = 0.0
        for item in self.inventory.values():
            # Si c'est un objet 
            if hasattr(item, 'weight'):
                total += item.weight
            elif isinstance(item, dict):
                total += item.get('weight', 0)
        return round(total, 2)

    
    def add_reward(self, reward):
        """
        Add a reward to the player's rewards list.
        
        Args:
            reward (str): The reward to add.
            
        Examples:
        
        >>> player = Player("Bob")
        >>> player.add_reward("Épée magique") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Épée magique
        <BLANKLINE>
        >>> "Épée magique" in player.rewards
        True
        >>> player.add_reward("Épée magique") # Adding same reward again
        >>> len(player.rewards)
        1
        """
        if reward and reward not in self.rewards:
            self.rewards.append(reward)
            print(f"\n🎁 Vous avez obtenu: {reward}\n")


    def show_rewards(self):
        """
        Display all rewards earned by the player.
        
        Examples:
        
        >>> player = Player("Charlie")
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Aucune récompense obtenue pour le moment.
        <BLANKLINE>
        >>> player.add_reward("Bouclier d'or") # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vous avez obtenu: Bouclier d'or
        <BLANKLINE>
        >>> player.show_rewards() # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        🎁 Vos récompenses:
        • Bouclier d'or
        <BLANKLINE>
        """
        if not self.rewards:
            print("\n🎁 Aucune récompense obtenue pour le moment.\n")
        else:
            print("\n🎁 Vos récompenses:")
            for reward in self.rewards:
                print(f"  • {reward}")
            print()

    


    

