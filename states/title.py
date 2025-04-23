import pygame
import pygame.freetype
from states.state import State

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
        top = self.game.GAME_H/4
        spacing = 20
        display.fill((255,255,255))
        self.game.draw_text(display, "Visualizing Kant's Categorical Imperative" , (0,0,0), self.game.GAME_W/2, top)
        self.game.draw_text(display, "Immanuel Kant believed in the existence of universal moral laws. He argued that any rational being could discover these laws by using reason (which he says we all have in common). This led him to his principle of the categorical imperative, which states that our actions must be guided by rules that apply equally to anyone in any circumstance.", (0,0,0), self.game.GAME_W/2, top+spacing)
        self.game.draw_text(display, "Kant’s categorical imperative basically says: act in a way that you’d be okay with everyone else acting, all the time, in the same situation. In simple terms: if it’d be a mess if everyone did what you’re about to do, then don’t do it! Morality has to be consistent and apply to everyone equally.", (0,0,0), self.game.GAME_W/2, top+2*spacing)
        self.game.draw_text(display, "We're going to illustrate Kant's categorical imperative with a simulation, where you're a fisherman taking fish from a pond to feed your family. You can survive with just one fish, but would really like a fish for each of your four family members. Overnight, every pair of fish in a pond will repopulate the pond with one new fish. Each day you'll have the option to take just one fish, or to take as many as you can (up to four). Here's the catch: the rest of the fisherman in the town will behave the same way you do. How will you act?" , (0,0,0), self.game.GAME_W/2, top+3*spacing)

        self.game.draw_text(display, "PRESS ENTER TO START", (0,0,0), self.game.GAME_W/2, top+4*spacing)
