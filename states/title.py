import pygame
import pygame.freetype
from states.state import State
from text_utils import *

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        

    def update(self, delta_time):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from states.fish_sim import FishSim
                FishSim(self.game).enter_state()

    def render(self, display):
        display.fill((255, 255, 255))

        W, H = self.game.GAME_W, self.game.GAME_H
        gap = -12
        top = H // 8 + gap
        spacing = 12
        font = self.game.font
        textcol = (0, 0, 0)

        draw_centered_text(font, display,
            "Visualizing Kant's Categorical Imperative",
            (W // 2, top), line_height=16, color=textcol
        )

        draw_centered_text(font, display,
            "Immanuel Kant believed in the existence of universal moral laws.\n" +
            "He argued that any rational being could discover these laws by using\n" +
            "reason (which he says we all have in common). This led him to his\n" +
            "principle of the categorical imperative, which states that our\n" +
            "actions must be guided by rules that apply equally to anyone.",      
            (W // 2, top + 4 * spacing), line_height=spacing, color=textcol
        )

        draw_centered_text(font, display,
            "Kant’s categorical imperative basically says: act in a way that you'd\n" +
            "be okay with everyone else acting, all the time. In simple terms: if it'd\n" +
            "be a mess if everyone did what you're about to do, then don't do it!\n" +
            "Morality has to be consistent and apply to everyone equally.",
            (W // 2, top + 9 * spacing), line_height=spacing, color=textcol
        )

        draw_centered_text(font, display,
            "We're going to illustrate Kant's categorical imperative with a simulation:\n" +
            "You're a fisherman taking fish from ponds to feed your family. You can\n" +
            "survive with just one fish, but you'd really like a fish for each of your four\n" +
            "family members. Overnight, every pair of fish in a pond will repopulate the pond\n" +
            "with one new fish. Each day you'll have the option to take just one fish, or to\n" +
            "ake as many as you can (up to four). Here's the catch: the rest of the fishermen\n" +
            "in the town will behave the same way you do. How will you act?",
            (W // 2, top + 15 * spacing), line_height=spacing, color=textcol
        )

        draw_centered_text(font, display,
            "PRESS ENTER TO START",
            (W // 2, top + 20 * spacing), line_height=spacing, color=textcol
        )

        draw_centered_text(font, display,
            "By Kit Levy",
            (42, H - spacing), line_height=8, color=textcol
        )

        draw_centered_text(font, display,
            "github.com/kitlevy",
            (W - 72, H - spacing), line_height=8, color=textcol
        )
