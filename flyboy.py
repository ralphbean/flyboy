#!/usr/bin/env python
""" flyboy.py

A game written in the Python programming language.

Run it with::

    python flyboy.py

"""

import random
import sys
import uuid


WIDTH = 80
HEIGHT = 20

map = [[' ' for i in range(WIDTH)] for j in range(HEIGHT)]


class CollisionException(Exception):
    def __init__(self, object):
        self.object = object


class Object(object):
    """ This class represents any object in the game.

    More specific kinds of objects extend this class to make
    sub-classes, like Mob or Bullet.
    """

    # Here, every object must have a x and y location.  They are
    # set to "none" before the object is created.
    x = None
    y = None

    # Every object also has a character that represents it on the
    # screen.  Player is '*' and mobs are '+' for now.  Before
    # the object is created (instantiated), the character is
    # set briefly to "none".
    character = None

    def __init__(self, x, y, character):
        """ This is the initializer code for all objects.

        Just save the x, y, and character properties and
        remember to render (draw) the character on the map.
        """

        self.character = character
        self.x = x
        self.y = y
        self.render(x, y, character)

    @staticmethod
    def render(x, y, character):
        """ Rendering any object is easy.

        Just set the character in the map at the coordinates.
        """
        map[y][x] = character

    @staticmethod
    def detect_collision(x, y):
        """ Raise an exception if there is a collision
        at the (x, y) coordinates.
        """
        # Check every mob in existence
        for mob in mobs:
            # If its coordinates are equal to the coordinates given,
            if mob.x == x and mob.y == y:
                # Then raise an exception which halts this code path.
                raise CollisionException(object=mob)

    # Here follow the four movement methods for up, down, left, right.
    # Each are very similar, but slightly different.  Notice the
    # changes in coordinate handling.
    def move_up(self):
        # Check for out of bounds first.
        if self.y == 0:
            return
        # Check for collisions next.
        self.detect_collision(self.x, self.y - 1)

        # If both of those are fine, then go ahead and do the move which
        # takes three steps.

        # First - draw a blank at our old position.
        self.render(self.x, self.y, ' ')

        # Then, update our position.
        self.y = self.y - 1

        # Lastly, draw us again at the new position.
        self.render(self.x, self.y, self.character)

    # This method is just like move_up, except... slightly different.
    def move_down(self):
        if self.y == HEIGHT - 1:
            return
        self.detect_collision(self.x, self.y + 1)
        self.render(self.x, self.y, ' ')
        self.y = self.y + 1   # <-- see the difference here?
        self.render(self.x, self.y, self.character)

    def move_left(self):
        if self.x == 0:
            return
        self.detect_collision(self.x - 1, self.y)
        self.render(self.x, self.y, ' ')
        self.x = self.x - 1
        self.render(self.x, self.y, self.character)

    def move_right(self):
        if self.x == WIDTH - 1:
            return
        self.detect_collision(self.x + 1, self.y)
        self.render(self.x, self.y, ' ')
        self.x = self.x + 1
        self.render(self.x, self.y, self.character)

    # Here are the four fire methods.  Each of them also very
    # similar with a slight coordinate difference.
    # Notice how bullets have a position (self.x, and self.y) but
    # also a velocity (dx, and dy) which lets the bullet know
    # which direction it should be moving.
    def fire_up(self):
        mobs.append(Bullet(self.x, self.y-1, '"', dx=0, dy=1))

    def fire_down(self):
        mobs.append(Bullet(self.x, self.y+1, '"', dx=0, dy=-1))

    def fire_left(self):
        mobs.append(Bullet(self.x-1, self.y, '=', dx=-1, dy=0))

    def fire_right(self):
        mobs.append(Bullet(self.x+1, self.y, '=', dx=1, dy=0))

    def move(self):
        raise NotImplementedError("Base objects don't move on their own.")


