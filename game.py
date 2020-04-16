#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snowman can move left or right. Press enter to start the game.
Get points and health by collecting snowflakes. Health runs out over time.
Snowman dies if it hits the branches or melts (does not have enough health)
"""

# --------------- Imports -------------------------------
from PPlay.window import Window
from PPlay.gameimage import GameImage
from scorer import Scorer
from highscoremanager import ScoreManager
from random import randint

import pygame
import os

# --------------- Global variables -------------------------------

game_state = 2  # Game starts showing menu

# Set display
background = GameImage('sprite/scenario/scenarionew.png')
menu_bg = GameImage('sprite/scenario/start1.png')
game_over = GameImage('sprite/scenario/GameOver1.png')
button = GameImage('sprite/scenario/button1.png', 0, -140)

# Define screen variables
sWidth = 512 # screen width
sHeight = 512 # screen height
window = Window(sWidth, sHeight)
window.set_title('Snowie Game')

# Managing points and health  
score_manager = ScoreManager() # Stores high score and last score
scorer = Scorer(window) # Calculates points and health
record_checked = False

# Define branch variables
branchHeight = 64 
treeHeight = GameImage('sprite/branches/middle.png').get_height()

# Define snowman variables
snowmanDist = 45   # Changes distance from tree
snowmanY = sHeight - 80  # Distance from bottom of screen
flakeDist = 50 # Flake distance from tree
snowmanH = 64 # Height of snowman

# Speed of branches and snowflakes
startSpeed = 6
maxSpeed = 12

# --------------- Additional classes ------------------------------- 

class Branches:
    
    global startSpeed 
    changeY = startSpeed # Speed at which branch moves down
    direction = "up" #Determines whether speed increases or decreases over time
    
    # Images for branches
    tree_types = ('sprite/branches/right.png',
                  'sprite/branches/left.png',
                  'sprite/branches/middle.png')
    
    endOfScreen = False # Records if branch has reached end of screen

    def __init__(self,y, pos):
        self.y = y # y-coordinate (distance from top of screen)
        self.pos = pos 
        if pos == "left": # branch 'left' to tree
            self.type = 1
        elif pos == "right": # branch 'right' to tree
            self.type = 0
        else:
            self.type = 2 # no branch if position is 'middle'
        
        # Assigns an image to each object
        self.texture = GameImage(self.tree_types[self.type])
        self.texture.set_position(0, self.y)
        
    # Change position of object
    def set_position(self, x, y):
        self.texture.set_position(x, y)
    
    # Display branch
    def paint(self):
        self.set_position(0,self.y)
        self.texture.draw()
        
    # Move branch
    def move(self, snowmanPos):
        global game_state
        
        # Finds new y value (which defines top of branch)
        newY = self.y + self.changeY
        
        lowerBound = newY + branchHeight # y coordinate for bottom of branch
        bottomOfSnowman = snowmanY + snowmanH # y value for bottom of snowman
         
        if lowerBound > snowmanY and newY < bottomOfSnowman \
        and snowmanPos == self.pos:
            # New branch would be in snowmans space (snowman hits branch)
                game_state = 0 # Game over
                gameEnd.play() # Play sound effect
                
        # Branch reaches end of screen so starts at top again
        elif (newY > sHeight):
            # Useful for objects of type 'middle' which create tree
            self.y = -64 
            self.paint()
            # Useful for other objects which are actual branches
            self.endOfScreen = True
        else:
            # Branch moves down 
            self.y += self.changeY
            self.paint()


class Snowman:
    
    # Images for snowman
    sprites = (GameImage('sprite/snowman/snowmanLeft.png',  snowmanDist, snowmanY),
               GameImage('sprite/snowman/snowmanRight.png', -snowmanDist, snowmanY),
               GameImage('sprite/snowman/meltyLeft.png',    snowmanDist, snowmanY),
               GameImage('sprite/snowman/meltyRight.png',   -snowmanDist, snowmanY))
 
    def __init__(self, pos):
        self.pos = pos # Snowman position is left or right of tree 
    
    # Draws snowman on correct side of tree
    def paint(self):   
        if self.pos == "left":
            self.sprites[0].draw()
        else:
            self.sprites[1].draw()


class Snowflake:
    
    flakeImage = ('sprite/scenario/flakeL.png', 'sprite/scenario/flakeR.png')
    
    endOfScreen = False # Checks if snowflake is at end of screen
    
    global startSpeed
    changeY = startSpeed # Snowflake speed

    def __init__(self, y, pos):
        self.pos = pos # left or right
        self.y = y # y coordinate
        
        if pos == "left":
            self.type = 0
        else:
            self.type = 1
        
        # Retrieves snowflake image
        self.texture = GameImage(self.flakeImage[self.type])
        self.set_position()
    
    # Changes position
    def set_position(self):
        if self.pos == "left":
            self.texture.set_position(flakeDist, self.y)
        else:
            self.texture.set_position(-flakeDist, self.y)
            
    # Displays snowflake
    def paint(self):
        self.set_position()
        self.texture.draw()  

    # Moves snowflake
    def move(self, snowmanPos):
        
        newY = self.y + self.changeY
        lowerBound = newY + branchHeight # y coordinate for bottom of flake
        bottomOfSnowman = snowmanY + snowmanH # y value for bottom of snowman
        
        # New flake would be in snowmans space
        if lowerBound > snowmanY and newY < bottomOfSnowman \
        and snowmanPos == self.pos:
            # Gain points and health by catching snowflakes
            scorer.snowflake_calc() 
            # This allows us to delete snowflake later
            self.endOfScreen = True

        elif (lowerBound > sHeight):
            # Snowflake reaches end of screen
            self.endOfScreen = True
        else:
            # Snowflake moves down
            self.y += self.changeY
            self.paint()
            

# --------------- Functions -------------------------------
            
# Displays all objects: background, snowman, tree, branches, snowflakes & score
def paintEverything():
    
    background.draw()
    snowman.paint()
    
    for item in tree:
        item.paint()

    for item in branches:
        item.paint()
        
    for item in flakes:
        item.paint()
    
    scorer.draw()
    pygame.display.flip()

# Move all objects: tree, branches and snowflakes
def moveEverything():
    
    for item in tree:
        item.move(snowman.pos)
        
    # Move branches
    for index, item in enumerate(branches):
        item.move(snowman.pos)
        # If branch reaches end of screen, delete it
        if item.endOfScreen:
            del branches[index]

    # Move snowflakes
    for index, item in enumerate(flakes):
        item.move(snowman.pos)
        # If snowflake reaches end of screen (or is hit by snowman), delete it
        if item.endOfScreen:
            del flakes[index]
    
    scorer.draw() # Update score
    pygame.display.flip()
    
    
# Add more branches
def add_branches():
    
    side = randint(0,1) # Generates random side of tree (left or right)
    gap = 200 # Minimum gap between branches
    desiredNumOfBranches = 4
    count = 1
    while True:
        # Finds a possible y coordinate to place the branch on 
        newY = randint(-512, 0)
        okayPosition = True
        
        # Checks if this would be too close to existing branches s
        for item in branches:
            if abs(newY-item.y) <= gap:
                okayPosition = False
        
        # Checks if newY is too close to existing snowflakes 
        """
        for item in flakes:
            if abs(newY-item.y) <= gap and side == item.type:
                okayPosition = False
        """
        """ This is commented because the game is not challenging enough if 
        snowflakes are never created close to branches.
        """
                
        # If an appropriate y value is found, exit loop
        if okayPosition:
            yValue = newY
            break
        
        count +=1
        # Exit loops if not possible (to avoid infinite loop)
        if count == 20:  
            yValue = False
            break
    
    # Add branch object to list of branches (if there are not enough branches)
    if len(branches) < desiredNumOfBranches and yValue != False:
        if side == 0: # Create left branch
                branches.append(Branches(yValue, "left"))
        else: # Create right branch
                branches.append(Branches(yValue, "right"))
        
 
# Add more snowflakes
def add_flakes():
    
    side = randint(0,1) # Generates random side
    gap = 100 # Minumum gap between snowflakes
    desiredNumOfFlakes = 4
    count = 1
    while True:
        newY = randint(-512, 0) # Finds possible y coordinate for snowflake
        okayPosition = True
        
        # Checks if newY is too close to existing branches and snowflakes
        for item in branches:
            if abs(newY-item.y) <= gap:
                okayPosition = False
        for item in flakes:
            if abs(newY-item.y) <= gap:
                okayPosition = False
                
        # If an appropriate y value is found, exit loop
        if okayPosition:
            yValue = newY
            break
        
        count += 1
        # Exit loops if not possible (to avoid infinite loop)
        if count == 20:
            yValue = False
            break
    
    # Add snowflake (if desired)
    if len(flakes) < desiredNumOfFlakes and yValue != False:
        if side == 0: # left branch
                flakes.append(Snowflake(yValue, "left"))
        else:
                flakes.append(Snowflake(yValue, "right"))
    

# --------------- Main code -------------------------------


# Initialise pygame and load screen
pygame.init()
pygame.mixer.pre_init(44100,16,2,4096)
screen = pygame.display.set_mode((sWidth, sHeight))

# Plays background music
pygame.mixer.music.load('sound_effects/music.ogg')
pygame.mixer.music.play(-1)

# Stores sound effect of gameover
gameEnd = pygame.mixer.Sound("sound_effects/sound2.wav")

# Initialise snowman
snowman = Snowman("right")

# List to store branches
branches = []

# Create initial snowflakes
flakes = []
flakes.append(Snowflake(50, "right"))
flakes.append(Snowflake(340, "left"))

# Create tree (default background)
tree = []
for i in range(sHeight*2):
    if (i+1)%(treeHeight-10)==0:
        tree.append(Branches(i+1-(2*treeHeight), "middle"))



# Sets the speed of program
clock = pygame.time.Clock()
clock.tick(40)
counter = 1 # Time counter

while True:
    
    # Can close game at any time 
    e = pygame.event.poll()
    if e.type == pygame.QUIT:
        break

    elif game_state == 1:
        # Game in progress
        pygame.mixer.music.unpause() # Keep background music playing
        
        # Pressing left and right changes snowman position
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            snowman.pos = "left"
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                snowman.pos = "right"
                
        # Add branches and snowflakes if necessary
        add_branches()
        add_flakes()

        # Update background and graphics
        paintEverything()
        # Lose health over time
        if counter > 50:
           scorer.update() 

        # Branches and snowflakes move at different speeds over time
        speedChange = 300
        if counter%speedChange == 0: 
            if Branches.changeY == maxSpeed:
                # When maxSpeed speed is reached, game starts slowing down 
                Branches.diretion = "down"
            elif Branches.changeY == startSpeed:
                # At startSpeed, game speeds up again
                Branches.direction = "up"
            
            if Branches.direction == "up":
                # Game speeds up
                Branches.changeY += 1
                Snowflake.changeY += 1
            else:
                # Game slows down
                Branches.changeY -= 1
                Snowflake.changeY -= 1
            
        # Move branches and snowflakes
        moveEverything()
        
        # Gain points over time
        if counter%50 == 0:
            scorer.add_points()
        
        # If snowie is no longer alive, game ends
        if not scorer.snowie_alive():
            game_state = 0 # Game over
            gameEnd.play() # Plays sound effect
            
        counter += 1

        # Shows any changes made
        pygame.display.flip()
        window.update()

    elif game_state == 2:
        # Menu screen
        
        background.draw()
        if counter < 500:
            # Initially display instructions for some time
            menu_bg.draw()
            window.draw_text(str(score_manager.get_records()), 512 - 260, 320, color=(255,255,255), font_file='font.TTF', size=20)
        else:
            # Then show 'press enter to play' button
            button.draw()
        pygame.display.flip()
        counter += 1
        
        # If enter is pressed, game starts
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            game_state = 1
            counter = 1 # Time resets

            # Initial graphics
            paintEverything()
        

    elif game_state == 0:
        # Game over
        
        # Pauses background music 
        pygame.mixer.music.pause()
        
        # Calculate high score
        if not record_checked:
            if scorer.get_points() > score_manager.get_records():
                score_manager.set_new_record(scorer.get_points())
            record_checked = True
        
        # Display game over screen
        background.draw()
        game_over.draw()
        
        # Draw melted snowman
        if snowman.pos== "left":
                Snowman.sprites[2].draw()
        else:
                Snowman.sprites[3].draw()

        # Show score and overall high score 
        window.draw_text(str(score_manager.get_records()), 260, 205, color=(20, 200, 50), font_file='font.TTF',
                         size=30) # High scoree
        window.draw_text(str(scorer.get_points()), 260, 240, color=(20, 200, 50), font_file='font.TTF',
                         size=30) # Last score

        # Press enter to start game again
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            game_state = 1
            counter = 1 # Time resets
            
            # Re-initialise objects
            snowman = Snowman("right")
            branches = []
            flakes = []
            
            # Reset speed 
            Branches.changeY = startSpeed 
            Snowflake.changeY = startSpeed
            Branches.direction = "up"
                      
            # Display graphics 
            paintEverything()
            
            # Reset score and health 
            scorer = Scorer(window)
            record_checked = False
            

        pygame.display.flip()



pygame.quit()  # Stops program
os._exit(0)  # Stops program for mac OS users
