"""Describes the items in the game."""
__author__ = ['Phillip Johnson', 'Chad Wilson']

class Item(object):
    """The base class for all items"""
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return "{0}\n=====\n{1}\nValue: {2}\n".format(self.name, self.description, self.value)

# Inherits from Item class
class Gold(Item):
    def __init__(self, amount):
        self.amount = amount
        super(Gold, self).__init__(name="Gold", 
                         description="{0} shimmering gold coins.".format(str(self.amount)), 
                         value=self.amount)

    def add(self, amount):
        self.amount += amount
        self.description = "{0} shimmering gold coins.".format(str(self.amount))
        self.value = self.amount

class Weapon(Item):
    def __init__(self, name, description, value, damage):
        self.damage = damage
        super(Weapon, self).__init__(name, description, value)

    def __str__(self):
        return "{0}\n=====\n{1}\nValue: {2}\nDamage: {3}\n".format(self.name, self.description, self.value, self.damage)

class Rock(Weapon):
    def __init__(self):
        super(Rock, self).__init__(name="Rock", 
                         description="A fist-sized rock, suitable for bludgeoning.", 
                         value=0, 
                         damage=5 )


class Dagger(Weapon):
    def __init__(self):
        super(Dagger, self).__init__(name="Dagger",
                         description="A small dagger with some rust. Somewhat more dangerous than a rock.",
                         value=10,
                         damage=10 )


