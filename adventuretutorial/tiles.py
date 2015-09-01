"""Describes the tiles in the world space."""
__author__ = ['Phillip Johnson', 'Chad Wilson']

import items, enemies, actions, world

class MapTile(object):
    """The base class for a tile within the world space"""
    def __init__(self, x, y):
        """Creates a new tile.

        :param x: the x-coordinate of the tile
        :param y: the y-coordinate of the tile
        """
        self.x = x
        self.y = y
        self.id = "??????????"

    def intro_text(self):
        """Information to be displayed when the player moves into this tile."""
        raise NotImplementedError()

    def modify_player(self, player):
        """Process actions that change the state of the player."""
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves

    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
        moves.append(actions.ViewMap())
        return moves


class StartingRoom(MapTile):
    def __init__(self, x, y):
        super(StartingRoom, self).__init__(x,y)
        self.id = "START"

    def intro_text(self):
        return """
        You find yourself in a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """

    def modify_player(self, player):
        # Room has no action on player. Must override parent method because of raise()
        pass


class EmptyCavePath(MapTile):
    def __init__(self, x, y):
        super(EmptyCavePath, self).__init__(x, y)
        self.id = "Empty Cave Path"

    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """

    def modify_player(self, player):
        pass


class LootRoom(MapTile):
    """A room that adds something to the player's inventory"""
    def __init__(self, x, y, item):
        self.item = item
        super(LootRoom, self).__init__(x, y)

    def add_loot(self, player):
        if isinstance(self.item, items.Gold):
            player.add_gold(self.item.amount)
        else:
            player.inventory.append(self.item)

        self.item = None

    def modify_player(self, player):
        if self.item:
            self.add_loot(player)
        

class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super(FindDaggerRoom, self).__init__(x, y, items.Dagger())
        self.id = "Treasure: Dagger"

    def intro_text(self):
        if self.item:
            return """
            You notice something shiny in the corner.
            It's a dagger! You pick it up.
            """
        else:
            return """
            This is the room that your dagger was found in.
            Nothing else remarkable about the room now.
            """


class Find5GoldRoom(LootRoom):
    def __init__(self, x, y):
        super(Find5GoldRoom, self).__init__(x, y, items.Gold(5))
        self.id = "Treasure: Gold"

    def intro_text(self):
        if self.item:
            return """
            Someone dropped a 5 gold piece. You pick it up.
            """
        else:
            return """
            You discovered gold in this room.
            It is now empty and unremarkable.
            """


class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super(EnemyRoom, self).__init__(x, y)

    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print "Enemy does {0} damage. You have {1} HP remaining.".format(self.enemy.damage, the_player.hp)

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()


class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super(GiantSpiderRoom, self).__init__(x, y, enemies.GiantSpider())
        self.id = "Giant Spider"

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider lies rotting on the ground.
            """


class OgreRoom(EnemyRoom):
    def __init__(self, x, y):
        super(OgreRoom, self).__init__(x, y, enemies.Ogre())
        self.id = "Ogre"

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            An ogre is blocking your path!
            """
        else:
            return """
            A dead ogre reminds you of your triumph.
            """

 
class SnakePitRoom(MapTile):
    def intro_text(self):
        return """
        You have fallen into a pit of deadly snakes!

        You have died!
        """

    def modify_player(self, player):
        player.hp = 0


class VictoryRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!

        Victory is yours!
        """

    def modify_player(self, player):
        player.victory = True
