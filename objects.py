import random
from animate import *


class Place:
    """A Place holds insects and has an exit to another Place."""
    is_hive = False
    is_anthome = False

    def __init__(self, x=-100, y=-100, exit_=None):
        """Create a Place with the given EXIT.
        exit -- The Place reached by exiting this Place (maybe None).
        """
        self.exit = exit_
        self.bees = []        # A list of Bees
        self.x = x
        self.y = y
        self.ant = None       # An Ant
        self.entrance = None  # A Place
        # Phase 1: Add an entrance to the exit
        # BEGIN Problem 2
        if self.exit is not None:
            self.exit.entrance = self
        # END Problem 2

    def add_insect(self, insect):
        """
        Asks the insect to add itself to the current place. This method exists so
            it can be enhanced in subclasses.
        """
        insect.add_to(self)

    def remove_insect(self, insect):
        """
        Asks the insect to remove itself from the current place. This method exists so
            it can be enhanced in subclasses.
        """
        insect.remove_from(self)


class Water(Place):
    """Water is a place that can only hold waterproof insects."""

    def add_insect(self, insect):
        """Add an Insect to this place. If the insect is not waterproof, reduce
        its health to 0."""
        super().add_insect(insect)
        if insect.is_waterproof:
            insect.reduce_health(insect.health)


class AntHomeBase(Place):
    """AntHomeBase at the end of the tunnel, where the queen resides."""
    is_anthome = True


class BeeHive:
    """BeeHive at the start of the tunnel, where ants resides."""
    is_hive = True

    def __init__(self, x=-1, y=-1, exit=None):
        """Create a Place with the given EXIT.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.exit = []
        self.bees = []        # A list of Bees
        self.x = x
        self.y = y
        self.ant = None       # An Ant
        self.entrance = None  # A Place

    def add_insect(self, insect):
        """
        Asks the insect to add itself to the current place. This method exists so
            it can be enhanced in subclasses.
        """
        insect.add_to(self)

    def remove_insect(self, insect):
        """
        Asks the insect to remove itself from the current place. This method exists so
            it can be enhanced in subclasses.
        """
        insect.remove_from(self)


class Insect:
    """An Insect, the base class of Ant and Bee, has health and a Place."""

    damage = 0
    name = ""
    is_waterproof = False
    # ADD CLASS ATTRIBUTES HERE

    def __init__(self, health, place=None):
        """Create an Insect with a health amount and a starting PLACE."""
        self.health = health
        self.place = place

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the insect from its place if it
        has no health remaining

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_health(2)
        >>> test_insect.health
        3
        """
        self.health -= amount
        if self.health <= 0:
            self.death_callback()
            self.place.remove_insect(self)

    def action(self, gamestate):
        """The action performed each turn.

        gamestate -- The GameState, used to access game state information.
        """

    def death_callback(self):
        pass

    def add_to(self, place):
        """Add this Insect to the given Place

        By default just sets the place attribute, but this should be overriden in the subclasses
            to manipulate the relevant attributes of Place
        """
        self.place = place

    def remove_from(self, place):
        self.place = None

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.health, self.place)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    implemented = False  # Only implemented Ant classes should be instantiated
    food_cost = 0
    is_container = False
    doubled = False
    blocks_path = True
    # ADD CLASS ATTRIBUTES HERE

    def __init__(self, health=2):
        """Create an Insect with a HEALTH quantity."""
        super().__init__(health)

    @classmethod
    def construct(cls, gamestate):
        """Create an Ant for a given GameState, or return None if not possible."""
        if cls.food_cost > gamestate.food:
            print('Not enough food remains to place ' + cls.__name__)
            return
        return cls()

    def can_contain(self, other):
        return False

    def store_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def remove_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def add_to(self, place):
        if place.ant is None:
            place.ant = self
        else:
            if place.ant.is_container and place.ant.can_contain(self):
                place.ant.store_ant(self)
            elif self.is_container and self.can_contain(place.ant):
                self.store_ant(place.ant)
                place.ant = self
            else:
                if place.ant is not None:
                    return
        Insect.add_to(self, place)

    def remove_from(self, place):
        if place.ant is self:
            place.ant = None
        elif place.ant is None:
            assert False, '{0} is not in {1}'.format(self, place)
        else:
            place.ant.remove_ant(self)
        Insect.remove_from(self, place)

    def double(self):
        """Double this ants's damage, if it has not already been doubled."""
        if self.doubled:
            self.damage *= 2
            self.doubled = True
        if self.is_container and self.ant_contained is not None and not self.ant_contained.doubled:
            self.ant_contained.double()


