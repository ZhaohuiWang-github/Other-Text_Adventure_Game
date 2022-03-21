# You can change the config file here
config_file = "game2.txt"

import re


# load data from configuration file.
def load_data(filepath):
    inventory = []
    game_info = {}
    game_map = {}
    npc_s = {}

    # use "with open"
    with open(filepath, "r") as config_file:
        for line in config_file:
            # step 1: construct game_info
            if line.startswith("game"):
                line = line.strip()
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                game_info.setdefault(key, value)

            # step 2: construct game_map
            elif line.startswith("r_id"):
                line = line.strip()
                r_id = line.split(":", 1)[1]
                r_id = r_id.strip()
                game_map.setdefault(r_id, {})
                game_map[r_id].setdefault("id", r_id)
                # add the empty obj list here
                game_map[r_id].setdefault("obj", [])

            elif line.startswith("r_desc"):
                line = line.strip()
                r_desc = line.split(":", 1)[1]
                r_desc = r_desc.strip()
                game_map[r_id].setdefault("desc", r_desc)

            elif line.startswith("r_obj"):
                line = line.strip()
                r_obj = line.split(":", 1)[1]
                r_obj = r_obj.strip()
                game_map[r_id]["obj"].append(r_obj)

            elif line.startswith("r_north"):
                line = line.strip()
                r_north = line.split(":", 1)[1]
                r_north = r_north.strip()
                game_map[r_id].setdefault("north", r_north)

            elif line.startswith("r_south"):
                line = line.strip()
                r_south = line.split(":", 1)[1]
                r_south = r_south.strip()
                game_map[r_id].setdefault("south", r_south)

            elif line.startswith("r_east"):
                line = line.strip()
                r_east = line.split(":", 1)[1]
                r_east = r_east.strip()
                game_map[r_id].setdefault("east", r_east)

            elif line.startswith("r_west"):
                line = line.strip()
                r_west = line.split(":", 1)[1]
                r_west = r_west.strip()
                game_map[r_id].setdefault("west", r_west)

            elif line.startswith("r_hiddenobj"):
                line = line.strip()
                r_hiddenobj = line.split(":", 1)[1]
                r_hiddenobj = r_hiddenobj.strip()
                game_map[r_id].setdefault("hiddenobj", r_hiddenobj)

            elif line.startswith("r_hiddenpath"):
                line = line.strip()
                r_hiddenpath = line.split(":", 1)[1]
                r_hiddenpath = r_hiddenpath.strip()
                game_map[r_id].setdefault("hiddenpath", r_hiddenpath)
                # This flag is to mark if the hidden path has been found
                game_map[r_id].setdefault("hiddenpath_flag", False)

            # step 3: construct the npc_s
            # use RegEx to judge npcs‘ location and sentences
            elif re.search(r'npc_[a-zA-Z0-9]+_loc', line.strip()):
                line = line.strip()
                a_npc_name = line.split("_", 2)[1]
                npc_s.setdefault(a_npc_name, {})
                npc_s[a_npc_name].setdefault("npc_loc", line.split(":")[1].strip())
                # This flag is to mark whether it is the first chat with the npc
                npc_s[a_npc_name].setdefault("npc_first_time", True)

            elif re.search(r'npc_[a-zA-Z0-9]+_1', line.strip()):
                line = line.strip()
                npc_s[a_npc_name].setdefault("npc_1", line.split(":")[1].strip())

            elif re.search(r'npc_[a-zA-Z0-9]+_2', line.strip()):
                line = line.strip()
                npc_s[a_npc_name].setdefault("npc_2", line.split(":")[1].strip())

            # step 4: deal with the --- and error
            elif line == "---\n":
                pass

            else:
                print("ERROR: " + line)

    return inventory, game_info, game_map, npc_s


# show details of current location
def show_desc(game_map, r_id, npc_s):
    # show the description of the current location
    desc = game_map[r_id]["desc"]
    print("You are", desc)
    # show the list of objects in the current position
    # if it is empty, nothing should be output
    obj = game_map[r_id]["obj"]
    for a_obj in obj:
        print("There is a " + a_obj + " here.")
    # show the name of the NPC at the current location
    for a_npc_name in npc_s.keys():
        if r_id == npc_s[a_npc_name]["npc_loc"]:
            print("The npc", a_npc_name, "is here.")


# for inv command
def show_inv(inventory):
    print("Your inventory: ", inventory)


# for goal command
def show_goal(gameinfo):
    print("The goal of this game is to:")
    print(gameinfo["game_goal"])


# for search command
def search(r_id, game_map):
    search_flag = False
    # search hidden object
    if "hiddenobj" in game_map[r_id].keys():
        print("You found a " + game_map[r_id]["hiddenobj"])
        # first add this hiddenobj to this loc's obj list
        game_map[r_id]["obj"].append(game_map[r_id]["hiddenobj"])
        # then delete this hiddenobj
        del game_map[r_id]["hiddenobj"]
        search_flag = True
    # search hidden path
    if "hiddenpath" in game_map[r_id].keys():
        print("You found a hidden path!")
        game_map[r_id]["hiddenpath_flag"] = True
        search_flag = True

    if not search_flag:
        print("You searched nothing.")
    return game_map


