from js import browser_print, browser_input

async def input(prompt=""):
    return await browser_input(prompt)

def print(*args, **kwargs):
    browser_print(" ".join(str(a) for a in args))

import random as r
import math as m
x = 0
y = 0
hp = 100
maxhp = 100
mp = 100
maxmp = 100
true = False
level = [10, 1, 1, 1, 1, 1, 10]
exp = [908, 0, 0, 0, 0, 0, 908]
skill = ["hitpoints", "attack", "defence", "fishing", "gathering", "mining", "magic"]
skillsunlocked = 6
inventory = ["" ,"", "", "", "", ""]
upgrades = []
gold = 0
fishguildmembership = False
immovable = 0
stance = 1
task = "none"
currenttask = "none"
taskamount = 0
tasksdone = []
bonusatt = 0
bonusdef = 0
spec = 1
fight = [(-1, -1), (-1, 1), (0, -1), (2, 1), (2, 0), (6, 6)]
edible = ["bread", "carp", "trout", "pike", "cake", "slice of cake", "beef", "anchovies", "purpleberry pie", "piece of purpleberry pie"]
locations = {(-1, -1): "goblin outpost", (-1, 0): "wheat field", (-1, 1): "spider cave", (0, -1): "william lake", (0, 0): "hospy", (0, 1): "hospy library", (1, -1): "fishing guild", (1, -2): "sea", (1, 0): "hospy market", (1, 1): "purple goblin inn", (2, 0): "hospy farm", (2, 1): "w.h. seaport", (-2, 1): "sea", (-2, 0): "sea", (-2, -1): "sea", (-1, 2): "sea", (-1, -2): "sea", (0, 2): "sea", (0, -2): "sea", (1, 2): "sea", (2, -2): "sea", (2, 2): "sea", (3, 1): "sea", (3, 0): "sea",  (2, -1): "sea", (6, 6): "loogustia harbor", (6, 7): "northloog beach", (6, 8): "open field", (5, 8): "sea", (6, 9): "wall",  (7, 5): "wall", (7, 7): "loogustia dairy farm", (8, 7): "wall", (7, 8): "wall", (8, 6): "wall", (6, 5): "sea", (7, 6): "adventurer's campsite", (5, 6): "sea"}
quest = ["start", "start"]
undropable = ["summoning rune", "charged summoning rune"]
titles = ["noble adventurer"]

def drops(drop, chance):
	rand = r.randint(1, chance)
	if rand == chance:
		additem(drop)
		if true == True:
			print(f"you got {drop}")
		else:
			print(f"you got {drop}, but had no free inventory spots to put it so you lost it")

def xp(level):
	need = 70
	for x in range(level-2):
		need += m.floor(x + (70 * (2 ** (x / 7))))
	return need

async def death(name, expen, golden, types, drop, chance):
	global gold, stance, exp, inventory, task, currenttask, taskamount
	print(f"you have killed the {name} gaining {expen} exp and {golden} gold")
	gold += golden
	if stance == 1:
		stancerand = r.randint(1,2)
		if stancerand == 1:
			exp[0] += m.floor(expen/2)
			exp[1] += m.ceil(expen/2)
		else:
			exp[0] += m.ceil(expen/2)
			exp[1] += m.floor(expen/2)
	elif stance == 2:
		stancerand = r.randint(1,2)
		if stancerand == 1:
			exp[0] += m.floor(expen/2)
			exp[2] += m.ceil(expen/2)
		else:
			exp[0] += m.ceil(expen/2)
			exp[2] += m.floor(expen/2)
	else:
		exp[0] += m.floor(expen/3)
		exp[1] += m.floor(expen/3)
		exp[2] += m.floor(expen/3)
	if types == currenttask:
		if taskamount == 0:
			print("you have already finished the task")
		elif taskamount == 1:
			taskamount = 0
			print(f"you have finished your {task} task. go back to your task master to reap the rewards")
		else:
			taskamount -= 1
			print(f"you have contributed to your task, only {taskamount} to go")
	if chance != 0:
		drops(drop, chance)
	return

def additem(item):
	global true, inventory
	true = False
	for i in range(6):
		if inventory[i] == "":
			inventory[i] = item
			true = True
			return

def switchitem(item1, item2):
	global true, inventory
	true = False
	for i in range(6):
		if inventory[i] == item1:
			inventory[i] = item2
			true = True
			return

def sellitem(item):
    global true, inventory
    true = False
    for i in range(len(inventory)):
        if inventory[i] == item:
            inventory[i] = ""
            true = True
            print(f"you have sold {item}")
            return
    print(f"you do not have {item}")

def removeitem(item):
    global inventory
    for i in range(len(inventory)):
        if inventory[i] == item:
            inventory[i] = ""
            return

def twotooneitem(item1, item2, item3):
	global true, inventory
	true = False
	for i in range(6):
		if inventory[i] == item1:
			true = "somewhat true"
			slot1 = i
	for j in range(6):
		if inventory[j] == item2:
			if true == "somewhat true":
				true = True
				inventory[slot1] = item3
				inventory[j] = ""
				return

def threetooneitem(item1, item2, item3, item4):
	global true, inventory
	true = False
	for i in range(6):
		if inventory[i] == item1:
			true = "somewhat true"
			slot1 = i
	for j in range(6):
		if inventory[j] == item2:
			if true == "somewhat true":
				true = "evenmoreso"
				slot2 = j
	for k in range(6):
		if inventory[k] == item3:
			if true == "evenmoreso":
				inventory[slot1] = item4
				inventory[slot2] = ""
				inventory[k] = ""
				true = True
				return

