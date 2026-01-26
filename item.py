class Item:
    def __init__(self, name, description, weight):
        self.name = name
        self.description = description
        self.weight = weight

    def __str__(self):
        return f"{self.name} : {self.description} ({self.weight} kg)"

class Beamer(Item):
    def __init__(self):
        super().__init__("Beamer", "Un étrange appareil technologique permettant de se téléporter.", 1.5)
        self.saved_room = None  # La pièce mémorisée

    def charge(self, room):
        self.saved_room = room
        return f"\n[Beamer] : Pièce '{room.name}' mémorisée.\n"

    def use(self, player):
        if not self.saved_room:
            return "\n[Beamer] : Erreur, l'appareil n'est pas chargé.\n"
        
        # Téléportation
        player.history.append(player.current_room) # On garde une trace pour la commande 'back'
        player.current_room = self.saved_room
        self.saved_room = None # Se décharge après usage
        return f"\n[Beamer] : Énergie libérée ! Vous êtes téléporté...\n{player.current_room.get_long_description()}"