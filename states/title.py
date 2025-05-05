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
        top = H // 8
        spacing = 10
        font = self.game.font

        draw_centered_text(font, display,
            "Visualizing Kant's Categorical Imperative",
            (W // 2, top), line_height=20, color=(0, 0, 0)
        )

        draw_centered_text(font, display,
            "Immanuel Kant believed in the existence of universal moral laws.\n"
            "He argued that any rational being could discover these laws by using reason\n"
            "(which he says we all have in common). This led him to his principle of the\n"
            "categorical imperative, which states that our actions must be guided by rules\n"
            "that apply equally to anyone in any circumstance.",
            (W // 2, top + 5 * spacing), line_height=spacing, color=(0, 0, 0)
        )

        draw_centered_text(font, display,
            "Kant’s categorical imperative basically says: act in a way that you’d be\n"
            "okay with everyone else acting, all the time, in the same situation.\n"
            "In simple terms: if it’d be a mess if everyone did what you’re about to do,\n"
            "then don’t do it! Morality has to be consistent and apply to everyone equally.",
            (W // 2, top + 11 * spacing), line_height=spacing, color=(0, 0, 0)
        )

        draw_centered_text(font, display,
            "We're going to illustrate Kant's categorical imperative with a simulation,\n"
            "where you're a fisherman taking fish from a pond to feed your family.\n"
            "You can survive with just one fish, but would really like a fish for each\n"
            "of your four family members. Overnight, every pair of fish in a pond will\n"
            "repopulate the pond with one new fish. Each day you'll have the option to take\n"
            "just one fish, or to take as many as you can (up to four).\n"
            "Here's the catch: the rest of the fisherman in the town will behave the same\n"
            "way you do. How will you act?",
            (W // 2, top + 18 * spacing), line_height=spacing, color=(0, 0, 0)
        )

        draw_centered_text(font, display,
            "PRESS ENTER TO START",
            (W // 2, H - 3 * spacing), line_height=spacing, color=(0, 0, 0)
        )
    
