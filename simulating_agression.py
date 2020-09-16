import random
import collections
import numpy as np
import matplotlib.pyplot as plt


class Area(object):
    """docstring for board."""
    def __init__(self, m, n, food):
        if food > (m*n):
            raise Exception("Too much food for this board!")

        self.m = m
        self.n = n
        self.food = food

        self.grid = [[0 for x in range(self.m)] for y in range(self.n)]

        food_loc = []
        for i in range(food):
            already_populated = True
            while already_populated:
                row = random.randrange(0, m)
                col = random.randrange(0, n)
                if self.grid[row][col] != 2:
                    self.grid[row][col] = 2
                    food_loc.append([row,col])
                    already_populated = False

        self.food_loc = food_loc


    def display_area(self):
        for row in self.grid:
            print(row)

class Dove(object):
    """docstring for dove."""
    def __init__(self, area):
        self.loc = random.choice(area.food_loc)
        self.food = 0
        self.type = "Dove"

    def get_info(self):
        return [self.loc, self.food, self.type]

    def display_info(self):
        info = self.get_info()
        print("Location: " + str(info[0]) + ", Food: " + str(info[1]) + ", Type: " + str(info[2]))

    def new_loc(self, area):
        self.loc = random.choice(area.food_loc)

    def set_food(self, amt):
        self.food = amt

    def add_food(self, amt):
        self.food += amt

    def remove_food(self, amt):
        self.food -= amt

class Hawk(object):
    """docstring for Hawk."""
    def __init__(self, area):
        self.loc = random.choice(area.food_loc)
        self.food = 0
        self.type = "Hawk"

    def get_info(self):
        return [self.loc, self.food, self.type]

    def display_info(self):
        info = self.get_info()
        print("Location: " + str(info[0]) + ", Food: " + str(info[1]) + ", Type: " + str(info[2]))

    def new_loc(self, area):
        self.loc = random.choice(area.food_loc)

    def set_food(self, amt):
        self.food = amt

    def add_food(self, amt):
        self.food += amt

    def remove_food(self, amt):
        self.food -= amt

def display_all_creatures(creature_lst):
    #print(creature_lst)
    num_doves = len([dove for dove in creature_lst if dove.get_info()[2] == "Dove"])
    num_hawks = len([hawk for hawk in creature_lst if hawk.get_info()[2] == "Hawk"])
    print("Num creatures: %d" % (len(creature_lst)))
    print("Num doves: %d" % (num_doves))
    print("Num hawks: %d" % (num_hawks))

    #for c in creature_lst:
        #c.display_info()
    return 0

def meeting(creature_lst, strategy):
    creature_lst.sort(key=lambda x: x.get_info()[2])
    creature_lst.reverse()

    if len(creature_lst) > 2:
        for i in creature_lst[2:-1]:
            i.set_food(0)

    creature1, creature2 = creature_lst[0], creature_lst[1]

    if creature1.get_info()[2] == "Dove" and creature2.get_info()[2] == "Dove":
        creature1.add_food(strategy[0][0])
        creature2.add_food(strategy[0][1])

    if creature1.get_info()[2] == "Dove" and creature2.get_info()[2] == "Hawk":
        creature1.add_food(strategy[1][0])
        creature2.add_food(strategy[1][1])

    if creature1.get_info()[2] == "Hawk" and creature2.get_info()[2] == "Dove":
        creature1.add_food(strategy[2][0])
        creature2.add_food(strategy[2][1])

    if creature1.get_info()[2] == "Hawk" and creature2.get_info()[2] == "Hawk":
        creature1.set_food(strategy[3][0])
        creature2.set_food(strategy[3][1])


def start_day(creature_lst, area):
    for creature in creature_lst:
        creature.new_loc(area)

    creature_locs = [(creature.get_info()[0][0], creature.get_info()[0][1]) for creature in creature_lst]

    loc_freq = {}
    for creature in creature_lst:
        curr = (creature.get_info()[0][0], creature.get_info()[0][1])
        if curr not in loc_freq:
            loc_freq[curr] = [creature]
        else:
            loc_freq[curr].append(creature)

    for loc in loc_freq:
        if len(loc_freq[loc]) > 1:
            meeting(loc_freq[loc], STRATEGY)
        else:
            loc_freq[loc][0].add_food(2)

    return creature_lst

"""
def end_day(creature_lst, area):
    new_lst = []
    for creature in creature_lst:
        creature_type = creature.type
        food_val = creature.food
        print("food_val: " + str(food_val))
        if food_val == .5:
            chance = random.choice([0,1])
            if chance == 0: new_lst.append(creature)
        if food_val == 1:
            new_lst.append(creature)
        if food_val == 1.5:
            new_lst.append(creature)
            chance = random.choice([0,1])
            if chance == 0:
                if creature_type == "Hawk":
                    new_lst.append(Hawk(area))
                else:
                    new_lst.append(Dove(area))
        if food_val == 2:
            new_lst.append(creature)
            if creature_type == "Hawk":
                new_lst.append(Hawk(area))
            else:
                new_lst.append(Dove(area))
    for creature in new_lst:
        creature.set_food(0)
    return new_lst
"""

def end_day(creature_lst, area):
    new_lst = []
    for creature in creature_lst:
        creature_type = creature.get_info()[2]
        food_val = creature.get_info()[1]
        if food_val < 1:
            food_val = food_val * 100
            chance = random.randint(0,100)
            if food_val >= chance: new_lst.append(creature)
        elif food_val == 1:
            new_lst.append(creature)
        elif food_val > 1:
            new_lst.append(creature)
            food_val = (food_val - 1) * 100
            chance = random.randint(0,100)
            if food_val >= chance:
                if creature_type == "Hawk":
                    new_lst.append(Hawk(area))
                else:
                    new_lst.append(Dove(area))
    for creature in new_lst:
        creature.set_food(0)
    return new_lst

def run(days, area, creatures):
    num_doves = []
    num_hawks = []
    for i in range(days):
        print("DAY %d" % (i))
        num_doves.append(len([dove for dove in creatures if dove.get_info()[2] == "Dove"]))
        num_hawks.append(len([hawk for hawk in creatures if hawk.get_info()[2] == "Hawk"]))
        if i == 10:
            creatures.append(Hawk(area))
        display_all_creatures(creatures)
        creatures = start_day(creatures, area)
        creatures = end_day(creatures, area)
    return num_doves, num_hawks


DAYS = 40
AREA_WIDTH = 15
AREA_LENGTH = 15
FOOD_PAIRS = 70
STARTING_DOVES = 5
STARTING_HAWKS = 0

#STRATEGY MATRIX
#       Dove  Hawk
#       ___________
# Dove | d,d | d,h |
#      |_____|_____|
# Hawk | h,d | h,h |
#      |_____|____ |

STRATEGY = [[1, 1], [0.5, 1.5], [1.5, 0.5], [0, 0]]

area = Area(AREA_WIDTH, AREA_LENGTH, FOOD_PAIRS)
creatures = [Dove(area) for i in range(STARTING_DOVES)] + [Hawk(area) for i in range(STARTING_HAWKS)]
result = run(DAYS, area, creatures)

x = range(DAYS)
y1, y2 = result

plt.stackplot(x, y1, y2, labels=['Doves','Hawks'], colors = ['#0c35a6', '#c40e0e'])
plt.legend(loc='upper left')
plt.ylabel('Num Creatures')
plt.xlabel('Days')

plt.show()