class Mob(Object):
    """ This class represents any Mob (bad guys, in our game).

    It is just like any other object, except it has a 'move' method
    that defines how bad guys should move and shoot.
    """
    def __init__(self, *args, **kwargs):
        super(Mob, self).__init__(*args, **kwargs)
        self.name = "Mob %s" % uuid.uuid4()

    def __str__(self):
        return self.name

    def move(self):
        # First, roll a dice and if a certain combination comes up,
        # then move randomly to give the bad guys some unpredictability.
        if random.random() < 0.1:
            return self.move_left()
        elif random.random() < 0.1:
            return self.move_right()
        elif random.random() < 0.1:
            return self.move_up()
        elif random.random() < 0.1:
            return self.move_down()

        # Then, if the bad guy is not in line with the player, try to
        # move in line to get a good shot -- horizontally.
        direction = player.x - self.x
        if direction < 0:
            if random.random() < 0.4:
                return self.move_left()
            elif random.random() < 0.4:
                return self.fire_left()
        elif direction > 0:
            if random.random() < 0.4:
                return self.move_right()
            elif random.random() < 0.4:
                return self.fire_right()

        # Then, do the same thing vertically!
        direction = player.y - self.y
        if direction < 0:
            if random.random() < 0.4:
                return self.move_up()
            elif random.random() < 0.4:
                return self.fire_up()
        elif direction > 0:
            if random.random() < 0.4:
                return self.move_down()
            elif random.random() < 0.4:
                return self.fire_down()


class Bullet(Object):
    """ This is our bullet.  It is an object that moves
    much more simply than Mobs.  Just in a straight line.
    """

    def __init__(self, x, y, character, dx, dy):
        """ A simple initializer method for bullets.  They initialize
        just like objects, except they *also* have to remember which
        way they are going (dx, dy).

        *Note: the 'd' in 'dx' stands for 'delta' which is the greek letter
               that we often use to mean "difference" in science and math.
               Understand it here to mean the regular difference in x and
               the regular difference in y that the bullet should be
               experiencing.

               Having dx=1 and dy=0 means that the bullet will be moving
               in the x direction, but not in the y direction.

               Having dx=0 and dy=-1 means that the bullet will be moving down.
        """

        super(Bullet, self).__init__(x, y, character)
        self.dx = dx
        self.dy = dy

    def move(self):
        """ Bullets move simply.  See the self.dy and self.dx handling?

        But, they have to detect if they collide with stuff.
        """

        try:
            if self.dy == 1:
                self.move_up()
            if self.dy == -1:
                self.move_down()
            if self.dx == 1:
                self.move_right()
            if self.dx == -1:
                self.move_left()
        except CollisionException as exception:
            # If a bullet collided with *anything*, handle it here.
            # Here, "object" is the thing that got hit.
            object = exception.object

            # First, delete it from the drawn map
            object.render(object.x, object.y, ' ')

            # If it is the player, then handle this special case.
            if object == player:
                print("You died.")
                sys.exit(0)

            print("%s died." % str(object))
            # Then, remove it from the list of things that move.
            if object in mobs:
                mobs.remove(object)


def display():
    """ Printing the map out is easy. """
    for row in map:
        print(''.join(row))


def handle_win_condition():
    # If none of the moving things are bad guys now, then we win.
    if not any([type(mob) == Mob for mob in mobs]):
        print("You win!")
        sys.exit(0)


def handle_input():
    key = raw_input("What is your move? [wasd]")

    try:
        if key == 'w':
            player.move_up()
        if key == 'a':
            player.move_left()
        if key == 'd':
            player.move_right()
        if key == 's':
            player.move_down()
    except CollisionException:
        pass

    if key == 'W':
        player.fire_up()
    if key == 'A':
        player.fire_left()
    if key == 'D':
        player.fire_right()
    if key == 'S':
        player.fire_down()


def handle_mobs():
    # For all the mobs in the game.
    for mob in mobs:
        try:
            # Have them decide how they should move.
            mob.move()
        except CollisionException:
            # If a mob tries to move into another mob or bullet, then ignore it
            pass


# Now, with all that code declared.  Define our starting objects.
# A player, and a few mobs.
player = Object(10, 10, '*')
mobs = [
    Mob(random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1), '+')
    for i in range(13)]

# SEE HERE - this is the "main loop" of the program.
# All the stuff above just defines things to be used in the game.
# The game itself just boils down to this loop here.
while True:
    display()  # Draw the map every time.
    handle_win_condition()  # Did we win yet?  Probably not.
    handle_input()
    handle_mobs()
