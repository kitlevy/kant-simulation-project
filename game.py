import pygame
import pygame.freetype
import os, sys

from title import Title

class Game():
        def __init__(self):
            pygame.init()
            self.GAME_W,self.GAME_H = 480, 270
            self.SCREEN_WIDTH,self.SCREEN_HEIGHT = 960, 540
            self.game_canvas = pygame.Surface((self.GAME_W,self.GAME_H))
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,self.SCREEN_HEIGHT))
            self.running, self.playing = True, True
            self.state = "TITLE"
            self.selfishmode = False
            self.dt, self.prev_time = 0, 0
            self.state_stack = []
            self.load_assets()
            self.load_states()

        def game_loop(self):
            while self.playing:
                self.get_dt()
                self.get_events()
                self.update()
                self.render()

        def get_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.state == "TITLE":
                            self.state = "FISH_SIM"
                    if event.key == pygame.K_s:
                        self.selfishmode = True
    
        def update(self):
            self.state_stack[-1].update(self.dt)

        def render(self):
            self.state_stack[-1].render(self.game_canvas)
            # Render current state to the screen
            self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), (0,0))
            pygame.display.flip()


        def get_dt(self):
            now = time.time()
            self.dt = now - self.prev_time
            self.prev_time = now

        def draw_text(self, surface, text, color, x, y):
            text_surface = self.font.render(text, True, color)
            #text_surface.set_colorkey((0,0,0))
            text_rect = text_surface.get_rect()
            text_rect.center = (x, y)
            surface.blit(text_surface, text_rect)

        def load_assets(self):
            # Create pointers to directories 
            self.assets_dir = os.path.join("assets")
            self.font_dir = os.path.join(self.assets_dir, "font")
            self.font = pygame.freetype.Font("assets/calibri-bold.ttf", 36)
            
        def load_states(self):
            self.title_screen = Title(self)
            self.state_stack.append(self.title_screen)


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()