class HarvesterAnt(Ant):
    """HarvesterAnt produces 2 additional food every 4
     turns for the colony."""

    name = 'harvester'
    implemented = True
    food_cost = 2

    def action(self, gamestate):
        """Produce 2 additional food for the colony.

        gamestate -- The GameState, used to access game state information.
        """
        # BEGIN Problem 1
        if gamestate.time % 3 == 0:
            gamestate.food += 2
        elif gamestate.time % 3 == 2:
            gamestate.leafs.append(Leaf([self.place.x, self.place.y], [70, 950], "food", 20))
        # END Problem 1


class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = 'thrower'
    implemented = True
    damage = 1
    food_cost = 3
    lower_bound = 0
    upper_bound = float('inf')

    def nearest_bee(self):
        """Return the nearest Bee in a Place that is not the HIVE, connected to
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).
        """
        p0 = self.place
        length = 0
        while (len(p0.bees) == 0 or length < self.lower_bound or length > self.upper_bound) and p0.is_hive is False:
            p0 = p0.entrance
            length += 1
        if p0.is_hive is False:
            return random_bee(p0.bees)
        else:
            return None

    def throw_at(self, target):
        """Throw a leaf at the TARGET Bee, reducing its health."""
        if target is not None:
            target.reduce_health(self.damage)

    def action(self, gamestate):
        """Throw a leaf at the nearest Bee in range."""
        target = self.nearest_bee()
        if target is not None:
            gamestate.leafs.append(Leaf([self.place.x, self.place.y], [target.x, target.y], "common"))
        self.throw_at(target)



def random_bee(bees):
    """Return a random bee from a list of bees, or return None if bees is empty."""
    assert isinstance(bees, list), "random_bee's argument should be a list but was a %s" % type(bees).__name__
    if bees:
        return random.choice(bees)


class ShortThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at most 3 places away."""

    name = 'shortthrower'
    food_cost = 2
    upper_bound = 3
    implemented = True


class LongThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at least 5 places away."""

    name = 'longthrower'
    food_cost = 2
    lower_bound = 5
    implemented = True


class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires."""

    name = 'fire'
    damage = 3
    food_cost = 5
    implemented = True

    def __init__(self, health=5):
        """Create an Ant with a HEALTH quantity."""
        super().__init__(health)

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the FireAnt from its place if it
        has no health remaining.

        Make sure to reduce the health of each bee in the current place, and apply
        the additional damage if the fire ant dies.
        """
        all_bees = list(self.place.bees)
        if self.health <= amount:
            for b in all_bees:
                b.reduce_health(self.damage + amount)
        else:
            for b in all_bees:
                b.reduce_health(amount)
        super().reduce_health(amount)

    def action(self, gamestate):
        if self.health > len(self.place.bees) > 0:
            gamestate.effects.append(Effect("fire0", [self.place.x, self.place.y]))
        elif self.health == len(self.place.bees):
            gamestate.effects.append(Effect("explode", [self.place.x, self.place.y]))


class WallAnt(Ant):
    name = 'wall'
    food_cost = 4
    implemented = True

    def __init__(self, health=6):
        super().__init__(health)


class HungryAnt(Ant):
    name = 'hungry'
    food_cost = 4
    chewing_turns = 3
    implemented = True

    def __init__(self, turns_to_chew=0, health=3):
        self.turns_to_chew = turns_to_chew
        super().__init__(health)

    def action(self, gamestate):
        if self.turns_to_chew == 0:
            if len(self.place.bees) > 0:
                gamestate.effects.append(Effect("hungry", [self.place.x, self.place.y]))
                b = random.choice(self.place.bees)
                b.reduce_health(b.health)
                self.turns_to_chew = HungryAnt.chewing_turns
        else:
            self.turns_to_chew -= 1


