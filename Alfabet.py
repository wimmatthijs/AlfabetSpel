#!/usr/bin/env python
""" pygame.examples.sound

Playing a soundfile and waiting for it to finish. You'll need the
pygame.mixer module for this to work. Note how in this simple example
we don't even bother loading all of the pygame package.
Just pick the mixer for sound and time for the delay function.

Optional command line argument: audio file name
"""
import sys
import os
from typing import List

import pygame
import pygame as pg
import pygame.freetype as freetype

import random


os.environ["SDL_IME_SHOW_UI"] = "1"

main_dir = os.path.split(os.path.abspath(__file__))[0]


class TextInput:
    """
    A simple TextInput class that allows you to receive inputs in pygame.
    """

    # Add font name for each language,
    # otherwise some text can't be correctly displayed.
    FONT_NAMES = ",".join(
        str(x)
        for x in [
            "notosanscjktcregular",
            "notosansmonocjktcregular",
            "notosansregular,",
            "microsoftjhengheimicrosoftjhengheiuilight",
            "microsoftyaheimicrosoftyaheiuilight",
            "msgothicmsuigothicmspgothic",
            "msmincho",
            "Arial",
        ]
    )
    BG_COLOR = "black"
    currentFrame = 0

    def __init__(
        self, screen_dimensions, print_event: bool, text_color="white"
    ) -> None:
        self.print_event = print_event
        # position of chatlist and chatbox

        self.currentCharacter=""
        self.currentFolder=""
        self.selectedSubFolder=""
        self.isDrawing = False
        self.isPlayingSound = False
        # Freetype
        # The font name can be a comma separated list
        # of font names to search for.
        self.font = freetype.SysFont(self.FONT_NAMES, size=pg.display.get_window_size()[1]/4*5)
        self.text_color = text_color
        pg.mixer.init()

        print("Using font: " + self.font.name)

    def update(self, events, screen: pygame.Surface) -> None:
        """
        Updates the text input widget
        """
        # Makes it possible to redraw and replay sound if the same character was pushed after tasks are finished
        if (not pg.mixer.get_busy()) and (not self.isDrawing):
            self.currentCharacter = ""

        for event in events:
            if event.type == pg.TEXTINPUT and event.text in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890":
                if self.print_event:
                    print(event)
                #keeping track of previous state
                if self.currentCharacter == event.text.upper():
                    return
                else:
                    self.currentCharacter = event.text.upper()
                    folders = os.listdir(os.path.join(main_dir,"data/"+self.currentCharacter))
                    print(folders)
                    if len(folders) > 0: self.selectedSubFolder = random.choice(folders)
                    self.currentFolder = "data/"+ self.currentCharacter + "/" + self.selectedSubFolder
                    print("selected folder = "+self.currentFolder)
                    self.draw(screen)
                    self.playSound()

        #update frame if frame was not yet finished
        if (self.isDrawing):
            self.draw(screen, self.currentFrame)

    def draw(self, screen: pygame.Surface, startFrame = 0) -> None:
        """
        Draws the text onto the provided surface, will in the future take frame into account
        """
        self.isDrawing = True
        print("Drawing screen")

        try:
            with open(os.path.join(main_dir, self.currentFolder, "color.txt"), "r") as color:
                self.BG_COLOR = color.readline()
        except:
            self.BG_COLOR = "black"

        if self.BG_COLOR == "white":
            self.text_color = "black"
        else:
            self.text_color = "white"
        screen.fill(self.BG_COLOR)
        characterRect = self.font.get_rect(self.currentCharacter)
        characterRect.center = screen.get_rect().center
        self.font.render_to(screen,characterRect,self.currentCharacter,self.text_color)
        self.isDrawing = False

    def playSound(self):
        try:
            #stop previous sound if necessary
            pg.mixer.stop()
            sound = pg.mixer.Sound(os.path.join(main_dir, self.currentFolder, self.selectedSubFolder+".wav"))
            print("Playing Sound...")
            sound.play()
        except FileNotFoundError:
            print("File for " + self.currentCharacter + " not found yet")

class Game:
    """
    A class that handles the game's events, mainloop etc.
    """

    # CONSTANTS
    # Frames per second, the general speed of the program
    FPS = 50

    def __init__(self, caption: str) -> None:
        # Initialize
        pg.init()
        self.screen = pg.display.set_mode((0,0), pygame.FULLSCREEN)
        pg.display.set_caption(caption)
        self.clock = pg.time.Clock()

        # Text input
        # Set to true or add 'showevent' in argv to see IME and KEYDOWN events
        #self.print_event = "showevent" in sys.argv
        self.print_event = True
        self.text_input = TextInput(
            screen_dimensions=(pygame.display.get_window_size()),
            print_event=self.print_event,
            text_color="white",
        )

    def main_loop(self) -> None:

        pg.key.start_text_input()
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                ''' #Escape to exit the game, disabled for now to just stay in the game
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pygame.quit()
                    return
                '''

            self.text_input.update(events, self.screen)
            pg.display.update()
            self.clock.tick(self.FPS)


# Main loop process
def main():
    game = Game("Alfabet")
    game.main_loop()

if __name__ == "__main__":
    main()