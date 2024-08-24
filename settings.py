#Imports + setup
import pygame as pg
import os

pg.init()

#Window size
size = width, height = (550, 400)

#Finds current directory
dir = os.path.dirname(os.path.realpath(__file__))

#Game font
def font(size: int):
  font = pg.font.Font('freesansbold.ttf', size)
  return font

#Max allowed mistakes
max_mistakes = 4
#Remaining mistakes
remaining_mistakes = max_mistakes

#Whether to keep running the game
game_over = False