"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _right: Determines whether aliens should continue moving right
    # Invariant: _right: is a boolean
    #
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    #Update Aliens
    def get_Alien_Image(self,row):
        """
        Returns the image index for a given row of aliens

        Parameter row: the row number of aliens
        Precondition: row is an int >= 0
        """
        #If modulo 3 and 4, 1 image
        num_images = len(ALIEN_IMAGES)
        new_row = row % num_images
        return ALIEN_IMAGES[new_row]

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS

    def __init__(self,width,height):
        """
        make wave of aliens
        """

        num_images = 1
        index = 0
        self._aliens = []
        for row in range(ALIEN_ROWS):
            alien_row = []
            num_images = num_images - 1
            for col in range(ALIENS_IN_ROW):
                x = col * (ALIEN_WIDTH + ALIEN_H_SEP) + ALIEN_WIDTH
                y = height - (ALIEN_CEILING + row * (ALIEN_HEIGHT + ALIEN_V_SEP))
                image = ALIEN_IMAGES[index]
                alien = Alien(x=x, y=y, width = ALIEN_WIDTH, height = ALIEN_HEIGHT, source=image)
                alien_row.append(alien)
            self._aliens.append(alien_row)
            if num_images == 0:
                num_images = 2
                index = index + 1
                if index == len(ALIEN_IMAGES):
                    index = 0

        self._bolts = []
        #bolt = Bolt(x=GAME_WIDTH//2, y=SHIP_BOTTOM+20, width=BOLT_WIDTH, height=BOLT_HEIGHT, fillcolor='black', linewidth=2, linecolor='black')
        self._ship = Ship(x=GAME_WIDTH//2, y=SHIP_BOTTOM, width=SHIP_WIDTH, height=SHIP_HEIGHT, source=SHIP_IMAGE)
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE], linewidth=2, linecolor='black')
        self._time = 0.0
        self._right = True

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):
        """
        update to move ship, aliens, laser bolts
        """
        self.ship_movement(input,dt)
        self.move_aliens(dt)
        #self.fire_bolts(input)

        #if self._time > ALIEN_SPEED:
        #    for row in self._aliens:
        #        for alien in row:
        #            alien.x = alien.x + ALIEN_H_WALK
        #    self._time = 0.0
        #self._time = self._time + dt

    def ship_movement(self, input, dt):
        if input.is_key_down('left'):
            if self._ship.x < 35:
                input.is_key_down('left') == False
            else:
                self._ship.x = self._ship.x-SHIP_MOVEMENT
                for bolt in self._bolts:
                    bolt.x = self._ship.x
                    bolt.y += bolt.getVelocity()
        elif input.is_key_down('right'):
            if self._ship.x > GAME_WIDTH - 35:
                input.is_key_down('right') == False
            else:
                self._ship.x = self._ship.x+SHIP_MOVEMENT
                for bolt in self._bolts:
                    bolt.x = self._ship.x
                    bolt.y = bolt.y + models.self.getVelocity()


    def move_aliens(self,dt):
        movement = True
        self._time += dt

        if self._time > ALIEN_SPEED:
            #for row in self._aliens:
            #    for alien in row:
            #        if row[-1].x > (GAME_WIDTH - ALIEN_H_SEP):
            if self._aliens[0][-1].x > (GAME_WIDTH - ALIEN_H_SEP):
                self._right = False
                self.alien_down(dt)
            elif self._aliens[0][0].x < ALIEN_H_SEP:
                self._right
                self.alien_down(dt)
                self.alien_left(dt)
            if self._right:
                self.alien_right(dt)
            else:
                self.alien_left(dt)

            self._time = 0.0
        self._time += dt

    def alien_left(self,dt):
        for row in self._aliens:
            for alien in row:
                alien.x = alien.x - ALIEN_H_WALK

    def alien_right(self,dt):
        for row in self._aliens:
            for alien in row:
                alien.x = alien.x + ALIEN_H_WALK
    def alien_down(self,dt):
        for row in self._aliens:
            for alien in row:
                alien.y = alien.y - ALIEN_V_WALK
    #def fire_bolts(self,input):
        #if input.is_key_pressed('up'):
        #    bolt = Bolt(x=self._ship.x, y=SHIP_BOTTOM+27, width=BOLT_WIDTH, height=BOLT_HEIGHT, fillcolor='white', linewidth=1, linecolor='black')
        #    self._bolts.append(bolt)


    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        draws stuff
        """
        #view = self._aliens
        for row in self._aliens:
            for alien in row:
                alien.draw(view)
        self._ship.draw(view)
        self._dline.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
