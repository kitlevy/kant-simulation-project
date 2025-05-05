import pygame
import pygame.freetype
from pygame import gfxdraw
import random
from states.state import State
from text_utils import draw_centered_text, draw_smooth_circle

class Pond:
    def __init__(self, loc, fish, radius=30):
        self.fish = fish
        self.center = loc
        self.x = self.center[0]
        self.y = self.center[1]
        self.size = radius
        self.color = (173, 216, 230)

    def display(self, surface):
        draw_smooth_circle(surface, self.x, self.y, self.size, self.color)
        #pygame.draw.circle(surface, (173, 216, 230), self.center, self.size)

    def set_fish(self, num):
        self.fish += num

    def repopulate(self):
        new_fish = self.fish // 2
        self.fish += new_fish

class Fisherman:
    def __init__(self, x, y, color, is_player=False):
        self.pos = [x, y]
        self.color = color
        self.size = 10
        self.fish_count = 0
        self.current_pond = None
        self.target_pond = None
        self.is_player = is_player
        self.day_complete = False
        self.speed = 80
        
    def display(self, surface):
        draw_smooth_circle(surface, int(self.pos[0]), int(self.pos[1]), self.size, self.color)
        #pygame.draw.circle(surface, self.color, [int(self.pos[0]), int(self.pos[1])], self.size)
        
    def move_to_pond(self, delta_time):
        if not self.target_pond:
            return
        direction = pygame.math.Vector2(self.target_pond.x - self.pos[0], self.target_pond.y - self.pos[1])
        if direction.length() > 0:
            direction.normalize_ip()
            self.pos[0] += direction.x * self.speed * delta_time
            self.pos[1] += direction.y * self.speed * delta_time
        distance = pygame.math.Vector2(self.pos[0] - self.target_pond.x, self.pos[1] - self.target_pond.y).length()
        if distance < self.size + self.target_pond.size - 5:
            self.current_pond = self.target_pond
            return True
        return False

class Player(Fisherman):
    def __init__(self, x, y, color, is_player=True):
        self.pos = [x, y]
        self.color = color
        self.size = 10
        self.fish_count = 0
        self.current_pond = None
        self.target_pond = None
        self.is_player = is_player
        self.day_complete = False 


