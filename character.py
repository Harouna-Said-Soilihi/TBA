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

    def get_msg(self, player): 
        # Gestion de la quête spécifique à Germain
        if self.name == "Germain":
            quest = player.quest_manager.get_quest("La Boussole de Germain")
            
            # Si la quête n'est pas encore activée
            if quest and not quest.is_active and not quest.is_completed:
                quest.is_active = True 
                return "Ach ! Justement, j'ai perdu ma boussole en argent dans le marécage au Sud... Pouvez-vous m'aider ?"
            
            # Si la quête est en cours
            if quest and quest.is_active:
                if "Boussole en argent" in player.inventory:
                    return "Incroyable ! Vous avez retrouvé ma boussole !"
                return "Avez-vous trouvé ma boussole ? Elle doit être au Sud, dans le marécage."

        # Si ce n'est pas Germain ou pas de quête, on cycle les messages de base
        if not self.msgs:
            self.msgs = list(self.original_msgs)
        
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

    # Exemple de ce que devrait faire Germain quand on lui parle
    def talk_to_germain(player):
        qm = player.quest_manager
        quest = qm.get_quest_by_title("La Boussole de Germain")

        if not quest: # La quête n'existe même pas encore
            return "Bonjour ! Je ne vous connais pas."

        if not quest.is_active:
            quest.activate()
            return "On m'a volé ma boussole ! Aidez-moi !"

        if "Boussole en argent" in player.inventory:
            qm.complete_objective("Rapporter la boussole")
            return "Merci ! Voici votre récompense."
            
        return "Avez-vous trouvé ma boussole ?"