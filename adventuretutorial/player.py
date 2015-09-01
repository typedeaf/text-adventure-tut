import random
import items, world

__author__ = ['Phillip Johnson', 'Chad Wilson']

class Player(object):
    global _max_x
    global _max_y

    def __init__(self):
        self.inventory = [items.Gold(15), items.Rock()]
        self.hp = 100
        self.location_x, self.location_y = (0, 0)
        self.victory = False
        self.map = [["?"*15 for i in range(world._max_x)] for j in range(world._max_y)]

    def is_alive(self):
        return self.hp > 0

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def print_inventory(self):
        print "{0:^40s}".format("-=( Inventory )=-")
        for item in self.inventory:
            print item

    def add_gold(self, amount):
        for i, j in enumerate(self.inventory):
            if isinstance(j, items.Gold):
                self.inventory[i].add(amount)
                
    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        self.map[self.location_y][self.location_x] = getattr(world._world[(self.location_x, self.location_y)], 'id')
        print world.tile_exists(self.location_x, self.location_y).intro_text()

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def view_map(self):
        print "{0:^60s}".format("-=( Dungeon Map )=-")
        for j in range(world._max_y):
            for i in range(world._max_x):
                if self.location_x == i and self.location_y == j:
                    print '[',self.map[j][i].center(16),']',
                else:
                    print self.map[j][i].center(20),
                    
            print ""

    def attack(self, enemy):
        best_weapon = None
        max_dmg = 0
        for i in self.inventory:
            if isinstance(i, items.Weapon):
                if i.damage > max_dmg:
                    max_dmg = i.damage
                    best_weapon = i

        print "You use {0} against {1}!".format(best_weapon.name, enemy.name)
        print "Your {0} does {1} damage to the {2}!".format(best_weapon.name, best_weapon.damage, enemy.name)
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print "You killed {0}!".format(enemy.name)
        else:
            print "{0} HP is {1}.".format(enemy.name, enemy.hp)

    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])