class FishSim(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.pond_color = (173, 216, 230)  #light blue
        self.player_color = (0, 128, 0)    #green
        self.ai_color = (255, 0, 59)       #red
        self.day = 1
        self.selfish_mode = False
        self.message = "You've just arrived in the village, and you're ready to get fishing!\n Press A to take just one fish per day\n Press S to take as many as you can"
        self.days_passed = 0
        self.game_over = False
        self.day_in_progress = False
        self.intro_mode = True
        self.fisher_count = 6
        
        self.ponds = []
        self.fishermen = []
        self.player = None
        self.setup_game()
        self.daily_goal = 4

    def setup_game(self):
        voffset = 16

        pond_locations = [
            (self.game.GAME_W // 4, self.game.GAME_H // 3 + voffset),
            (3 * self.game.GAME_W // 4, self.game.GAME_H // 3 + voffset),
            (self.game.GAME_W // 4, 2 * self.game.GAME_H // 3 + voffset),
            (3 * self.game.GAME_W // 4, 2 * self.game.GAME_H // 3 + voffset)
        ]
        rad = 40
        for loc in pond_locations:
            fish_count = random.randint(10, 20)
            self.ponds.append(Pond(loc, fish_count, rad))
        
        player_x = self.game.GAME_W // 2
        player_y = self.game.GAME_H // 2
        self.player = Fisherman(player_x, player_y, self.player_color, is_player=True)
        self.fishermen.append(self.player)

        edge_buffer = 20
        for i in range(self.fisher_count):
            x = random.randint(edge_buffer, self.game.GAME_W - edge_buffer)
            y = random.randint(edge_buffer, self.game.GAME_H - edge_buffer)
            self.fishermen.append(Fisherman(x, y, self.ai_color))
        
        self.assign_random_targets()
    
    def assign_random_targets(self):
        for fisherman in self.fishermen:
            if not fisherman.day_complete:
                fisherman.target_pond = random.choice(self.ponds)
                while fisherman.target_pond.fish == 0:
                    fisherman.target_pond = random.choice(self.ponds)
    
    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                from states.ending import Ending
                Ending(self.game).enter_state()
        elif self.intro_mode:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.intro_mode = False
                    self.selfish_mode = False
                    self.game.selfishmode = False
                    self.day_in_progress = True
                    self.message = "You've chosen to take just one fish per day!\n All the other fishermen in the village will also take one fish each per day.\n"
                elif event.key == pygame.K_s:
                    self.intro_mode = False
                    self.selfish_mode = True
                    self.game.selfishmode = True
                    self.day_in_progress = True
                    self.message = "You've chosen to take as many  fish as possible! But uh oh!\nAll the other fishermen in the village will also now take as many as they can.\n"

    def update(self, delta_time):
        if self.game.selfishmode and not self.selfish_mode:
            self.selfish_mode = True
            #self.message = "Selfish mode activated! All fishermen will take as many fish as possible."

        if not self.intro_mode or self.game_over:
            all_complete = True
            for fisherman in self.fishermen:
                if fisherman.day_complete:
                    continue
                    
                all_complete = False
                
                if fisherman.move_to_pond(delta_time):
                    pond = fisherman.current_pond
                    if pond.fish > 0:
                        if self.selfish_mode:
                            fish_to_take = min(pond.fish, self.daily_goal)
                        else:
                            fish_to_take = 1
                        
                        pond.set_fish(-fish_to_take)  # Subtract fish from pond
                        fisherman.fish_count += fish_to_take
                    
                    fisherman.day_complete = True
            
            if all_complete:
                self.end_day()
    
    def end_day(self):
        total_fish = sum(pond.fish for pond in self.ponds)
        
        if total_fish == 0:
            self.game_over = True
            self.message = f"GAME OVER: All fish are gone after {self.day} days! The ecosystem has collapsed.\nYour selfish behavior, when applied universally, caused the village to starve.\nDo better next time!"
            return

        elif not self.selfish_mode and self.day >= 7:
            self.game_over = True
            self.message = f"SUCCESS: You made it through the week with {total_fish} fish remaining!\nYou've been accepted into your new village, and your responsible moral\nbehavior has served as a model for the rest of the fishermen."
            return

        self.message = f"Day {self.day} complete! Player has {self.player.fish_count} fish total."
        for pond in self.ponds:
            pond.repopulate()
        
        self.day += 1
        for fisherman in self.fishermen:
            fisherman.day_complete = False
            fisherman.current_pond = None
        
        self.assign_random_targets()
        self.day_in_progress = False
    
    def render(self, surface):
        surface.fill((255, 255, 255))
        for pond in self.ponds:
            pond.display(surface)
            draw_centered_text(self.game.font, surface, str(pond.fish), (pond.center[0],pond.center[1] + 5), (0, 0, 0), line_height=16)
            #self.game.draw_text(surface, str(pond.fish), (0, 0, 0), pond.center[0], pond.center[1])
        for fisherman in self.fishermen:
            fisherman.display(surface)
        self.draw_game_info(surface)
    
    def draw_game_info(self, surface):
        message_height = 40
        draw_centered_text(self.game.font, surface, self.message, (self.game.GAME_W // 2, message_height), (0, 0, 0))

        #player_text = f"Your fish: {self.player.fish_count}"
        #draw_centered_text(self.game.font, surface, player_text, (self.game.GAME_W // 2, 100), (0,0,0))
        #self.game.draw_text(surface, player_text, (0, 0, 0), self.game.GAME_W // 2, 100)

        total_fish = sum(pond.fish for pond in self.ponds)
        fish_text = f"Fish remaining: {total_fish}"
        #self.game.draw_text(surface, fish_text, (0, 0, 0), self.game.GAME_W // 2, 120)
        if not self.intro_mode and not self.game_over and self.day > 1:
            draw_centered_text(self.game.font, surface, fish_text, (self.game.GAME_W // 2, message_height + 15), (0,0,0))

        draw_centered_text(self.game.font, surface, "Green = you", (50, self.game.GAME_H - 12), line_height=8, color=self.player_color)

        draw_centered_text(self.game.font, surface, "Red = other fishermen", (self.game.GAME_W - 85, self.game.GAME_H - 12), line_height=8, color=self.ai_color)

        if self.game_over:
            draw_centered_text(self.game.font, surface, "PRESS ENTER TO CONTINUE", (self.game.GAME_W // 2, self.game.GAME_H - 30), (0, 0, 0))