async def dropitem(item):
	global inventory
	for i in range(len(inventory)):
		if inventory[i] == item:
			print(f"are you sure you want to drop {item}? (y/n)")
			command = await input("")
			command = command.lower()
			if command == "y":
				inventory[i] = ""
				print(f"you dropped {item}")
			else:
				print("you keep the item")
			return
	print(f"you do not have {item}")

def dropallitem(item):
	global inventory
	dropped = 0
	for i in range(len(inventory)):
		if inventory[i] == item:
			inventory[i] = ""
			print(f"you dropped {item}")
			dropped += 1
	if dropped == 0:
		print(f"you do not have {item}")
	return

def eatitem(item):
	global inventory, hp, edible
	true = False
	if item in edible:
		for i in range(len(inventory)):
			if inventory[i] == item:
				if item == "bread":
					hp += 25
				elif item == "carp":
					hp += 19
				elif item == "trout":
					hp += 28
				elif item == "pike":
					hp += 37
				elif item == "cake":
					hp += 16
					print("a slice of cake remains")
					inventory[i] = "slice of cake"
					maxedhp()
					true = True
					return
				elif item == "slice of cake":
					hp += 16
				elif item == "":
					print("a piece of purpleberry pie remains")
					inventory[i] = "piece of purpleberry pie"
					true = True
					maxedhp()
					return
				elif item == "piece of purpleberry pie":
					mp += 10
				elif item == "beef":
					hp += 15
				elif item == "anchovies":
					hp += 46
				print(f"you eat the {item}")
				maxedhp()
				inventory[i] = ""
				true = True
				return
		print(f"you do not have {item}")
	else:
		print("you cannot eat this item")

def maxedhp():
	global hp, maxhp
	if hp > maxhp:
		hp = maxhp

def gather(gatherable):
	global level, exp, true
	if gatherable == "carp":
		random = r.randint(1, level[3]+10)
		if random > 8:
			additem("raw carp")
			if true == True:
				print("you catch a raw carp and gain some exp")
				exp[3] += 12
			else:
				print("there is no room for you to keep the carp and you lose out on some exp")
		else:
			print("you failed to catch the carp")
	elif gatherable == "trout":
		random = r.randint(1, level[3]+10)
		if random > 16:
			additem("raw trout")
			if true == True:
				print("you catch a raw trout and gain some exp")
				exp[3] += 28
			else:
				print("there is no room for you to keep the trout and you lose out on some exp")
		else:
			print("you failed to catch the trout")
	elif gatherable == "pike":
		random = r.randint(1, level[3]+10)
		if random > 22:
			additem("raw pike")
			if true == True:
				print("you catch a raw pike and gain some exp")
				exp[3] += 39
			else:
				print("there is no room for you to keep the pike and you lose out on some exp")
		else:
			print("you failed to catch the pike")
	elif gatherable == "anchovies":
		random = r.randint(1, level[3]+10)
		if random > 28:
			additem("raw anchovies")
			if true == True:
				print("you catch a raw anchovies and gain some exp")
				exp[3] += 45
			else:
				print("there is no room for you to keep the anchovies and you lose out on some exp")
		else:
			print("you failed to catch the anchovies")
	elif gatherable == "purpleberry":
		random = r.randint(1, level[4]+5)
		if random > 4:
			additem("purpleberry")
			if true == True:
				print("you carefully grab a purpleberry from the bush and gain some exp")
				exp[4] += 16
			else:
				print("there is no room for you to keep the purpleberry and you lose out on some exp")
		else:
			random = r.randint(1, 3)
			if random == 3:
				print("youch! you prick yourself on the bush and lose 5hp")
				hp -= 5
				if hp < 1:
					print("oh no! you've died...")
			else:
				print("you failed to grab the berry")
	elif gatherable == "wood":
		random = r.randint(1, level[4]+5)
		if random > 4:
			additem("wood")
			if true == True:
				print("you chop of a piece of wood and gain some exp")
				exp[4] += 9
			else:
				print("there is no room for you to keep the wood piece and you lose out on some exp")
		else:
			print("you failed to grab the berry")

async def battle(name, atten, defen, hpen, expen, golden, types, drop, chance, attacking):
	global hp, gold, exp, stance, task, currenttask, taskamount, bonusatt, bonusdef, mp, inventory
	while True:
		ea = False
		print("what would you like to do")
		command3 = await input("")
		if command3 == "attack":
			ea = True
			dmg = round((r.randint(1, (level[1]+bonusatt)*10) - r.randint(1, defen*3)) * (1 - defen / (defen + 10)))
			if dmg < 1:
				dmg = 1
			hpen -= dmg
			if hpen < 0:
				hpen = 0
			print(f"you dealt {dmg} damage, leaving the {name} at {hpen}")
			if hpen < 1:
				await death(name, expen, golden, types, drop, chance)
				return
		elif command3 == "special attack":
			if spec == 1:
				if mp >= 25:
					ea = True
					mp -= 25
					dmg = round((r.randint(1, (level[1]+bonusatt)*10) - r.randint(1, defen)) * (1 - defen / (defen + 10)))
					if dmg < 1:
						dmg = 1
					hpen -= dmg
					if hpen < 0:
						hpen = 0
					print(f"you dealt {dmg} damage, leaving the {name} at {hpen}")
					if hpen < 1:
						await death(name, expen, golden, types, drop, chance)
						return
				else:
					print("you do not have enough mp to use this attack")
		elif command3 == "stance":
			print("what stance will you change to?\n1. power (att and hp exp)\n2. accurate (def and hp exp)\n3. balanced (all)")
			command4 = await input("")
			if command4 == "1":
				print("you are now in power stance")
				stance = 1
			elif command4 == "2":
				print("you are now in accurate stance")
				stance = 2
			elif command4 == "3":
				print("you are now in balance stance")
				stance = 3
			else:
				print("you have not changed stance")
		elif command3 == "special check":
			if spec == 1:
				print("slash (25 mp): attack greatly reducing the effect of your enemy's defence")
		elif command3.startswith("eat "):
			eatitem(command3[4:])
			ea = true
		if ea == True and attacking != 1:
			dmgen = round((r.randint(1, atten*10) - r.randint(1, (level[2]+bonusdef)*3)) * (1 - (level[2]+bonusdef) / ((level[2]+bonusdef) + 10)))
			if dmgen < 1:
				dmgen = 1
			hp -= dmgen
			if hp < 0:
				hp = 0
			print(f"the {name} dealt {dmgen} damage, leaving you at {hp}")
		if hp == 0:
			print("oh no! you've died...")
			return
		print(f"you have {mp}mp left")

