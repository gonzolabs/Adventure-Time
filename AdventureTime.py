import os
import sys
import time
import random

# Game function
def game():

    class Player():

        def __init__(self, name, location):
            # initialize the character at start of game
            self.name = name
            self.level = 1
            self.inventory = []
            self.allies = []
            self.location = location

        def fight(self, enemy):

            # tell the player what he's up against
            print "The %s has strength %s." %(enemy.name, enemy.level)
            if len(enemy.inventory) > 0:
                print "It is carrying:"
                for item in enemy.inventory:
                    print item.name, "(+%s)" %(item.bonus)
            else:
                print "It is carrying nothing."
            print "You are level %s with a bonus of %s, %s." %(self.level, sum([i.bonus for i in self.inventory]) , self.name)
            
            # decide whether to fight or flee
            choice = raw_input("Do you fight? (Y/N)")

            if choice.upper() == "Y":
                # Fight!
                say("It's on...!")
                time.sleep(0.5)
                if enemy.level + sum([i.bonus for i in enemy.inventory]) < self.level + sum([i.bonus for i in self.inventory]):
                    # you are powerful enough to kill it!
                    say("You killed the %s!" %(enemy.name))
                    self.level += 1
                    for item in enemy.inventory:
                        self.location.items.append(item)
                        print "You found a %s" %(item.name)
                    print "You are now level %s!" %(self.level)
                    self.location.enemies.remove(enemy)
                    return
                else:
                    # Run!
                    time.sleep(1)
                    print "Oh wait. You don't stand a chance, %s!" %(self.name)
                    print "The %s is more powerful than you!" %(enemy.name)
                    print "Time to run away!" 
            player.flee(enemy)
        
        def flee(self, enemy):
            # run away...
            say("Time to bravely run away!")
            raw_input("Hit return to roll the die")
            for i in range(3):
                time.sleep(0.5)
                print "."
            roll = random.randint(1,6)
            say("Roll was %s" %(roll))
            if roll > 4: 
                # success!
                say("Success!")
                say("You can run in these directions: %s" %(self.location.exits.keys()))
                direction = raw_input("Where would you like to run?")
                while direction.upper() not in self.location.exits:
                    say("You can't run that way!")
                    direction = raw_input("Where would you like to run?")
                destination_name = self.location.exits[direction.upper()]
                destination = gamemap.locations[destination_name]
                move(destination)
                return
            else:
                # bad stuff
                if len(self.inventory) == 0:
                    print "You had nothing to lose."
                    return
                else:
                    lost_item = random.choice(self.inventory)
                    say("Oh dang! You just lost your %s!" %(lost_item.name))
                    self.inventory.remove(lost_item)
                    enemy.inventory.append(lost_item)
                    return

    class Enemy():
        def __init__(self,name,level):
            self.name = name
            self.level = level
            self.inventory = []

    class Item():
        def __init__(self,name, bonus):
            self.name = name
            self.bonus = bonus

    class Location():
        def __init__(self, name, exits, message):
            self.items = []
            self.enemies = []
            self.exits = exits
            self.name = name
            self.message = message



    class Gamemap():
        def __init__(self):
            # When we initialize the Gamemap at the start of the game, all this happens

            # First, let's create all the items
            self.items = [Item(name="Pooper Scooper", bonus=1),
                        Item(name = "Cane", bonus = 1),
                        Item(name = "Top Hat of Doom", bonus = 0),
                        Item(name = "Leash", bonus = 0),
                        Item(name = "Shotgun", bonus = 4),
                        Item(name = "Chainsaw", bonus = 4),
                        Item(name = "22 Rifle", bonus = 4),
                        Item(name = "Snow Shovel", bonus = 1),
                        Item(name = "Tire Iron", bonus = 1),
                        Item(name = "Hedge Trimmers", bonus = 1)]

            # Then, let's create all the enemies
            self.enemies = [Enemy(name = "Monopoly Guy", level = 1),
                            Enemy(name = "Cape Air", level = 40),
                            Enemy(name = "Wood Chuck", level = 3),
                            Enemy(name = "Flying Squirrel", level = 2), 
                            Enemy(name = "Angry Blackberry Picker", level = 2)]

            # And then let's create all the locations (with no enemies or items in them)
            self.locations = {"Front Yard":
                            Location(name = "Front yard", 
                            exits = {"W":"West Yard", "E": "East Yard","N": "House","S": "Road"},
                            message = "You see rather nice driveway with no cars."),
                            "East Yard":
                            Location(name = "East Yard",
                            exits = {"W":"Front Yard", "E": "Forrest","N": "Meadow"},
                            message = "You are in a very flat, very clear grassy yard. (Someone loves mowing grass!)"),
                            "West Yard":
                            Location(name = "West Yard",
                            exits = {"W":"Appalation Trail", "E": "Front Yard","N": "Meadow"},
                            message = "You see a barn. It's locked up."),
                            "Meadow":
                            Location(name = "Meadow",
                            exits = {"W":"West Yard", "E": "East Yard", "S": "House"},
                            message = "You are in a vast meadow edged by forest. (Someone loves mowing grass!)"),
                            "House":
                            Location(name = "House", 
                            exits = {"N": "Meadow","S": "Front Yard"},
                            message = "You are in a lovely log cabin house. No one is home."),
                            "Road":
                            Location(name = "Road",
                            exits = {"N": "Front Yard"},
                            message = "You are on a steep dirt road. No cars to be seen."),
                            "Appalation Trail":
                            Location(name = "Appalation Trail",
                            exits = {"E": "East Yard"},
                            message = "You see a trailer through the forest."),
                            "Forrest":
                            Location(name = "Forrest", 
                            exits = {"W":"East Yard"},
                            message = "You are in a deep, dark forest.")}

            # Finally, let's place the items and enemies in random locations
            for enemy in self.enemies:
                someplace = random.choice(self.locations.values())
                someplace.enemies.append(enemy)
            for item in self.items:
                someplace = random.choice(self.locations.values())
                # if there are no enemies here, put item on the ground
                if len(someplace.enemies) == 0:
                    someplace.items.append(item)
                # otherwise, put it in the inventory of one of the enemies here!
                else:
                    some_enemy = random.choice(someplace.enemies)
                    some_enemy.inventory.append(item)

    def say(stuff):
        print
        print stuff

    def move(location):
        player.location = location
        say(player.location.name)
        print player.location.message
        # are there any enemies here?
        while len(player.location.enemies) > 0:
            say("You see a %s here!" %(" and ".join([i.name for i in location.enemies])))
            attacker = random.choice(location.enemies)
            say("The %s looks ready to fight!" %(attacker.name))
            player.fight(attacker)

    def command():

        comm = raw_input("\n--> ")
        comm = comm.split(" ")

        # only 1 command word given
        if len(comm) == 1:
            comm = comm[0]
            # move to new location
            if comm.upper() in player.location.exits:
                destination_name = player.location.exits[comm.upper()]
                destination = gamemap.locations[destination_name]
                move(destination)
                return
            # check inventory
            elif comm.lower() in ("i", "inventory"):
                if len(player.inventory) == 0:
                    say("You are carrying nothing.")
                    return
                else:
                    say("You are carrying:")
                    for item in player.inventory:
                        print item.name, "(+%s)" %(item.bonus)
                    return
            # look around
            elif comm.lower() in ("l", "look"):
                say(player.location.message)
                print "Possible directions you can go: ", ", ".join([i for i in player.location.exits])
                if len(player.location.items) == 0:
                    say("There are no items on the ground.")
                    return
                else:
                    say("You see: ")
                    for i in player.location.enemies:
                        print i.name
                    for i in player.location.items:
                        print i.name, "(+%s)" %(i.bonus)
                    return
            # quit
            elif comm.lower() in ("q", "quit"):
                choice = raw_input("You can quit or start a new game: Q or N")
                if choice.lower() == "q":
                    game_over()
                if choice.lower() == "n":
                    game()

        # 2 command words were given
        elif len(comm) >= 2:
            obj = " ".join(comm[1:]).lower()
            comm = comm[0]
            if comm.lower() == "get":
                if obj in [i.name.lower() for i in player.location.items]:
                    this_item = [item for item in player.location.items if item.name.lower() == obj][0]
                    # put it in the player's inventory
                    say("You picked up the %s" %(this_item.name))
                    player.inventory.append(this_item)
                    # remove it from the location
                    player.location.items.remove(this_item)
                    return
                if obj == "all":
                    for i in player.location.items:
                        player.inventory.append(i)
                        print "You picked up the %s" %(i.name)
                    player.location.items = []
                    return
        say("You can't do that, %s." %(player.name))

    def game_over():
        say("You reached level %s..." %(player.level))
        if player.level >= 10:
            say("You have won the game, %s!" %(player.name))
        else:
            say("Sorry, %s, you needed to reach level 10 to win. :(" %(player.name))
        sys.exit()


    # INTRO SCENE

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("   Welcome to the Mysterious Woods    ")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    gamemap = Gamemap()
    time.sleep(1)
    name = raw_input("What is your name player? ")
    player = Player(name = name, location = gamemap.locations["Front Yard"])

    print

    print "%s wakes up in a mysterious place. It is dark. You should look around." %(player.name)
    print "The commands you know: look, inventory, get [item], get all, quit (or new game)."
    print

    while True:
        command()


game()
