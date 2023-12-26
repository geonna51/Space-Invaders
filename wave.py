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
    # Attribute _right: determines if alien wave should move right or not
    # Invariant: _right is a boolean
    #
    # Attribute _random: determines random player bolt rate of fire
    # Invariant: _random is an int between 1 and BOLT_RATE, inclusive
    #
    # Attribute _step: the number of alien steps taken since last alien-fired bolt
    # Invariant: _step is an int >= 0
    #
    # Attribute _won: determines if the player has won the game
    # Invariant: _won is a boolean
    #
    # Attribute _lost: determines if the player has lost the game
    # Invariant: _lost is a boolean

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLives(self):
        """
        Returns the number of player lives left.
        """
        return self._lives

    def getWon(self):
        """
        Returns the game state by checking if the player has won the game.
        """
        return self._won

    def getLost(self):
        """
        Returns the game state by checking if the player has lost the game.
        """
        return self._lost

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self, width, height):
        """
        Initializes the Alien Invaders game with all its attributes.

        The alien wave, ship, defense line are created.
        The ship appears on the left side of the screen and the ship appears
        in the lower center of the screen.

        Parameter width: the game width
        Precondition: width is GAME_WIDTH

        Parameter height: the game height
        Precondtion: height is GAME_HEIGHT
        """
        assert width == GAME_WIDTH and height == GAME_HEIGHT
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
                alien = Alien(x=x, y=y, width = ALIEN_WIDTH, \
                height = ALIEN_HEIGHT, source=image)
                alien_row.append(alien)
            self._aliens.append(alien_row)
            if num_images == 0:
                num_images = 2
                index = index + 1
                if index == len(ALIEN_IMAGES):
                    index = 0
        self._bolts = []
        self._ship = Ship(x=GAME_WIDTH//2, y=SHIP_BOTTOM, width=SHIP_WIDTH, \
        height=SHIP_HEIGHT, source=SHIP_IMAGE)
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE], \
        linewidth=2, linecolor='black')
        self._time = 0.0
        self._right = True
        self._random = random.randint(1,BOLT_RATE)
        self._step = 0
        self._lives = 3
        self._won, self._lost = False, False

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, input, dt):
        """
        Determines the current game state and runs the animation if the
        game state is active.

        When the spacebar is clicked, the ship fires a bolt.

        If the alien wave is at or below the defense line, the game ends.

        Parameter input: responds to keyboard events
        Precondition: input is an instance of GInput

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(input, GInput)
        assert isinstance(dt, int) or isinstance(dt, float)
        self.ship_movement(input,dt)
        self.bolt_movement(input,dt)
        self.move_aliens(dt)
        self.remove_offscreen_bolts()
        self.check_collision()
        if input.is_key_pressed('spacebar'):
            if not self._ship is None and not self.has_player_bolt():
                bolt = Bolt(x=self._ship.x, y=SHIP_BOTTOM+27, \
                width=BOLT_WIDTH, height=BOLT_HEIGHT, fillcolor='white', \
                linewidth=1, linecolor='black', pos=True)
                self._bolts.append(bolt)
        if self._step == self._random:
            chosen_alien = self.choose_alien()
            if chosen_alien is not None:
                bolt = Bolt(x = chosen_alien.x, y = chosen_alien.y,\
                width = BOLT_WIDTH, height = BOLT_HEIGHT, fillcolor = 'black',\
                linewidth =1, linecolor =
                 'black', pos = False)
                self._bolts.append(bolt)
            self._random, self._step = random.randint(1, BOLT_RATE), 0
            is_none = False
    # HELPER METHODS FOR UPDATE
    def ship_movement(self, input, dt):
        """
        Moves the ship left when the player holds down the left arrow key.
        Moves the ship right when the player holds down the right arrow key.

        Parameter input: responds to keyboard events
        Precondition: input is an instance of GInput

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(input, GInput)
        assert isinstance(dt, int) or isinstance(dt, float)

        if input.is_key_down('left'):
            if not self._ship is None and self._ship.x < 35:
                input.is_key_down('left') == False
            else:
                if not self._ship is None:
                    self._ship.x = self._ship.x-SHIP_MOVEMENT
        elif input.is_key_down('right'):
            if not self._ship is None and self._ship.x > GAME_WIDTH - 35:
                input.is_key_down('right') == False
            else:
                if not self._ship is None:
                    self._ship.x = self._ship.x+SHIP_MOVEMENT

    def bolt_movement(self, input, dt):
        """
        Moves the bolt vertically (either up or down) when a bolt is fired by
        an alien or the ship.

        Parameter input: responds to keyboard events
        Precondition: input is an instance of GInput

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(input, GInput)
        assert isinstance(dt, int) or isinstance(dt, float)

        for bolt in self._bolts:
            bolt.y = bolt.y + bolt.getVelocity()

    def move_aliens(self, dt):
        """
        Controls all alien wave left, right and downwards movement.

        If the rightmost alien column is at the game border, the waves moves down and
        continues leftward. If the leftmost alien column is at the game border,
        the wave moves down and continues rightward.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(dt, int) or isinstance(dt, float)
        if all(all(alien is None for alien in row) for row in self._aliens):
            self._won = True
            return 
        if self._time > ALIEN_SPEED:
            if self._right:
                self.alien_right(dt)
                self._step = self._step + 1
            else:
                self.alien_left(dt)
                self._step = self._step + 1
            y, pos = 0, -1
            if self._aliens[0][pos] is None:
                while self._aliens[0][pos] is None:
                    pos = pos - 1
            if self._aliens[y][pos] is None:
                y = y + 1
            if self._aliens[y][pos].x > \
            (GAME_WIDTH - ALIEN_H_SEP - SHIP_WIDTH//2):
                self.alien_left(dt)
                self.alien_down(dt)
                self._right = False
            pos = 0
            if self._aliens[0][pos] is None:
                while self._aliens[0][pos] is None:
                    pos = pos + 1
            if self._aliens[y][pos] is None:
                y = y + 1
            if self._aliens[y][pos].x < (ALIEN_H_SEP + SHIP_WIDTH//2):
                self.alien_right(dt)
                self.alien_down(dt)
                self._right = True
            self._time = 0.0
        self._time = self._time + dt

    def alien_left(self,dt):
        """
        Moves alien wave leftwards

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(dt, int) or isinstance(dt, float)

        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    alien.x = alien.x - ALIEN_H_WALK

    def alien_right(self,dt):
        """
        Moves alien wave rightwards

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(dt, int) or isinstance(dt, float)

        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    alien.x = alien.x + ALIEN_H_WALK

    def alien_down(self,dt):
        """
        Moves alien wave downwards

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(dt, int) or isinstance(dt, float)

        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    alien.y = alien.y - ALIEN_V_WALK

    def find_bot_row(self):
        """
        Returns the row closest to the defense line in the alien wave.
        Does not include empty rows.
        """
        pos = -1
        bottom_row = self._aliens[pos]
        if all(elem is None for elem in bottom_row):
            while all(elem is None for elem in bottom_row):
                pos = pos - 1
                bottom_row = self._aliens[pos]
        return bottom_row

    def choose_alien(self):
        """
        Returns a randomly chosen alien in the bottom row.
        """
        bottom_row = self.find_bot_row()
        col = random.randint(0, len(bottom_row) - 1)
        y = self._aliens.index(bottom_row)
        while y >= 0 and self._aliens[y][col] is None:
            y -= 1
        if y<0:
            return None
        return self._aliens[y][col]

    def remove_offscreen_bolts(self):
        """
        Removes bolts that exit the game screen from the list of bolts.
        """
        self._bolts = [bolt for bolt in self._bolts
               if (bolt.y - BOLT_HEIGHT // 2) <= GAME_HEIGHT]

    def has_player_bolt(self):
        """
        Returns True if the list of bolts already contains a bolt shot by the
        player ship, False otherwise.
        """
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                return True
        return False

    def restore_ship(self):
        """
        Restores the player ship after losing a life.
        """
        self._ship = Ship(x=GAME_WIDTH//2, y=SHIP_BOTTOM, width=SHIP_WIDTH, \
        height=SHIP_HEIGHT, source=SHIP_IMAGE)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Animates the Alien Invaders game.

        Parameter: The view window
        Precondition: view is a GView object
        """
        assert isinstance(view, GView)

        for row in self._aliens:
            for alien in row:
                if not alien is None:
                    alien.draw(view)
        if not self._ship is None:
            self._ship.draw(view)
        self._dline.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def check_collision(self):
        """
        Hides the player ship, removes alien bolt from the list of bolts, and
        removes a player life if the ship is hit by an alien bolt.

        Hides the alien and removes player bolt from the list of bolts if
        an alien is hit by a player bolt.
        """
        for bolt in self._bolts:
            if not self._ship is None and self._ship.collides(bolt):
                self._ship = None
                self._bolts.remove(bolt)
                self._lives = self._lives - 1
            for alien_row in self._aliens:
                for alien in alien_row:
                    y = self._aliens.index(alien_row)
                    if not alien is None and alien.collides(bolt):
                        x = self._aliens[y].index(alien)
                        self._aliens[y][x] = None
                        self._bolts.remove(bolt)

    def checkChange(self):
        """
        Returns True if the player has lost a ship and has lives left.
        Does nothing otherwise.
        """
        change = self._ship is None
        if change and self._lives != 0:
            return True
