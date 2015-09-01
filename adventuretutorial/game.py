"""
A simple text adventure designed as a learning experience for new programmers.
"""
__author__ = ['Phillip Johnson', 'Chad Wilson']

import world
from player import Player

def play():
    world.load_tiles()
    player = Player()
    #This line loads the player into the starting room location and displys the room text
    player.move(2,5) # starting location
    while player.is_alive() and not player.victory:
        room = world.tile_exists(player.location_x, player.location_y)
        room.modify_player(player)
        # Check again since the room could have changed the player's state
        if player.is_alive() and not player.victory:
            print "Choose an action:\n"
            available_actions = room.available_actions()
            for action in available_actions:
                print action
            action_input = str(raw_input("Action: "))
            for action in available_actions:
                if action_input == action.hotkey:
                    player.do_action(action, **action.kwargs)
                    break

if __name__ == "__main__":
    play()
