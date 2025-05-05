import pygame
import pygame.freetype
import os, sys, time

from states import Title, FishSim

class Game():
    def __init__(self):
        pygame.init()
        self.GAME_W, self.GAME_H = 600, 300
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 960, 540
        self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.running, self.playing = True, True
        self.selfishmode = False
        self.dt, self.prev_time = 0, time.time()
        self.state_stack = []
        self.load_assets()
        self.load_states()

    def game_loop(self):
        clock = pygame.time.Clock()
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()
            clock.tick(60)

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            else:
                if self.state_stack:
                    self.state_stack[-1].handle_event(event)

    def update(self):
        if self.state_stack:
            self.state_stack[-1].update(self.dt)

    def render(self):
        if self.state_stack:
            self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(pygame.transform.scale(self.game_canvas, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0, 0))
        pygame.display.flip()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y):
        self.font.render_to(surface, (x, y), text, color)

    def load_assets(self):
        self.assets_dir = os.path.join("assets")
        self.font_dir = os.path.join(self.assets_dir, "font")
        self.font = pygame.freetype.Font("assets/PixelOperator-Bold.ttf",16)
        #self.font = pygame.freetype.Font("assets/PressStart.ttf",12)


    def load_states(self):
            Title(self).enter_state()

    def change_state(self, new_state):
        if self.state_stack:
            self.state_stack.pop()
        self.state_stack.append(new_state)

    def push_state(self, new_state):
        self.state_stack.append(new_state)

    def pop_state(self):
        if self.state_stack:
            self.state_stack.pop()

if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()
