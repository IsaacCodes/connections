#Imports + setup
import pygame as pg
import random as r

import object
import settings
import connection_list

pg.init()

#Individual blocks
class Block(object.Rectangle):
  def __init__(self, word, connection, board):
    #Stores vars
    self.word = word
    self.connection = connection
    self.selected = False
    self.board = board

    #Text to be passed into rectangle object
    text = word
    #Other vars to be passed
    text_size = 14
    block_size = (120, 50)
    #If the text is too big,
    render_size = settings.font(text_size).size(text)
    if render_size[0] > block_size[0] and text.count(" ") >= 1:
      text = word.replace(" ", "\n", 1)
    #Text overlay for selected text
    self.selected_overlay = object.Rectangle((0, 0), block_size, (90, 90, 80), border_size=1, border_color="black", corner_rounding=8, text=text, text_size=text_size, text_color="white", group=False, layer=1)
    
    #Creates blocks (position will be set by board)
    super().__init__((0, 0), block_size, (240, 240, 220), border_size=1, border_color="black", corner_rounding=8, text=text, text_size=14, text_color="black")
    
  #Switches between selection states
  def switch_selected(self):
    #If its not selected
    if not self.selected:
      #Break when 4 already selected
      if len(self.board.selected) >= 4:
        return
      #Change vars and add the selected
      self.selected = True
      self.board.selected.append(self)
      object.objects.add(self.selected_overlay)
    #If it is selected
    else:
      #Change vars and remove the selected
      self.selected = False
      self.board.selected.remove(self)
      object.objects.remove(self.selected_overlay)

class Connection_block(object.Rectangle):
  def __init__(self, words, connection, color, board):
    #Vars
    self.words = words
    self.connection = connection
    self.board = board

    #Creates block, position set later
    super().__init__((0, 0), (510, 50), color, text=f"{connection}:\n{', '.join(words)}", text_size=15, group=False)

  #Sets connection block position and reveals it
  def reveal_self(self):
    self.rect.centerx = settings.width/2
    self.rect.centery = (self.board.revealed-1.5)*(50+self.board.buff) + settings.height/2
    object.objects.add(self)

    self.board.revealed += 1
    

#Board class
class Board():
  def __init__(self):
    #Vars
    self.selected = []
    #How many times the connections have been revealed so far
    self.revealed = 0
    
    #Gets a random word index
    i = r.randint(0, len(connection_list.easy_list)-1)
    #Uses that day's connections
    self.easy_list = connection_list.easy_list[i]
    self.medium_list = connection_list.medium_list[i]
    self.hard_list = connection_list.hard_list[i]
    self.insane_list = connection_list.insane_list[i]
    #List of all lists
    self.all_lists = [self.easy_list, self.medium_list, self.hard_list, self.insane_list]
    print(self.all_lists)
    
    #Creates matrix of blocks based on difficulty lists from all_lists
    self.matrix = []
    for diff_list in self.all_lists:
      for word in diff_list[1]:
        block = Block(word, diff_list[0], self)
        self.matrix.append(block)

    #Block buffer
    self.buff = 10
    #Shuffles the matrix and assigns positions
    self.reoder_matrix(4)

    #Connection category blocks
    colors = ["green", "yellow", "orange", "red"]
    self.connection_blocks = [Connection_block(words, connection, colors[i], self) for i, (connection, words) in enumerate(self.all_lists)]

  #Submits all selected blocks
  def submit_selected(self, mistakes, one_away):
    #Cancel if not enough selected
    if len(self.selected) != 4:
      return
    #Creates a sorted list of all the selected blocks' words
    selected_words = [block.word for block in self.selected]
    selected_words.sort()
    #Loops thru the connections in all lists
    for diff_list in self.all_lists:
      #If you have the correct word list
      if selected_words == diff_list[1]:
        #Removes the blocks and their components from the screen and matrix
        for block in self.selected:
          object.objects.remove(block)
          object.objects.remove(block.selected_overlay)
          self.matrix.remove(block)
        #Empties selected list
        self.selected = []
        #Reorders matrix
        self.reoder_matrix(len(self.matrix)/4)
        #Loops thru connection blocks
        for connection_block in self.connection_blocks:
          #Reveals connection category block for correct connection
          if connection_block.connection == diff_list[0]:
            connection_block.reveal_self()
            return
    #If function didn't return (failed to match connection) remove circle
    mistakes.remove_circle()
    one_away.check_appear()

  #Randomizes the matrix and moves to selected number of rows
  def reoder_matrix(self, row_count):
    #Randomizes blocks
    r.shuffle(self.matrix)
    for block in self.matrix:
      #X and Y positions for the block in the matrix. Split by row and column
      x = self.matrix.index(block) % 4
      y = self.matrix.index(block) // 4
      #Creates a matrix of blocks in the center of the screen
      screen_x = (x-2)*(block.rect.width+self.buff) + settings.width/2 + self.buff/2
      screen_y = (y-2+(4-row_count))*(block.rect.height+self.buff) + settings.height/2 + self.buff/2
      block.rect.topleft = (screen_x, screen_y)
      block.selected_overlay.rect.topleft = (screen_x, screen_y)