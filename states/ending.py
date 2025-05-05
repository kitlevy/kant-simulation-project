import pygame
import pygame.freetype
from states.state import State
from text_utils import *

class Ending(State):
    def __init__(self, game):
        State.__init__(self, game)
        

    def update(self, delta_time):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            from states.title import Title
            Title(self.game).enter_state()
       
    def render(self, display):
        display.fill((255, 255, 255))

        W, H = self.game.GAME_W, self.game.GAME_H
        gap = 0
        top = H // 8 + gap
        spacing = 12
        font = self.game.font
        textcol = (0, 0, 0)
        green = (0, 128, 0)
        red = (255, 0, 59)



        if self.game.selfishmode:
            draw_centered_text(font, display,
                "You took more than you needed, and because everyone else followed\n" +
                "your lead, the ponds were emptied and the village collapsed.",
                (W // 2, top), line_height=16, color=red
            )

            draw_centered_text(font, display,
                "Kant’s categorical imperative challenges us to ask: “What if\n" +
                "everyone did what I’m doing?” If the answer is destruction\n" +
                "or contradiction, the action is immoral. Your choice to take\n" +
                "as many fish as possible may seem justifiable for your own\n" +
                "survival or comfort, but if everyone did the same, the resource\n" +
                "couldn’t survive. That’s exactly what happened: the system broke\n" +
                "because the rule you acted on - “Take as much as you can” - can’t\n" +
                "be universalized without disaster.",
                (W // 2, top + 6 * spacing), line_height=spacing, color=textcol
            )

            draw_centered_text(font, display,
                "In the real world, we often face similar challenges with shared\n" +
                "resources. Whether it’s overfishing, pollution, or hoarding during\n" +
                "shortages, Kant’s principle reminds us that ethical choices aren’t\n" +
                "just about short-term gain, but about whether the logic of our\n" +
                "actions could sustain a fair world for all.",
                (W // 2, top + 13 * spacing), line_height=spacing, color=textcol
            )


        else:
            draw_centered_text(font, display,
                "You chose to take only what you needed, and because everyone else\n" +
                "followed your example, the community thrived.",
                (W // 2, top), line_height=16, color=green
            )

            draw_centered_text(font, display,
                "From a Kantian perspective, your decision reflects a moral action guided by a\n" +
                "universal principle: “Only take what you need so the resource can replenish.”\n" +
                "If everyone acted as you did, the rule would still hold and lead to a\n" +
                "sustainable world, so you passed the test of the categorical imperative. You\n" +
                "respected the idea that morality isn’t about making exceptions for yourself;\n" +
                "it's about acting in ways that could consistently be adopted by everyone.",
                (W // 2, top + 6 * spacing), line_height=spacing, color=textcol
            )

            draw_centered_text(font, display,
                "In real life, sustainable resource management depends on just this kind\n" +
                "of thinking. Whether it’s fishing, logging, or carbon emissions, Kantian\n" +
                "moral reasoning requires us to consider what would happen if everyone\n" +
                "made the same choice we’re making, and then act accordingly.",
                (W // 2, top + 12 * spacing), line_height=spacing, color=textcol
            )
        
        draw_centered_text(font, display,
            "PRESS R TO RESTART",
            (self.game.GAME_W // 2, self.game.GAME_H - 30), (0, 0, 0))