class ContainerAnt(Ant):
    """
    ContainerAnt can share a space with other ants by containing them.
    """
    is_container = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ant_contained = None

    def can_contain(self, other):
        return other.is_container is False and self.ant_contained is None

    def store_ant(self, ant):
        self.ant_contained = ant

    def remove_ant(self, ant):
        if self.ant_contained is not ant:
            assert False, "{} does not contain {}".format(self, ant)
        self.ant_contained = None

    def remove_from(self, place):
        # Special handling for container ants
        if place.ant is self:
            # Container was removed. Contained ant should remain in the game
            place.ant = place.ant.ant_contained
            Insect.remove_from(self, place)
        else:
            # default to normal behavior
            Ant.remove_from(self, place)

    def action(self, gamestate):
        if self.ant_contained is not None:
            self.ant_contained.action(gamestate)


class BodyguardAnt(ContainerAnt):
    """BodyguardAnt provides protection to other Ants."""

    name = 'bodyguard'
    food_cost = 4

    implemented = True

    def __init__(self, health=2):
        super().__init__(health)


class TankAnt(ContainerAnt):
    name = 'tank'
    food_cost = 6
    damage = 1
    implemented = True

    def __init__(self, health=3):
        super().__init__(health)

    def action(self, gamestate):
        if self.ant_contained is not None:
            self.ant_contained.action(gamestate)
        if self.place is not None and len(self.place.bees) > 0:
            b = list(self.place.bees)
            for b0 in b:
                b0.reduce_health(self.damage)


class ScubaThrower(ThrowerAnt):
    name = 'scuba'
    food_cost = 6
    is_waterproof = True
    implemented = True


