# Adventure-Time
Adventure Time
import os
import time
import random

# Game function
def game():

    class Player():
        def __init__(self,name,location):
            self.name = name
            self.bonus = 0
            self.level = 1
            self.inventory = []
            self.allies = []
            self.location = location

        def combat(self, enemy):
            for item in self.inventory:
                self.bonus += item.bonus
            print "The %s has strength %s." %(enemy.name, enemy.level)
            print "You are level %s with a bonus of %s, %s." %(self.level, self.bonus, self.name)
            fight = raw_input("Do you fight? (Y/N)")
            if fight.upper() == "Y":
                # it's on!
                print "It's on!"
                if enemy.level > (self.level + self.bonus):
                    # bad stuff!
                    print "You don't have a chance, %s!" %(self.name)
                    print "The %s is more powerful than you!" %(enemy.name)
                    print "Time to run away!" 

                else:
                    # you are powerful enough to kill it!
                    print "You killed the %s!" %(enemy.name)
                    for i in self.location.enemies:
                        if i.name == enemy.name:
                            self.location.enemies.remove(enemy)
                    self.level += 1
                    for item in enemy.inventory:
                        self.location.items.append(item)
                        print "You found a %s" %(item.name)
                    print "You are now level %s!" %(self.level)
                    return
        
            # run away...
            raw_input("Hit return to roll the die")
            roll = random.randint(1,6)
            print "Roll was %s" %(roll)
            if roll > 4: 
                print "You ran away, Yayyy!"
                return
            else:
                if len(self.inventory) == 0:
                    print "You had nothing to lose."
                else:
                    lost_item = random.choice(self.inventory)
                    print "Oh dang! You just lost your %s!" %(lost_item.name)
                    self.inventory.remove(lost_item)
                    return

    class Enemy():
        def __init__(self,name,level, inventory):
            self.name = name
            self.level = level
            self.inventory = inventory

    class Item():
        def __init__(self,name, bonus):
            self.name = name
            self.bonus = bonus

    class Location():
        def __init__(self, name, items, enemies, exits, message):
            self.items = items
            self.enemies = enemies
            self.exits = exits
            self.name = name
            self.message = message

    #Items
    pooper_scooper = Item(name="Pooper Scooper", bonus=1)
    cane = Item(name = "Cane", bonus = 1)
    top_hat = Item(name = "Top Hat of Doom", bonus = 0)
    leash = Item(name = "Leash", bonus = 0)
    shotgun = Item(name = "Shotgun", bonus = 4)
    chainsaw = Item(name = "Chainsaw", bonus = 4)
    rifle = Item(name = "22 Rifle", bonus = 4)
    shovel = Item(name = "Snow Shovel", bonus = 1)
    tire_iron = Item(name = "Tire Iron", bonus = 1)
    hedge_trimmers = Item(name = "Hedge Trimmers", bonus = 1)

    #Enemies
    Monopoly_Guy = Enemy(name = "Monopoly Guy", level = 1, inventory = [cane, top_hat])
    Cape_Air = Enemy(name = "Cape Air", level = 40, inventory = [])
    Wood_Chuck = Enemy(name = "Wood Chuck", level = 3, inventory = [])
    Flying_Squirrel = Enemy(name = "Flying Squirrel", level = 2, inventory = [])
    Angry_BlackBerry_Picker = Enemy(name = "Angry Blackberry Picker", level = 2, inventory = [hedge_trimmers])

    class Gamemap():
        def __init__(self):
            self.locations = {
            "Front Yard": Location(name = "Front yard", items = [pooper_scooper], 
            enemies = [], 
            exits = {"W":"West Yard", "E": "East Yard","N": "House","S": "Road"},
            message = "You see rather nice driveway with no cars."),
            #East Yard
            "East Yard": Location(name = "East Yard", items = [rifle], 
            enemies = [Wood_Chuck], 
            exits = {"W":"Front Yard", "E": "Forrest","N": "Meadow"},
            message = "You are in a very flat, very clear grassy yard. (Someone loves mowing grass!)"),
            #West Yard
            "West Yard": Location(name = "West Yard", items = [shovel], 
            enemies = [], 
            exits = {"W":"Appalation Trail", "E": "Front Yard","N": "Meadow"},
            message = "You see a barn. It's locked up."),
            #Meadow
            "Meadow": Location(name = "Meadow", items = [], 
            enemies = [Angry_BlackBerry_Picker], 
            exits = {"W":"West Yard", "E": "East Yard", "S": "House"},
            message = "You are in a vast meadow edged by forest. (Someone loves mowing grass!)"),
            #House
            "House": Location(name = "House", items = [shotgun, chainsaw], 
            enemies = [], 
            exits = {"N": "Meadow","S": "Front Yard"},
            message = "You are in a lovely log cabin house. No one is home."),
            #Road
            "Road": Location(name = "Road", items = [tire_iron], 
            enemies = [Monopoly_Guy], 
            exits = {"N": "Front Yard"},
            message = "You are on a steep dirt road. No cars to be seen."),
            #Appalation Trail
            "Appalation Trail": Location(name = "Appalation Trail", items = [], 
            enemies = [], 
            exits = {"E": "East Yard"},
            message = "You see a trailer through the forest."),
            #Forrest
            "Forrest": Location(name = "Forrest", items = [], 
            enemies = [], 
            exits = {"W":"East Yard"},
            message = "You are in a deep, dark forest.")
            }

    def say(stuff):
        print
        print stuff

    def command():
        comm = raw_input("--> ")
        comm = comm.split(" ")
        # only 1 command word given
        if len(comm) == 1:
            comm = comm[0]
            # move to new location
            if comm.upper() in player.location.exits:
                destination_name = player.location.exits[comm.upper()]
                destination = gamemap.locations[destination_name]
                player.location = destination
                print player.location.name
                say(player.location.message)
                if len(player.location.enemies) > 0:
                    say("You see a %s here!" %(" and ".join([i.name for i in player.location.enemies])))
                    for enemy in player.location.enemies:
                        player.combat(enemy)
                return
            # check inventory
            elif comm.lower() in ("i", "inventory"):
                if len(player.inventory) == 0:
                    say("You are carrying nothing.")
                    return
                else:
                    print "\n".join([i.name for i in player.inventory]), "\n"
                    return
            # look around
            elif comm.lower() in ("l", "look"):
                say(player.location.message)
                print "Possible directions you can go: ", ", ".join([i for i in player.location.exits])
                if len(player.location.items) == 0:
                    say("There are no items on the ground.")
                else:
                    say("You see: " + "\n".join([i.name for i in player.location.items]))
                return
        # 2 command words were given
        elif len(comm) >= 2:
            object = " ".join(comm[1:]).lower()
            comm = comm[0]
            if comm.lower() == "get":
                if object in [i.name.lower() for i in player.location.items]:
                    this_item = [item for item in player.location.items if item.name.lower() == object][0]
                    # put it in the player's inventory
                    say("You picked up the %s" %(this_item.name))
                    player.inventory.append(this_item)
                    # remove it from the location
                    player.location.items.remove(this_item)
                    return
        say("You can't do that, %s." %(player.name))


    # INTRO SCENE

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("   Welcome to the Mysterious Woods    ")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    gamemap = Gamemap()
    time.sleep(1)
    name = raw_input("What is your name player? ")
    player = Player(name = name, location = gamemap.locations["Front Yard"])

    print

    print "%s wakes up in a mysterious place. It is dark and you can only make out a pooper scooper." %(player.name)
    print "The commands you know: look, inventory, get [item]."
    print

    while True:
        command()


game()
