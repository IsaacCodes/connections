#Imports + setup
import pygame as pg

import settings

pg.init()


#List of all game objects
objects = pg.sprite.LayeredUpdates()

#Basic object class
class Object(pg.sprite.Sprite):
  def __init__(self, pos: "tuple[int, int]", group: bool, layer: int):
    #Sprite class parent
    super().__init__()
    #Converts image type + alpha
    self.image = self.image.convert_alpha()
    #Creates a rect from the surface
    self.rect = self.image.get_rect(center=pos)

    #Assigns layer and adds player to objects list
    self._layer = layer
    if group:
      objects.add(self)

#Text class
class Text(Object):
  def __init__(self, pos=(0, 0), text="", text_size=24, text_color="black", group=True, layer=0):
    #Creates font image
    self.image = settings.font(text_size).render(text, True, text_color)
    #Stores vars
    self.text = text
    self.text_size = text_size
    self.text_color = text_color
    self.font = settings.font(self.text_size)

    #Object parent
    super().__init__(pos, group, layer)
  
  def update(self, new_text):
    #If text is changing
    if new_text != self.text:
      #Store and updates the text
      self.text = new_text
      self.image = self.font.render(new_text, True, self.text_color)


#Rectangle class
class Rectangle(Object):
  def __init__(self, pos=(0, 0), size=(25, 25), color="black", border_size=0, border_color="black", corner_rounding=0, text="", text_size=24, text_color="black", group=True, layer=0):
    #Creates the base rectangle
    self.image = pg.Surface(size, pg.SRCALPHA)
    pg.draw.rect(self.image, color, pg.Rect((0, 0), size), 0, corner_rounding)
    #If there is a border
    if border_size != 0:
      #Draw a border onto the rectangle
      pg.draw.rect(self.image, border_color, pg.Rect((0, 0), size), border_size, corner_rounding)

    #Object parent (done before adding text so self.rect may be used)
    super().__init__(pos, group, layer)
    
    #Creates text and adds its image
    if text != "":
      #All lines of text
      self.lines = []
      #If all on one line
      if "\n" not in text:
        line_1 = Text(pos, text, text_size, text_color, group=False, layer=layer)
        self.lines.append(line_1)
        
      #If on multiple lines
      else:
        #Finds the size of the rendered text
        render_size = settings.font(text_size).size(text)
        #Finds texts
        lines_text = text.split("\n")
        
        #Create the text objects
        line_1 = Text((pos[0], pos[1]-render_size[1]/2), lines_text[0], text_size, text_color, group=False, layer=layer)
        line_2 = Text((pos[0], pos[1]+render_size[1]/2), lines_text[1], text_size, text_color, group=False, layer=layer)
        #Adds it to the lines attribute
        self.lines.extend([line_1, line_2])
      
      #Loop thru the text list
      for line in self.lines:
        #Finds upper left position where text is blitted then blit it
        blit_pos = (line.rect.left - self.rect.left, line.rect.top - self.rect.top)
        self.image.blit(line.image, blit_pos)

#Circle class
class Circle(Object):
  def __init__(self, pos=(0, 0), diameter=1, color="black", border_size=0, border_color="black", group=True, layer=0):    
    #Alpha compatible image + draw circle on it
    self.image = pg.Surface((diameter, diameter), pg.SRCALPHA)
    image_center = self.image.get_rect().center
    pg.draw.circle(self.image, color, image_center, diameter/2-border_size)
    #Draw interior circle when there is a border
    if border_size != 0:
      pg.draw.circle(self.image, border_color, image_center, diameter/2, width=border_size)

    #Object parent
    super().__init__(pos, group, layer)

#Custom image class
class Image(Object):
  def __init__(self, pos=(0, 0), file="restart.png", size=(0, 0), group=True, layer=0):
    #Loads image
    self.image = pg.image.load(f"{settings.dir}//images//{file}")

    #Changes the size
    if size != (0, 0):
      self.image = pg.transform.smoothscale(self.image, size)

    #Object parent
    super().__init__(pos, group, layer)