class QueenAnt(ScubaThrower):
    """The Queen of the colony. The game is over if a bee enters her place."""

    name = 'queen'
    food_cost = 7
    implemented = True

    @classmethod
    def construct(cls, gamestate):
        """
        Returns a new instance of the Ant class if it is possible to construct, or
        returns None otherwise. Remember to call the construct() method of the superclass!
        """
        if gamestate.queen_num == 0:
            gamestate.queen_num += 1
            return super().construct(gamestate)
        else:
            return

    def action(self, gamestate):
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.
        """
        target = self.nearest_bee()
        if target is not None:
            gamestate.leafs.append(Leaf([self.place.x, self.place.y], [target.x, target.y], "queen"))
        self.throw_at(target)
        plc = self.place
        while plc.exit is not None:
            plc = plc.exit
            if plc.ant is not None:
                plc.ant.double()


class NinjaAnt(Ant):
    """NinjaAnt does not block the path and damages all bees in its place.
    This class is optional.
    """
    name = 'ninja'
    damage = 1
    food_cost = 5
    blocks_path = False
    implemented = True

    def action(self, gamestate):
        all_bees = list(self.place.bees)
        if len(self.place.bees) > 0:
            gamestate.effects.append(Effect("ninja", [self.place.x, self.place.y]))
        for b in all_bees:
            b.reduce_health(self.damage)


def make_slow(bee, action):
    """Return a new action method that calls ACTION every other turn.
    action -- An action method of some Bee
    """
    def new_action(bee, colony):
        if colony.time % 2 == 0:
            bee.action(colony)
    return lambda g: new_action(bee, g)


def apply_effect(effect, bee, duration):
    """Apply a status effect to a BEE that lasts for DURATION turns."""
    origin_action = bee.action
    new_action = effect(bee, bee.action)

    def action(colony):
        nonlocal duration
        if duration == 0:
            return origin_action(colony)
        else:
            duration -= 1
            return new_action(colony)

    bee.action = action


class SlowThrower(ThrowerAnt):
    """ThrowerAnt that causes Slow on Bees."""

    name = 'slow'
    food_cost = 6
    implemented = True

    def throw_at(self, target):
        if target:
            apply_effect(make_slow, target, 5)

    def action(self, gamestate):
        """Throw a leaf at the nearest Bee in range."""
        target = self.nearest_bee()
        if target is not None:
            gamestate.leafs.append(Leaf([self.place.x, self.place.y], [target.x, target.y], "cold"))
        self.throw_at(target)


class LaserAnt(ThrowerAnt):
    name = 'laser'
    food_cost = 10
    damage = 5
    implemented = True

    def __init__(self, health=3):
        super().__init__(health)
        self.insects_shot = 0

    def insects_in_front(self):
        dic, dist = {}, 0
        if self.place.ant.is_container:
            dic[self.place.ant] = dist
        place = self.place
        for b in place.bees:
            dic[b] = dist
        while place.entrance.is_hive:
            dist += 1
            place = place.entrance
            if place.ant is not None:
                dic[place.ant] = dist
                if place.ant.is_container and place.ant.ant_contained is not None:
                    dic[place.ant.ant_contained] = dist
            for b in place.bees:
                dic[b] = dist
        return dic

    def calculate_damage(self, distance):
        return self.damage - 0.25 * distance - 0.0625 * self.insects_shot

    def action(self, gamestate):
        insects_and_distances = self.insects_in_front()
        for insect, distance in insects_and_distances.items():
            damage = self.calculate_damage(distance)
            insect.reduce_health(damage)
            if damage:
                self.insects_shot += 1
        gamestate.leafs.append(Leaf([self.place.x, self.place.y], [self.place.x, gamestate.yindex[-1]], "laser"))



class AntRemover(Ant):
    """Allows the player to remove ants from the board in the GUI."""

    name = 'remover'
    implemented = True

    def __init__(self):
        super().__init__(0)


class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants."""

    name = 'bee'
    damage = 1
    is_waterproof = True
    blocks_path = False

    def __init__(self, x, y, health=6):
        """Create an Insect with a HEALTH quantity."""
        super().__init__(health)
        self.x = x
        self.y = y
        self.endx = x
        self.endy = y

    def sting(self, ant):
        """Attack an ANT, reducing its health by 1."""
        ant.reduce_health(self.damage)

    def move_to(self, place):
        """Move from the Bee's current Place to a new PLACE."""
        self.place.remove_insect(self)
        self.endx = place.x
        self.endy = place.y
        place.add_insect(self)

    def blocked(self):
        """Return True if this Bee cannot advance to the next Place."""
        # Special handling for NinjaAnt
        return self.place.ant is not None and self.place.ant.blocks_path is True

    def action(self, gamestate):
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.

        gamestate -- The GameState, used to access game state information.
        """
        destination = self.place.exit
        if self.blocked():
            if self.place.ant.health - self.damage <= 0 and self.place.ant.name == "queen":
                gamestate.gamemode = 3
            self.sting(self.place.ant)
        elif self.health > 0 and destination is not None:
            self.move_to(destination)
            if destination.is_anthome:
                gamestate.gamemode = 3

    def add_to(self, place):
        place.bees.append(self)
        Insect.add_to(self, place)

    def remove_from(self, place):
        place.bees.remove(self)
        Insect.remove_from(self, place)

    def update(self):
        if self.endx == self.x and self.endy == self.y:
            return
        distance = math.sqrt((self.endx - self.x) ** 2 + (self.endy - self.y) ** 2)
        direction = ((self.endx - self.x) / distance, (self.endy - self.y) / distance)
        speed = 18
        self.x += direction[0] * speed
        self.y += direction[1] * speed
        if math.sqrt((self.x - self.endx)**2 + (self.y - self.endy)**2) <= speed:
            self.x = self.endx
            self.y = self.endy


def ants_win():
    """Signal that Ants win."""
    raise AntsWinException()


def ants_lose():
    """Signal that Ants lose."""
    raise AntsLoseException()


class GameOverException(Exception):
    """Base game over Exception."""
    pass


class AntsWinException(GameOverException):
    """Exception to signal that the ants win."""
    pass


class AntsLoseException(GameOverException):
    """Exception to signal that the ants lose."""
    pass


class Leaf:
    def __init__(self, start, end, type, speed=12):
        self.current = start
        self.end = end
        self.type = type
        self.speed = speed

    def update(self):
        if self.current == self.end:
            return
        distance = math.sqrt((self.end[0] - self.current[0]) ** 2 + (self.end[1] - self.current[1]) ** 2)
        direction = ((self.end[0] - self.current[0]) / distance, (self.end[1] - self.current[1]) / distance)
        self.current[0] += direction[0] * self.speed
        self.current[1] += direction[1] * self.speed
        if math.sqrt((self.current[0] - self.end[0]) ** 2 + (self.current[1] - self.end[1]) ** 2) <= self.speed:
            self.current = self.end


class Effect:
    def __init__(self, type, position, time=30):
        self.type = type
        self.time = time
        self.position = position

    def update(self):
        if self.time > 0:
            self.time -= 1
        if self.time % 5 == 0:
            if self.type == "fire0":
                self.type = "fire1"
            elif self.type == "fire1":
                self.type = "fire0"


class GameState:
    """An ant collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    ... ...
    """

    def __init__(self, ant_types, xindex, yindex, beexindex, beenum, dic):
        """Create an GameState for a game.

        Arguments:
        beehive -- a Hive full of bees
        ant_types -- a list of ant classes
        create_places -- a function that creates the set of places
        dimensions -- a pair containing the dimensions of the game layout
        ... ...
        """
        self.time = 0
        self.gamemode = 1   # 1 running 2 win 3 lost
        self.food = 2
        self.beehive = BeeHive()
        self.activebees = []
        self.ant_types = ant_types
        self.dimensions = (10, 5, 6)
        self.places = []
        self.queen_num = 0
        self.xindex = xindex
        self.yindex = yindex
        self.beexindex = beexindex
        self.anthome = AntHomeBase()
        self.fadingobjects = FadingObjects()
        self.attackdict = dic
        self.leafs = []
        self.effects = []
        for i in range(self.dimensions[1]):
            row, lastplace = [], self.anthome
            for j in range(self.dimensions[0]):
                newplace = Place(self.xindex[i] + 15, self.yindex[j], lastplace)
                lastplace.entrance = newplace
                row.append(newplace)
                lastplace = newplace
            lastplace.entrance = self.beehive
            self.beehive.exit.append(lastplace)
            self.places.append(row)
        for x in self.xindex:
            for y in self.beexindex:
                newbee = Bee(x, y)
                self.beehive.add_insect(newbee)

    def add_ants(self, x, y, ant):
        if self.food < ant.food_cost:
            return
        if (self.places[x][y].ant is not None and not self.places[x][y].ant.can_contain(ant) and
                not ant.can_contain(self.places[x][y].ant)):
            return
        if ant.name == 'queen' and self.queen_num == 0:
            self.queen_num = 1
        elif ant.name == 'queen':
            return
        self.food -= ant.food_cost
        self.places[x][y].add_insect(ant)

    def remove_ants(self, x, y):
        self.places[x][y].ant = None

    def loop(self):
        self.time += 1
        if self.time % 5 == 0:
            self.food += 1
        for row in self.places:
            for place in row:
                if place.ant is not None:
                    place.ant.action(self)
        for row in self.places:
            for place in row:
                for bee in place.bees:
                    bee.action(self)
        beenum = self.attackdict.get(self.time)
        if (beenum is not None and
                beenum > len(self.beehive.bees)):
            for x in self.xindex:
                for y in self.beexindex:
                    newbee = Bee(x, y)
                    self.beehive.add_insect(newbee)
        availableplace = [p[-1] for p in self.places]
        while beenum:
            if not availableplace:
                availableplace = [p[-1] for p in self.places]
            p = random.choice(availableplace)
            self.beehive.bees[0].endx = p.x
            self.beehive.bees[0].endy = p.y
            self.activebees.append(self.beehive.bees[0])
            self.beehive.bees[0].move_to(p)
            availableplace.remove(p)
            beenum -= 1
        if len(self.beehive.bees) + len(self.activebees) == 0:
            self.gamemode = 2