async def craft():
	print("what item would you like to make")
	command3 = await input("")
	command3 = command3.lower()
	if command3 == "candle":
		switchitem("wax", "candle")
		if true == True:
			print("you successfully made a candle")
		else:
			print("you do not have the wax to make the candle")
	elif command3 == "charged summoning rune":
		twotooneitem("summoning rune", "raw beef", "charged summoning rune")
		if true == True:
			print("you successfully charge the summoning rune. it cackles with demonic energy")
			quest[1] = "ready"
		else:
			print("you cannot charge the rune")
	elif command3 == "fishing net part":
		if inventory.count("seaweed") >= 3:
			for t in range(3):
				removeitem("seaweed")
			additem("fishing net part")
			print("you weave together the seaweed and create a fishing net part")
		else:
			print("you do not have enough seaweed")
	elif command3 == "fishing net":
		if inventory.count("fishing net part") >= 4:
			for t in range(4):
				removeitem("fishing net part")
			additem("fishing net")
			print("you expertly create a fishing net out of the seaweed parts")
		else:
			print("you do not have enough fishing net parts")
	else:
		print("that is not a name of a item you can make, to find a list of items you can make, type \"crafting\"")

async def cook():
	print("what recipe would you like to make")
	command3 = await input("")
	command3 = command3.lower()
	if command3 == "bread":
		twotooneitem("flour", "water", "bread")
		if true == True:
			print("you successfully made bread")
		else:
			print("you do not have all the ingredients to make this recipe")
	elif command3 == "carp":
		switchitem("raw carp", "carp")
		if true == True:
			print("you successfully cooked the carp")
		else:
			print("you do not have all the ingredients to make this recipe")
	elif command3 == "trout":
		if level[3] >= 10:
			twotooneitem("raw trout", "flour", "trout")
			if true == True:
				print("you successfully cooked the trout")
			else:
				print("you do not have all the ingredients to make this recipe")
		else:
			print("you do not have the required fishing level to cook this fish")
	elif command3 == "pike":
		if level[3] >= 15:
			twotooneitem("raw pike", "butter", "pike")
			if true == True:
				print("you successfully cooked the pike")
			else:
				print("you do not have all the ingredients to make this recipe")
		else:
			print("you do not have the required fishing level to cook this fish")
	elif command3 == "cake":
		threetooneitem("flour", "egg", "milk", "cake")
		if true == True:
			print("you successfully made a cake")
		else:
			print("you do not have all the ingredients to make this recipe")
	elif command3 == "beef":
		switchitem("raw beef", "beef")
		if true == True:
			print("you successfully cooked the beef")
		else:
			print("you do not have all the ingredients to make this recipe")
	elif command3 == "anchovies":
		threetooneitem("raw anchovies", "egg", "butter", "anchovies")
		if true == True:
			print("you successfully made some great looking anchovies")
		else:
			print("you do not have all the ingredients to make this recipe")
	elif command3 == "purpleberry pie":
		threetooneitem("flour", "water", "purpleberry", "purpleberry pie")
		if true == True:
			print("you successfully made a purpleberry pie")
		else:
			print("you do not have all the ingredients to make this recipe")
	else:
		print("that is not a name of a recipe, to find a list of recipes, type \"cookbook\"")

