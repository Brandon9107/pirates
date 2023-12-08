from game import location 
#There is some pretence that the game might not be played over the terminal so we use a custom function announce to print things instead of print.
from game.display import announce
import game.config as config
from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as Item
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu
from game.player import Player




#demo island inherits from location(demo island is a location)
class ChaosIsland(location.Location):
    def __init__(self,x,y,world):
        super().__init__(x,y,world)
        #object orientated handling, super() erfers to the parent class in this case
        #(Location in this case)
        #so this runs the initializer of Location
        self.name="island"
        self.symbol='C' #symbol for map
        self.visitable=True #marks the island as a place the pirates can go to.
        self.locations={}#Dictionary of sub-locations on the island.
        self.locations["DockedAtBeach"]= DockedAtBeach(self)
        self.locations["trees"]= Trees(self)
        self.locations["valley"]= Valley(self)
        self.locations["crash_site"]=CrashSite(self)
        self.locations["SmokeyArea"]=SmokeyArea(self)
        self.locations["asteroids"]=Asteroid(self)
        self.locations["tower"]=Tower(self)
        self.locations["CrashedShip"]=CrashedShip(self)
        self.locations["InsideTower"]=InsideTower(self)
        #where do the pirates start?
        self.starting_location=DockedAtBeach(self)
    def enter(self, ship):
        #what to do when the ship visits this location on the map
        announce("Your ship has docked at an island. As a musty breeze looms through the air, a sight of smoke can be seen in the distance. Maybe this island is worth an adventure?")
    #Boilerplate code for starting a visit
    def visit(self):
        config.the_player.location=self.starting_location
        config.the_player.location.enter()
        super().visit()