# for move path command
def move_path(r_id, game_map):
    if "hiddenpath_flag" in game_map[r_id].keys():
        if game_map[r_id]["hiddenpath_flag"]:
            r_id = game_map[r_id]["hiddenpath"]
        else:
            print("WARNING: You have to find a hidden path first.")
    else:
        print("WARNING: You have to find a hidden path first.")
    return r_id


# for take command
def take(r_id, game_map, cmd, inventory):
    item = cmd.split(" ", 1)[1].strip()
    if item in game_map[r_id]["obj"]:
        # first add this item to player's inventory
        inventory.append(item)
        # then remove this item from this loc's obj list
        game_map[r_id]["obj"].remove(item)
    else:
        print("WARNING: That object is not here.")
    return inventory, game_map


# for drop command
def drop(r_id, game_map, cmd, inventory):
    item = cmd.split(" ", 1)[1].strip()
    if item in inventory:
        # first add this item to this loc's obj list
        game_map[r_id]["obj"].append(item)
        # then remove this item from the player's inventory
        inventory.remove(item)
    else:
        print("WARNING: The", item, "is not in your inventory")
    return inventory, game_map


# for move command
def move(r_id, game_map, cmd, x_size, y_size):
    direction = cmd.split(" ", 1)[1].strip()
    if direction.lower() == "west":
        if "west" in game_map[str(r_id)].keys():
            r_id = game_map[str(r_id)]["west"]
        else:
            # if there is no other location to the west of the location
            if r_id % x_size == 1:
                r_id = r_id + x_size - 1
            else:
                r_id = r_id - 1

    elif direction.lower() == "east":
        if "east" in game_map[str(r_id)].keys():
            r_id = game_map[str(r_id)]["east"]
        else:
            # if there is no other location to the east of the location
            if r_id % x_size == 0:
                r_id = r_id - x_size + 1
            else:
                r_id = r_id + 1

    elif direction.lower() == "north":
        if "north" in game_map[str(r_id)].keys():
            r_id = game_map[str(r_id)]["north"]
        else:
            # if there is no other location to the north of the location
            if r_id - x_size < 1:
                r_id = r_id + x_size * (y_size - 1)
            else:
                r_id = r_id - x_size

    elif direction.lower() == "south":
        if "south" in game_map[str(r_id)].keys():
            r_id = game_map[str(r_id)]["south"]
        else:
            # if there is no other location to the south of the location
            if r_id + x_size > x_size * y_size:
                r_id = r_id + x_size - x_size * y_size
            else:
                r_id = r_id + x_size

    else:
        print("WARNING:", direction, "is not a correct direction")

    return str(r_id)


# for talk command
def talk(r_id, npc_s, cmd):
    npc_name = cmd.split(" ", 1)[1].strip()
    # determine if it is an NPC
    if npc_name in npc_s.keys():
        # determine if the location is correct
        if r_id == npc_s[npc_name]["npc_loc"]:
            # the first talk
            if npc_s[npc_name]["npc_first_time"]:
                print(npc_name, ": ", npc_s[npc_name]["npc_1"])
                npc_s[npc_name]["npc_first_time"] = False
            # the second and subsequent talks
            else:
                print(npc_name, ": ", npc_s[npc_name]["npc_2"])
        else:
            print("WARNING:", npc_name, "is not a npc here")
    else:
        print("WARNING:", npc_name, "is not a npc here")

    return npc_s


# for exit command
def game_exit():
    print("You successfully exit this game.")
    return False


# main
def main():
    # you can change the config file here
    # config_file = "game1.txt"

    # load game's config file
    inventory, gameinfo, game_map, npc_s = load_data(config_file)

    x_size = int(gameinfo["game_xsize"])
    y_size = int(gameinfo["game_ysize"])

    goal_loc = gameinfo["game_goalloc"]
    goal_obj = gameinfo["game_goalobj"]

    # Get the position at the start of the game
    r_id = gameinfo["game_start"]
    # flag used to end the game
    game_flag = True

    # game start prompt
    print("Welcome to " + gameinfo["game_name"])
    print(" ")
    print("The goal of this game is to:")
    print(gameinfo["game_goal"])

    while game_flag:
        print(" ")

        # judge whether the goal is achieved
        if (r_id == goal_loc) and (goal_obj in game_map[goal_loc]["obj"]):
            print("Congratulations! You have won the game.")
            break

        # show information about current location
        show_desc(game_map, r_id, npc_s)

        # prompt the user to enter a command
        cmd = input("What next?  ")
        # determine different commands and make corresponding responses
        if cmd.lower() == "inv":
            show_inv(inventory)

        elif cmd.lower() == "goal":
            show_goal(gameinfo)

        elif cmd.lower() == "search":
            search(r_id, game_map)

        elif cmd.lower() == "move path":
            r_id = move_path(r_id, game_map)

        elif cmd.lower().startswith("take "):
            inventory, game_map = take(r_id, game_map, cmd, inventory)

        elif cmd.lower().startswith("drop "):
            inventory, game_map = drop(r_id, game_map, cmd, inventory)

        elif cmd.lower().startswith("move "):
            r_id = move(int(r_id), game_map, cmd, x_size, y_size)

        elif cmd.lower().startswith("talk "):
            npc_s = talk(r_id, npc_s, cmd)

        elif cmd.lower() == "exit":
            game_flag = game_exit()

        else:
            print("WARNING: wrong command")


if __name__ == '__main__':
    main()