async def main():
	global x, y, hp, maxhp, mp, maxmp, true, level, exp, inventory, gold, fishguildmembership, immovable, stance, task, currenttask, taskamount, bonusatt, bonusdef, spec, quest, skillsunlocked

	print("welcome to forle, the world of adventure! type \"commands\" for a list of commands, \"examine\" to learn what is in the area you are currently in, \"attack\" to attack the monster in the area (if there is one) or \"interact x\" to interact with the xth item in the area's examine text")
	print("you are currently in hopsy")
	while True:
		command = await input("")
		command = command.lower()
		if command == "examine":
			if x == 0 and y == 0:
				print("you are in hospy, where every adventure begins. around you, you can see...\n1. a statue\n2. a combat instructor\n3. the mayor.")
			elif x == 0 and y == 1:
				print("you are in the hospy library. around you, there are...\n1. bookshelves \n2. librarian\n3. craftsman's workshop")
			elif x == -1 and y == -1:
				print("you are in the goblin outpost outside of hospy, you can see some worker goblins and...\n1. hobgoblin leader\n2. purpleberry plant\nENEMY: goblin mugger")
			elif x == -1 and y == 0:
				print("you are in a wheat field, it is very barren but you can see...\n1. wheat \n2. watermill\n3. tree")
			elif x == 1 and y == 1:
				print("you are in the purple goblin inn, there is only a...\n1. innkeep")
			elif x == 0 and y == -1:
				print("you are on william lake, there is a...\n1. carp fishing spot\n2. fireplace\n3. well\nENEMY: hobgoblin fisher")
			elif x == 1 and y == -1:
				if level[3] >= 10:
					print("you are in the fishing guild, there is...\n1. gary, guild leader\n2. trout fishing spot\n3. pike fishing spot\n4. fish exchange")
				else:
					print("you cannot use anything in the fishing guild, come back when you are a higher fishing level")
			elif x == 2 and y == 0:
				print("you are in the one and only hospy farm, you can see...\n1. dairy cow\n2. churn\n3. beehives\n4. chicken coop\nENEMY: bull")
			elif x == 1 and y == 0:
				print("you are currently in the bustling hospy market, you can see...\n1. armour stall\n2. weapon stall\n3. mable's oddities")
			elif x == -1 and y == 1:
				if "goggle" in upgrades:
					print("you are in the spider cave, you can see...\n1.massive spider mother\nENEMY: giant spider")
				else:
					print("you are in the spider cave. It is very dark and you can only see...\nENEMY: giant spider")
			elif x == 2 and y == 1:
				print("you are in the william hospy seaport, you can see...\n1. portmaster\n2. elven ambassador\nENEMY: merfolk")
			elif x == 6 and y == 6:
				print("you are in the loogustia harbour, you can see...\n1. portmaster\n2. local guide\n3. gem merchant\nENEMY: siren")
			elif x == 6 and y == 7:
				print("you are at the northloog beach, you can see...\n1. seaweed\n2. net fishing spot")
			elif x == 7 and y == 6:
				print("you are in the adventurer's campsite, you can see...\n1. campfire\n2. workbench\n3. trout fishing spot\nENEMY?: punching bag")
			elif x == 7 and y == 7:
				print("you are in the loogustia dairy farm, you can see...\n1. dairy cow\n2. churn\n3. cheese press")
			elif x == 6 and y == 8:
				print("you are an open field, you can see...\n1. wandering mage\n2. tree\nENEMY: ogre")
		elif command == "inventory":
			print("INVENTORY")
			for n in range(6):
				if inventory[n] != "":
					print(f"{n+1}. {inventory[n]}")
				else:
					print(f"{n+1}. empty")
		elif command in ("quit", "exit", "end"):
			print("are you sure? (y/n)")
			command2 = await input("")
			command2 = command2.lower()
			if command2 == "y":
				break
		elif command.startswith("drop all "):
			if command[9:] not in undropable:
				dropallitem(command[9:])
			else:
				print("you can't drop all that")
		elif command.startswith("drop "):
			if command[5:] not in undropable:
				await dropitem(command[5:])
			else:
				print("you can't drop that")
		elif command.startswith("eat "):
			eatitem(command[4:])
		elif command == "stats":
			print(f"HP: {hp}/{maxhp}\nMP: {mp}/{maxmp}\n\nSTATS")
			for n in range(skillsunlocked):
				print(f"{skill[n]}: you are currently level {level[n]}, you have {exp[n]}exp and need {xp(level[n] + 1) - exp[n]}exp more to level up")
		elif command == "commands":
			print('NORMAL COMMANDS:\ncommands: get a list of commands\nexamine: learn the interactable objects in the area you are currently in\ninteract (x)/(x)/i (x): interact with the (x)th object in the area (listed in the area\'s examine text)\nattack: begin a battle with the enemy in the area (if there is one)\nnorth/n/up/u: go north\neast/e/right/r: go east\nsouth/s/down/d: go south\nwest/w/left/l: go west\ngold/g: check how much gold you have\ninventory: check your inventory\nquit/exit/end: quit the game\ncookbook: get a list of recipes learned\ncrafting: get a list of items you can make at crafting facilities\ndrop (item): remove an instance of (item) from your inventory (if you have one)\ndrop all (item): remove all instances of (item) from your inventory\neat (item): eat a item (if edible) and heal back some hp/mp\nstats: get a list of your stats\ncompass: learn what area you are in and the areas around you\nBATTLE COMMANDS:\nattack: use your normal attack (you will be attacked back)\nstance: change your stance to change what exp you get\nspecial attack: perform your special attack (you will be attacked back)\nspecial check: check what your special attack is\neat (item): eat a item (if edible) and heal back some hp/mp')
		elif command in ("interact 1", "interact one", "1", "one", "i 1", "i1"):
			if x == 0 and y == 0:
				print('the plaque on the statue reads "william hospy (6.342 - 6.385), founder of hospy, father of too many, and master explorer"')
			elif x == 0 and y == 1:
				if quest[0] == "shelf":
					print("you search the shelves and find a book named \"iron weaponry schematics\", but just as you go to take it out, the librarian comes up to you, \"don't do it! don't give those goblins that book. last week they sent a fool like you to get a book on raiding and we lost our month's wheat supply! just please don't do it. i have a plan, but let's go... somewhere more private.\"")
					quest[0] = "schematics"
				else:
					print("nothing here intrests you at all. just old dusty history books and stuff")
			elif x == -1 and y == -1:
				if quest[0] == "start":
					print('the hobgoblin speaks to you in a think goblinese accent and broken common, "you help us big human, i need you to go in library and get iron sword schematics. if you do it, i will give big money. you in?" (y/n)')
					command2 = await input("")
					command2 = command2.lower()
					if command2 == "y":
						print('the hobgoblin bows in respect, "thank you big human for help"')
						quest[0] = "shelf"
					else:
						print('the hobgoblin ignores you')
				elif quest[0] == "schematics":
					print('you see his eye light up as he sees you carrying the book, "thanks much for this! here reward as promised." he hands you a small bag of coins (30)')
					gold += 30
					quest[0] = "goblinfinish"
				elif quest[0] == "goblinfinish":
					print("the hobgoblin points and says to a goblin worker, \"that one, that one is ally, don't attack him... he help alot\"")
				elif quest[0] == "fake":
					print('you see his eye light up as he sees you carrying the book, "thanks much for this! here reward as promised." he hands you a small bag of coins (30)')
					gold += 30
					quest[0] = "fakefinish"
				elif quest[0] == "fakefinish":
					print('the hobgoblin looks quite on edge, \"iron sword hasn\'t worked yet human, it better\"')
				else:
					print("he ignores you")
			elif x == -1 and y == 0:
				additem("wheat")
				if true == True:
					print("you pick up the wheat")
				else:
					print("you have no inventory slots available")
			elif x == 1 and y == 1:
				if gold >= 12:
					if hp == maxhp and mp == maxmp:
						print("there is no need to rest right now")
					else:
						print("would you like to stay the night for 12g? (y/n)")
						command2 = await input("")
						command2 = command2.lower()
						if command2 == "y":
							gold -= 12
							print("you fully restore hp and mp")
							hp = maxhp
							mp = maxmp
				else:
					print("you don't have enough for a room")
			elif x == 0 and y == -1:
				gather("carp")
			elif x == 1 and y == -1:
				if level[3] >= 10:
					if fishguildmembership == False:
						if gold >= 35:
							print('the guildmaster welcomes you, "welcome to the fishing guild! we can tell you are quite skilled at fishing, and we are always looking for new members. would you like to buy membership for 35g? (y/n)"')
							command2 = await input("")
							command2 = command2.lower()
							if command2 == "y":
								fishguildmembership = True
								gold -= 35
								titles.append("member of fishing guild")
							else:
								print('the guildmaster sighs, "that\'s completely understandable"')
						else:
							print('the guildmaster welcomes you, "welcome to the fishing guild! we can tell you are quite skilled at fishing, and we are always looking for new members. but membership is quite pricey (35g), so come back when you are a little, mmmm.... richer"')
					else:
						if quest[1] == "summon2" and  "rune" not in upgrades:
							print('the guildmaster says, "here is that rune"')
							additem("summoning rune")
							if true == True:
								print("gary hands you an demonic summoning rune")
								upgrades.append("rune")
							else:
								print("gary tries to hand you a summoning rune, but your inventory is full")
						if quest[1] == "summon":
							print('you ask gary about the rune, "well since you\'re a guildmember, i can trust you that you will not do anything wrong with it. here is the rune, though it does require one thing, to charge it up, you must feed it quote \'the flesh of a bovine\' at a crafting table. good luck"')
							quest[1] = "summon2"
							additem("summoning rune")
							if true == True:
								print("gary hands you an demonic summoning rune")
								upgrades.append("rune")
							else:
								print("gary tries to hand you a summoning rune, but your inventory is full")
						else:
							print('gary welcomes you back to the guild')
				else:
					print("you cannot use anything in the fishing guild, come back when you are a higher fishing level")
			elif x == 2 and y == 0:
				additem("milk")
				if true == True:
					print("you grab a bucket and milk the diary cow")
				else:
					print("you have no inventory slots available")
			elif x == 1 and y == 0:
				if gold > 47:
					if "armourstall" not in upgrades:
						print("would you like to upgrade your armour for 48g (y/n)")
						command2 = await input("")
						command2 = command2.lower()
						if command2 == "y":
							print("you upgrade your armour and you feel more safe")
							gold -= 48
							bonusdef += 1
							upgrades.append("armourstall")
						else:
							print("quite understandable")
					else:
						print("you already own this item")
				else:
					print("you do not have enough money to buy anything here")
			elif x == -1 and y == 1:
				if "goggle" in upgrades:
					if "massivespidermother" in tasksdone:
						print('the spider looks over you and says, "you have done everything i need you to do"')
					elif task == "massivespidermother" and taskamount == 0:
						print('the spider bares its giant fangs, "thank you for this delivery puny human, here is the reward i promised"')
						tasksdone.append("massivespidermother")
						print("the spider spits it's acid on your sword, improving its offensive abilities")
						task = "none"
						currenttask = "none"
						bonusatt += 1
					elif task == "massivespidermother" and taskamount != 0:
						print(f'the spider reminds you of the {taskamount} goblins you still have to kill')
					elif task == "none":
						print('the spider speaks to you, "would you like to collect me some goblin bodies, maybe 12, and i\' give you a reward (y/n)"')
						command2 = await input("")
						command2 = command2.lower()
						if command2 == "y":
							task = "massivespidermother"
							currenttask = "goblin"
							taskamount = 12
							print('the spider says, "thank you human"')
						else:
							print('the spider says, "i\'ll know you will back, puny human"')
					else:
						print("the spider tells you to finish your other task before helping her with hers")
				else:
					print("there is no interactable object in that slot")
			elif x == 2 and y == 1:
				if quest[1] == "start":
					print('the portmaster welcomes you to the w.h. port, "i would suggest you one of these boat, but the only way of getting to go to the mainland is to do something of \'grand importance\', so i was wondering if you could help me fake a crisis for you to solve. you up for it? (y/n)"')
					command2 = await input("")
					command2 = command2.lower()
					if command2 == "y":
						print('the portmaster\'s face lights up, "thank you so much, i would suggest talking to the librarian west of here about summoning monsters, that sounds crisislike right?"')
						quest[1] = "crisis"
					else:
						print('the portmaster says, "thanks for listenin\' mate"')
				elif quest[1] == "crisis":
					print('the portmaster asks, "have you gone to the librarian and learnt about summoning yet? if not go do that now"')
				elif quest[1] in ("summon", "summon2"):
					print('you tell the portmaster about the demon, rune, and the candles, "you can get some wax for the candles to the south of \'ere you know"')
				elif quest[1] == "ready":
					print('you talking about you success with charging the rune, "what are you doing here then you donce! go and summon it"')
				elif quest[1] == "impkilled":
					print('the portmaster looks proud, "i saw what you did out there young skipper, well done indeed, i would say that they would let you on the the mainland now."')
					quest[1] = "finished"
					print('he says, "i could give you a one-time free trip to loogustia port. would you like that? (y/n)"')
					command2 = await input("")
					command2 = command2.lower()
					if command2 == "y":
						print("you take a short boat trip to loogustia as you see the mainland for the first time")
						x = 6
						y = 6
						print("you are in loogustia port")
				else:
					if gold > 11:
						print("would you like to go to loogutsia harbour for 12g (y/n)?")
						command2 = await input("")
						command2 = command2.lower()
						if command2 == "y":
							gold -= 12
							print("you take a short boat trip to loogustia as you see the mainland")
							x = 6
							y = 6
					else:
						print("you do not have enough money for a boat trip")
			elif x == 6 and y == 6:
				if gold > 11:
					print("would you like to go to w.h. port for 12g (y/n)?")
					command2 = await input("")
					command2 = command2.lower()
					if command2 == "y":
						gold -= 12
						print("you take a short boat trip to the small island of hospy")
						x = 2
						y = 1
				else:
					print("you do not have enough money for a boat trip")
			elif x == 7 and y == 6:
				await cook()
			elif x == 6 and y == 7:
				additem("seaweed")
				if true == True:
					print("you grab a handleful of seaweed")
				else:
					print("you have no inventory slots available")
			elif x == 7 and y == 7:
				additem("milk")
				if true == True:
					print("you grab a bucket and milk the diary cow")
				else:
					print("you have no inventory slots available")
			elif x == 6 and y == 8:
				print("the mage scrambles around, looking for some sort of item. they are deep in focus and shouldn't be bothered")
			else:
				print("there is no interactable object in that slot")
		elif command in ("interact 2", "interact two", "2", "two", "i 2", "i2"):
			if x == 0 and y == 0:
				print('the instructor teaches the basics of combat, "to attack an enemy, you type "attack" and you begin combat, but be warned, you cannot exit combat prematurely. there are also battles that occur without you typing "attack" so always be wary')
			elif x == 0 and y == 1:
				if quest[0] == "schematics":
					print('the librarian whispers into your ear, looking around for others, "i will make you a fake iron sword schematic and you will give it to the goblins. when they try to make the iron swords, they won\'t be cool and will be unusable. and they will be none the wiser!" he quickly whips up the schematic and gives it to you')
					quest[0] = "fake"
				elif quest[0] == "goblinfinish" and quest[1] == "crisis":
					print('the librarian looks mad at you, "i know i shouldn\'t help you because you helped those digusting monsters, but i can tell you really want to go to the mainland. what you\'ll need to do to start a crisis is to summon a demon in the middle of town, all you\'ll need is 4 candles lit in a circle, a special demonic rune (which gary the guildmaster might know a thing or two about), and type "gusto permo hosti". and that\'s all! now get out"')
					quest[1] = "summon"
					print('you are now in hospy')
					y = 0
				elif quest[0] == "goblinfinish":
					print('the librarian yells, "get out of the library!"')
					print('you are now in hospy')
					y = 0
				elif quest[1] == "crisis":
					print('you tell the librarian about the port, and he seems eager to help, "what you\'ll need to do to start a crisis is to summon a demon in the middle of town, all you\'ll need is 4 candles lit in a circle, a special demonic rune (which gary the guildmaster might know a thing or two about), and type "gusto permo hosti". and that\'s all! i wish you all the luck, all of it"')
					quest[1] = "summon"
				elif quest[0] == "fakefinish":
					print('you tell him the goblins fell for the trick. \"thank kop that was close! if i didn\'t intervene, we may have been doomed!\"')
					quest[0] = "truefinish"
				else:
					print("he looks too busy to talk to right now")
			elif x == -1 and y == 0:
				switchitem("wheat", "flour")
				if true == True:
					print("you grind the wheat into flour")
				else:
					print("you do not have wheat to turn into flour")
			elif x == -1 and y == -1:
				gather("purpleberry")
			elif x == 0 and y == -1:
				await cook()
			elif x == 1 and y == -1:
				if level[3] >= 10:
					gather("trout")
				else:
					print("you cannot use anything in the fishing guild, come back when you are a higher fishing level")
			elif x == 2 and y == 0:
				switchitem("milk", "butter")
				if true == True:
					print("you churn the milk into some creamy butter")
				else:
					print("you do not have milk to turn into butter")
			elif x == 1 and y == 0:
				if gold > 35:
					if "weaponstall" not in upgrades:
						print("would you like to upgrade your sword for 36g (y/n)")
						command2 = await input("")
						command2 = command2.lower()
						if command2 == "y":
							print("you upgrade your sword and you feel more powerful")
							gold -= 36
							bonusatt += 1
							upgrades.append("weaponstall")
						else:
							print("quite understandable")
					else:
						print("you already own this item")
				else:
					print("you do not have enough money to buy anything here")
			elif x == 2 and y == 1:
				print('the elven ambassador speaks to you, "we are looking for some adventurers to help us in the elven lands of the north, m!rte, but you not fit the bill, you don\'t even know magic"')
			elif x == 6 and y == 6:
				print('the local guide welcomes you to the mainland, "loogustia is a small seaside town, but we are still home to some extraordinary things! like one of only 3 wizard towers on the whole of the mainland, and the oldest town hall aswell"')
			elif x == 7 and y == 6:
				await craft()
			elif x == 6 and y == 7:
				if "fishing net" in inventory:
					if level[3] >= 20:
						gather("anchovies")
					else:
						print("you cannot fishing in this spot, come back when you are a higher fishing level")
				else:
					print("you do not have a fishing net so you cannot fish here")
			elif x == 7 and y == 7:
				switchitem("milk", "butter")
				if true == True:
					print("you churn the milk into some creamy butter")
				else:
					print("you do not have milk to turn into butter")
			elif x == and 6 y == 8:
				gather("wood")
			else:
				print("there is no interactable object in that slot")
		elif command in ("interact 3", "interact three", "3", "three", "i 3", "i3"):
			if x == 0 and y == 0:
				print('you introduce your self to the mayor, and he starts talking about being mayor "it is not a sissy\'s job, let me tell you that much. it\'s hard work out there, i have to talk to people all day, and that is extremely socially draining"')
			elif x == 0 and y == -1:
				additem("water")
				if true == True:
					print("you collect some water in a near by bucket")
				else:
					print("you have no inventory slots available")
			elif x == -1 and y == 0:
				gather("wood")
			elif x == 1 and y == -1:
				if level[3] >= 10:
					if level[3] >= 15:
						gather("pike")
					else:
						print("you cannot fishing in this spot, come back when you are a higher fishing level")
				else:
					print("you cannot use anything in the fishing guild, come back when you are a higher fishing level")
			elif x == 1 and y == 0:
				if gold > 19:
					if "goggle" not in upgrades:
						print("would you like to purchase night-vision goggles for 20g (y/n)")
						command2 = await input("")
						command2 = command2.lower()
						if command2 == "y":
							print("you purchase and put the goggles on, everything seems so bright!")
							gold -= 20
							upgrades.append("goggle")
						else:
							print("quite understandable")
					else:
						print("you already own this item")
				else:
					print("you do not have enough money to buy anything here")
			elif x == 2 and y == 0:
				additem("wax")
				if true == True:
					print("you carefully collect some wax from the bee hive")
				else:
					print("you have no inventory slots available")
			elif x == 0 and y == 1:
				await craft()
			elif x == 6 and y == 6:
				print('the merchant greets you, "you got any gems to sell? i pay a pretty penny for gems you know. to sell a gem, type "sell (gem)" and make sure you have the item!"')
				command2 = await input("")
				command2 = command2.lower()
				if command2.startswith("sell "):
					if command2[5:] in ("pearl", "opal"):
						sellitem(command2[5:])
						if true == True:
							if command2[5:] == "pearl":
								print("you gain 30 gold")
								gold += 30
							if command2[5:] == "opal":
								print("you gain 25 gold")
								gold += 25
					else:
						print("you cannot sell this item here")
				else:
					print("you can't do this here")
			elif x == 7 and y == 6:
				gather("trout")
			elif x == 7 and y == 7:
				switchitem("milk", "cheese")
				if true == True:
					print("you press the milk into a block of cheese")
				else:
					print("you do not have milk to turn into cheese")
			else:
				print("there is no interactable object in that slot")
		elif command in ("interact 4", "interact four", "4", "four", "i 4", "i4"):
			if x == 1 and y == -1:
				if level[3] >= 10:
					print('the shoprunner greets you, "thank you for coming to my shop! i buy cooked fish. to sell a fish, type "sell (fish)" and make sure you have the item!"')
					command2 = await input("")
					command2 = command2.lower()
					if command2.startswith("sell "):
						if command2[5:] in ("carp", "trout", "pike", "anchovies"):
							sellitem(command2[5:])
							if true == True:
								if command2[5:] == "carp":
									print("you gain 2 gold")
									gold += 2
								elif command2[5:] == "trout":
									print("you gain 3 gold")
									gold += 3
								elif command2[5:] == "pike":
									print("you gain 4 gold")
									gold += 4
								elif command2[5:] == "anchovies":
									print("you gain 6 gold")
									gold += 6
						else:
							print("you cannot sell this item here")
					else:
						print("you can't do this here")
				else:
					print("you cannot use anything in the fishing guild, come back when you are a higher fishing level")
			elif x == 2 and y == 0:
				additem("egg")
				if true == True:
					print("you grab an egg from the coop")
				else:
					print("you have no inventory slots available")
			else:
				print("there is no interactable object in that slot")
		elif command in ("gold", "g"):
			print(f"you have {gold} gold")
		elif command in ("north", "n", "up", "u"):
			if immovable == 0:
				if locations.get((x, y+1)) not in ("sea", "wall"):
					y += 1
					print(f"you move north and end up in {locations.get((x, y))}")
				else:
					print("you cannot move more north")
			else:
				print("you cannot move from this area")
		elif command in ("south", "s", "down", "d"):
			if immovable == 0:
				if locations.get((x, y-1)) not in ("sea", "wall"):
					y -= 1
					print(f"you move south and end up in {locations.get((x, y))}")
				else:
					print("you cannot move more south")
			else:
				print("you cannot move from this area")
		elif command in ("east", "e", "right", "r"):
			if immovable == 0:
				if locations.get((x+1, y)) not in ("sea", "wall"):
					x += 1
					print(f"you move east and end up in {locations.get((x, y))}")
				else:
					print("you cannot move more east")
			else:
				print("you cannot move from this area")
		elif command in ("west", "w", "left", "l"):
			if immovable == 0:
				if locations.get((x-1, y)) not in ("sea", "wall"):
					x -= 1
					print(f"you move west and end up in {locations.get((x, y))}")
				else:
					print("you cannot move more west")
			else:
				print("you cannot move from this area")
		elif command in ("attack", "interact attack", "i a", "i attack", "interact a"):
			if (x, y) in fight:
				print("are you sure you would like to begin combat? (y/n)")
				command2 = await input("")
				command2 = command2.lower()
				if command2 == "y":
					if x == -1 and y == -1:
						await battle("goblin mugger", 1, 1, 35, 30, 4, "goblin", "", 0, 0)
					elif x == -1 and y == 1:
						await battle("giant spider", 1, 1, 10, 15, 2, "spider", "", 0, 0)
					elif x == 0 and y == -1:
						await battle("hobgoblin fisher", 2, 2, 40, 65, 8, "goblin", "", 0, 0)
					elif x == 2 and y == 1:
						await battle("merfolk", 3, 1, 45, 72, 10, "seabeast", "raw carp", 4, 0)
					elif x == 2 and y == 0:
						await battle("bull", 1, 1, 24, 10, 1, "livestock", "raw beef", 1, 0)
					elif x == 6 and y == 6:
						await battle("siren", 2, 3, 55, 75, 12,"seabeast", "pearl", 5, 0)
					elif x == 7 and y == 6:
						await battle("punching bag", 0, 1, 100, 0, 0, "nothing", "", 0, 1)
					elif x == 7 and y == 6:
						await battle("ogre", 4, 2, 77, 95, 15, "giant", "opal", 4, 0)
				else:
					print("understandable")
			else:
				print("there is no-one here to fight")
		elif command == "gusto permo hosti":
			if quest [1] == "ready": 
				if x == 0 and y == 0:
					if inventory.count("candle") >= 4 and "charged summoning rune" in inventory:
						print("you place the candles in a circle and recite the words")
						print('a small imp raises up from the ground, as the mayor sighs, "i don\'t have time for this"')
						print("a battle begins!")
						for t in range(4):
							removeitem("candle")
						removeitem("charged summoning rune")
						await battle("small imp", 3, 2, 66, 198, 15, "demon", "", 0, 0)
						print("you have stopped a crisis!")
						titles.append("crisis stopper")
						quest[1] = "impkilled"
					else:
						print("you don't have everything you need, you need...\n1. 4 candles\n2. a charged summoning rune")
				else:
					print("you have to do this in the town hall")
			elif quest[1] in ("finished", "impkilled"):
				print("why even try to do it again?!")
			elif quest[1] in ("summon", "summon2"):
				print("you are not ready")
			else:
				print("what are you saying?!")
		elif command == "cookbook":
			print("RECIPES LEARNED")
			print("LEGEND| recipe name: ingredients")
			print("bread: water + flour, heals 25hp")
			print("carp: raw carp, heals 19hp")
			print("cake: flour + milk + eggs, heals 16hp, leaves a slice which also heals 16hp")
			print("beef: raw beef, heals 15hp")
			print("purpleberry pie: purpleberry + flour + water, heals 10mp, leaves a slice which also heals 10mp")
			if level[3] >= 10:
				print("trout: raw trout + flour, heals 28hp")
			if level[3] >= 15:
				print("pike: raw pike + butter, heals 37hp")
			if level[3] >= 20:
				print("anchovies: raw anchovies + egg + butter, heals 46hp")
		elif command == "crafting":
			print("RECIPES LEARNED")
			print("LEGEND| recipe name: ingredients")
			print("candle: wax")
			if "rune" in upgrades:
				print("charged summoning rune: summoning rune + raw beef") 
			if fishguildmembership == True:
				print("fishing net part: seaweed + seaweed + seaweed")
				print("fishing net: fishing net part + fishing net part + fishing net part + fishing net part")
		elif command == "compass":
			print(f"you are currently in: {locations.get((x, y))}")
			print(f"to your north: {locations.get((x, y+1))}")
			print(f"to your east: {locations.get((x+1, y))}")
			print(f"to your south: {locations.get((x, y-1))}")
			print(f"to your west: {locations.get((x-1, y))}")
		else:
			print(f'there is no function called "{command}", try a different command')
		while exp[0] >= xp(level[0] + 1):
			maxhp += 10
			hp = maxhp
			level[0] += 1
			print(f"you advanced a hitpoints level, you are now level {level[0]}. you have also restored all health")
		for skills in range(5):
			while exp[skills + 1] >= xp(level[skills + 1] + 1):
				level[skills + 1] += 1
				print(f"you advanced a {skill[skills + 1]} level, you are now level {level[skills + 1]}")
		if skillsunlocked > 6:
			while exp[6] >= xp(level[6] + 1):
				level[6] += 1
				maxmp += 10
				mp = maxmp
				print(f"you advanced a magic level, you are now level {level[6]}. you have also restored all magic points")

import asyncio
asyncio.ensure_future(main())