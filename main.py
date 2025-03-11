#Imports and setup
import pygame as pg

import game_board
import ui
import object
import settings

pg.init()

#Creates screen
screen = pg.display.set_mode(settings.size)
pg.display.set_caption("Connections")

restart = False
#Main functions
def main():
  #Board object
  board = game_board.Board()
  #Buttons/ui
  submit_button = ui.Submit(board)
  mistakes_ui = ui.Mistakes(board)
  game_state_ui = ui.Game_state(board)
  one_away_ui = ui.One_away(board)
  help_ui = ui.Help()
  restart_button = object.Image((settings.width - 15, 15), "restart.png", layer=1)
  
  #Game loop
  running = True
  clock = pg.time.Clock()
  while running:
    global restart
    #Max 60 fps
    clock.tick(60)
  
    #Event loop
    for event in pg.event.get():
      #Quit
      if event.type == pg.QUIT:
        running, restart = False, False
      #On left click
      if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        #Checks if restart button is clicked
        if restart_button.rect.collidepoint(pg.mouse.get_pos()):
          running, restart = False, True
        if help_ui.button.rect.collidepoint(pg.mouse.get_pos()):
          help_ui.toggle_show()

        #Don't activate events when game is over or help_ui is overlayed
        if settings.game_over or help_ui.is_visible:
          break
        
        #Select blocks
        for block in board.matrix:
          if block.rect.collidepoint(pg.mouse.get_pos()):
            block.switch_selected()
        #Click submit
        if submit_button.rect.collidepoint(pg.mouse.get_pos()) and len(board.selected) == 4:
          board.submit_selected(mistakes_ui, one_away_ui)
  
    #If game has ended
    if not settings.game_over:
      #Checks if submit is valid and a win/loss case passes
      submit_button.check_valid_select()
      game_state_ui.check_state()
      one_away_ui.check_disappear()
    #If the game has ended, force these functions
    if settings.game_over:
      one_away_ui.check_disappear(True)
    
    #Background
    screen.fill((250, 250, 250))
    #Draw all game objects
    object.objects.draw(screen)
    #Updates screen
    pg.display.update()

#Runs the game
main()
#If the player clicks restart
while restart == True:
  #Reset some vars and rerun main
  settings.game_over = False
  settings.remaining_mistakes = settings.max_mistakes
  object.objects = pg.sprite.LayeredUpdates()
  main()

