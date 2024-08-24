#Imports + setup
import pygame as pg

import object
import settings

pg.init()

#Class for submit button
class Submit(object.Rectangle):
  def __init__(self, board):
    #Vars
    self.board = board
    
    #Overlay that adds color when 4 selected
    self.valid_select_overlay = object.Rectangle((settings.width/2, settings.height - 65), (60, 20), (50, 50, 50), border_size=1, border_color="black", corner_rounding=8, text="Submit", text_size=12, text_color="white", group=False, layer=1)

    #Normal text button
    super().__init__((settings.width/2, settings.height - 65), (60, 20), "white", border_size=1, border_color="black", corner_rounding=8, text="Submit", text_size=12, text_color="black")
    self.image.fill((255, 255, 255, 100), pg.Rect((0, 0), self.rect.size), pg.BLEND_RGBA_MULT)

  #Checks if 4 are selected + potentially reveal overlay 
  def check_valid_select(self):
    #If there is 4, 
    if len(self.board.selected) == 4:
      object.objects.add(self.valid_select_overlay)
    elif self.valid_select_overlay in object.objects:
      object.objects.remove(self.valid_select_overlay)

#Class for mistakes text and circles
class Mistakes():
  def __init__(self, board):
    #Vars
    self.board = board
    
    #"Mistakes: " text
    self.mistakes_text = object.Text((0, 65), "Mistakes:", text_size=18, text_color="black", layer=1)
    self.mistakes_text.rect.right = settings.width/2 - 5

    #Circles for mistakes
    self.mistake_circles = []
    for i in range(settings.max_mistakes):
      self.mistake_circles.append(object.Circle((0, 65), 16, (90,90,80), layer=1))
      self.mistake_circles[i].rect.left = settings.width/2 + 5 + (i*20)

  def remove_circle(self):
    settings.remaining_mistakes -= 1
    object.objects.remove(self.mistake_circles[settings.remaining_mistakes])

#Class for win text
class Game_state():
  #Makes hidden text
  def __init__(self, board):
    #Vars
    self.board = board
    #Win and lose text
    self.win_text = object.Text((settings.width/2, 30), "You win!", text_size=28, text_color="green", group=False, layer=1)
    self.lose_text = object.Text((settings.width/2, 30), "You lose!", text_size=28, text_color="red", group=False, layer=1)
    
  #Checks whether to reveal the text
  def check_state(self):
    #If successfully selected all blocks, you win
    if len(self.board.matrix) == 0:
      object.objects.add(self.win_text)
      settings.game_over = True
    #If out of mistakes, you lose
    elif settings.remaining_mistakes <= 0:
      object.objects.add(self.lose_text)
      settings.game_over = True


#Class for one away text
class One_away(object.Rectangle):
  def __init__(self, board):
    #Vars
    self.board = board
    self.is_visible = False
    self.appear_cd = 3000 #ms
    self.appear_time = 0
    
    #One away text
    super().__init__((settings.width/2, 30), (65, 20), "black", text="One Away!", text_size=12, text_color="white", group=False)

  def check_appear(self):
    #The words (strings) that the user has selected
    selected_words = [block.word for block in self.board.selected]

    #Loops through all the board's difficulty lists
    for diff_list in self.board.all_lists:
      #How many words of overlap do they have
      overlap_count = 0
      for word in selected_words:
        if word in diff_list[1]:
          overlap_count += 1
      #If they have 3 words of overlap
      if overlap_count == 3:
        #Reveal the one away text and change vars
        object.objects.add(self)
        self.appear_time = pg.time.get_ticks()
        self.is_visible = True
  
  def check_disappear(self, force_off=False):
    #If text is visible and atleast appear_time ms have passed
    if self.is_visible and pg.time.get_ticks() - self.appear_time > self.appear_cd or force_off:
      #Hide the object and change vars
      object.objects.remove(self)
      self.is_visible = False

#Help button and text
class Help():
  def __init__(self):
    #Vars
    self.is_visible = False
    
    #Creates the button and help text
    self.button = object.Rectangle((13, 13), (22, 22), color="black", corner_rounding=7, text="?", text_size=20, text_color="white")
    
    self.help_text = object.Rectangle((settings.width/2, settings.height/2), (settings.width-15, 75), color="gray", text="Select 4 different words that fit in to one connected category.\n Then click submit. Good luck gettings all 4 connections!", text_size=16, text_color="white", layer=2, group=False)

  #Toggles where it is visible
  def toggle_show(self):
    if not self.is_visible:
      object.objects.add(self.help_text)
      self.is_visible = True
    else:
      object.objects.remove(self.help_text)
      self.is_visible = False