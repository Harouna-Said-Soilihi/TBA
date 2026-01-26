import random

class Character:
    def __init__(self, name, description, current_room, msgs):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs
        self.original_msgs = list(msgs) # Aaspect cyclique

    def __str__(self):
        return f"{self.name} : {self.description}"

    def get_msg(self):
        if not self.msgs:
            # Si la liste est vide, on la remplit à nouveau avec les messages originaux
            self.msgs = list(self.original_msgs)
        
        # On renvoie le premier message et on le retire de la liste actuelle
        return self.msgs.pop(0)

    def move(self):
        # 1 chance sur 2 de bouger
        if random.choice([True, False]):
            # Récupérer les sorties possibles (on filtre les None)
            exit_names = [direction for direction, room in self.current_room.exits.items() if room is not None]
            
            if exit_names:
                chosen_direction = random.choice(exit_names)
                next_room = self.current_room.exits[chosen_direction]
                
                # Retirer le PNJ de l'ancienne pièce et l'ajouter à la nouvelle
                self.current_room.characters.pop(self.name, None)
                self.current_room.characters[self.name] = self
                self.current_room = next_room
                return True
        return False
    
    def move(self):
        if random.choice([True, False]):
            exit_names = [dir for dir, room in self.current_room.exits.items() if room is not None]
            if exit_names:
                chosen_dir = random.choice(exit_names)
                next_room = self.current_room.exits[chosen_dir]
                
                # Utilise pop pour retirer le perso en toute sécurité
                self.current_room.characters.pop(self.name, None)
                
                # On le place dans la nouvelle pièce
                self.current_room = next_room
                self.current_room.characters[self.name] = self
                return True
        return False