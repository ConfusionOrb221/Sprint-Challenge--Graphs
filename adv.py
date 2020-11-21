from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

def dft(explored, prev=None, move=None):
    starting_id = player.current_room.id
    exits = player.current_room.get_exits()
    #Creates a reverse dictionary to easily take us backwards without having to do if statements
    reverse_dict = {'s': 'n', 'n': 's', 'e': 'w', 'w': 'e'}

    #Creates dicts for paths we have explored and where each room connects to
    if starting_id not in explored:
        explored[starting_id] = {}
    #Add the move to a already currently explored 
    if move is not None:
        explored[prev][move] = starting_id
    
    if prev is not None:
        explored[starting_id][reverse_dict[move]] = prev
    #if we still have rooms to explore in current then we explore them
    if len(explored[starting_id]) < len(exits):
        for movement in exits:
            if movement not in explored[starting_id]:
                player.travel(movement)
                traversal_path.append(movement)
                dft(explored, prev=starting_id, move=movement)
    #if we dont then we go back till we a hit a room that we do have rooms to explore
    if len(explored) < len(room_graph):
        movement = reverse_dict[move]
        player.travel(movement)
        traversal_path.append(movement)
explored = {}
dft(explored)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
#player.current_room.print_room_description(player)
#while True:
#    cmds = input("-> ").lower().split(" ")
#    if cmds[0] in ["n", "s", "e", "w"]:
#        player.travel(cmds[0], True)
#    elif cmds[0] == "q":
#        break
#    else:
#        print("I did not understand that command.")