#sub-locations(beach and trees)
class DockedAtBeach(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "beach"
        #the verbs dict was set up by the super() init
    def __init__ (self, m):
        super().__init__(m)
        self.name = "eastBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        # All the beaches on the island have a 25% chance for a seagull encounter.
        self.event_chance = 10
        self.events.append(seagull.Seagull())

    def enter (self):
        announce ("an eery feeling overwhelms you as your feet touches the sand.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["valley"]
        ##elif (verb == "north" or verb == "south"):
            ##config.the_player.next_loc = self.main_location.locations[f"{verb}DockedAtBeach"]

class Valley(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "valley"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
    def enter (self):
        description = "After walking for a bit, you arrive at a mountainous valley, with trees surrounding you."
        announce(description)
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["trees"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["DockedAtBeach"]






class Trees(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "trees"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
    def enter (self):
        description = "After going into the trees, you come upon a small cliff, with 3 paths opening infront of you."
        announce(description)
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["asteroids"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["tower"]
        elif (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["crash_site"]

class CrashSite(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "crash_site"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['explore']=self
    def enter (self):
        #explores and gets a new gun, a key for tower, emerald crown, fights some pirates
        description = "Arriving at a smokey surrounding, you see an unknown object like structure in disarray, some parts are non recognizeable, almost like its from another place. This area looks explorable."
        announce(description)
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["trees"]
        if (verb == "explore"):
            config.the_player.go = True
            config.the_player.next_loc = self.main_location.locations["CrashedShip"]

class CrashedShip (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "CrashedShip"
        self.verbs['exit'] = self
        self.verbs['leave'] = self

        self.event_chance = 100
        self.events.append(Ambush1())
        
    

    def enter (self):
        description = "The area is covered in smoke, a musty scent looms the air and you hear voices in the distant."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "exit" or verb == "leave"):
            config.the_player.next_loc = self.main_location.locations["crash_site"]
            config.the_player.go = True

class Ambush1 (event.Event):

    def __init__ (self):
      self.name = "trio pirate attack"  

    def process (self, world):
        result = {}
        ##rogues = combat.Rogue_Pirate(Monster)
        announce("You are ambushed by a trio of rogue pirates!")
        monsters=[]
        for i in range(0,3):
            monsters.append(combat.Rogue_Pirate(Monster))
            
        combat.Combat(monsters).combat()
        announce("The pirates regret their decision as their souls drift away.")
        # Set newevents to an empty list. If I added 'self' to the list, the event would be readded upon completing, effectively making the spider respawn every turn you are in here.
        result["newevents"] = []
        # Set the result message to an empty string, as we are printing our own strings at the right time.
        result["message"] = ""

        announce("In the crash site you find a blunderbass gun, a key, and an emerald crown .")
        config.the_player.add_to_inventory([Item.Blunderbass()])
        config.the_player.add_to_inventory([Item.Tower_Key()])
        config.the_player.add_to_inventory([Item.Emerald_Crown()])
        
        return result
    
class Ambush2 (event.Event):

    def __init__ (self):
      self.name = "trio pirate attack"  

    def process (self, world):
        result = {}
        ##rogues = combat.Rogue_Pirate(Monster)
        announce("You are ambushed by a trio of rogue pirates!")
        monsters=[]
        for i in range(0,3):
            monsters.append(combat.Rogue_Pirate(Monster))
            
        combat.Combat(monsters).combat()
        
        
        announce("The pirates regret their decision as their souls drift away.")
        # Set newevents to an empty list. If I added 'self' to the list, the event would be readded upon completing, effectively making the spider respawn every turn you are in here.
        result["newevents"] = []
        # Set the result message to an empty string, as we are printing our own strings at the right time.
        result["message"] = ""

        announce("In the smokey area you find a blunderbass gun, a key, and an gold pendant .")
        config.the_player.add_to_inventory([Item.Blunderbass()])
        config.the_player.add_to_inventory([Item.Tower_Key()])
        config.the_player.add_to_inventory([Item.Gold_Pendant()])
        
        return result
    
class Ambush3 (event.Event):

    def __init__ (self):
      self.name = "boss battle"  

    def process (self, world):
        result = {}
        announce("You are attacked by a menacing stone golem and his spawnlings, possibly the guardian of the island!")
        monsters=[]
        for i in range(0,5):
            monsters.append(combat.Golemites(Monster))
        monsters.append(combat.Stone_Golem(Monster))
        combat.Combat(monsters).combat()
        ##golem = combat.Stone_Golem(Monster)
        ##golemites = combat.Golemites(Monster)
        
        ##combat.Combat([golemites]).combat()
        ##combat.Combat([golem]).combat()
        
        announce("The stone golem crumbles at your feet.")
        # Set newevents to an empty list. If I added 'self' to the list, the event would be readded upon completing, effectively making the spider respawn every turn you are in here.
        result["newevents"] = []
        # Set the result message to an empty string, as we are printing our own strings at the right time.
        result["message"] = ""

        announce("As the giant crumbles, it drops an item, an Obsidian Sword.")
        config.the_player.add_to_inventory([Item.Obsidian_Sword()])
        
        return result
    


class Asteroid(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "asteroids"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['explore']=self
    def enter (self):
        #key for tower, another gun, fights some pirates, gold pendant
        description = "Infront of you is a large rock, with a trail behind it, it looks like its from up above. This area is explorable."
        announce(description)
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["trees"]
        if (verb == "explore"):
            config.the_player.go = True
            config.the_player.next_loc = self.main_location.locations["SmokeyArea"]

class SmokeyArea (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "SmokeyArea"
        self.verbs['exit'] = self
        self.verbs['leave'] = self

        self.event_chance = 100
        self.events.append(Ambush2())

    def enter (self):
        description = "The area is covered in smoke, a musty scent looms the air and you hear voices in the distant."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "exit" or verb == "leave"):
            config.the_player.next_loc = self.main_location.locations["asteroids"]
            config.the_player.go = True

class Tower(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "tower"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['enter']=self
    def enter (self):
        #obsidian sword, 1000 gold.
        description = "As you trail through the trees a large tower makes its way into your view, seemingly overwatching the entire island. Looking at the locks, it requires two keys."
        announce(description)
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["trees"]
        if (verb == "enter"):
            if self.allowed()==True:
                config.the_player.go = True
                config.the_player.next_loc = self.main_location.locations["InsideTower"]
            else:
                announce('You do not have the necessary keys to enter, keep searching the island.')
    def allowed(self):
        counter=0
        for i in config.the_player.inventory:
            if isinstance(i, Item.Tower_Key)==True:
                counter=counter+1
        if counter>=2:
            return (True)
        else:
            return (False)
    

class InsideTower (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "InsideTower"
        self.verbs['exit'] = self
        self.verbs['leave'] = self

        self.event_chance = 100
        self.events.append(Ambush3())

    def enter (self):
        description = "As you enter the tower, a small beam of light beams in, illuminating a dormant stone golem in front of you."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "exit" or verb == "leave"):
            config.the_player.next_loc = self.main_location.locations["tower"]
            config.the_player.go = True
        


    