import pygame
import random
from state import State

class Pond:
    def __init__(self, loc, fish):
        self.fish = fish
        self.center = loc
        self.x = self.center[0]
        self.y = self.center[1]
        self.size = 30
                
    def display(self, surface):
        pygame.draw.circle(surface, (173, 216, 230), self.center, self.size)
        text_surface, text_rect = pygame.font.Font(None, 24).render(str(self.fish), True, (0, 0, 0))
        text_rect.center = self.center
        surface.blit(text_surface, text_rect)

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
        
    def display(self, surface):
        pygame.draw.circle(surface, self.color, [int(self.pos[0]), int(self.pos[1])], self.size)
        
    def move_to_pond(self, delta_time):
        if not self.target_pond:
            return
        direction = pygame.math.Vector2(self.target_pond.x - self.pos[0], self.target_pond.y - self.pos[1])
        if direction.length() > 0:
            direction.normalize_ip()
            self.pos[0] += direction.x * 60 * delta_time
            self.pos[1] += direction.y * 60 * delta_time
        distance = pygame.math.Vector2(self.pos[0] - self.target_pond.x, self.pos[1] - self.target_pond.y).length()
        if distance < self.size + self.target_pond.size - 5:
            self.current_pond = self.target_pond
            return True
        return False

class FishSim(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.pond_color = (173, 216, 230)  #light blue
        self.player_color = (0, 128, 0)    #green
        self.ai_color = (255, 0, 59)       #red
        self.day = 1
        self.selfish_mode = False
        self.message = "Day 1: Choose your fishing strategy (1 for fair, S for selfish)"
        self.days_passed = 0
        self.game_over = False
        self.day_in_progress = False
        
        self.ponds = []
        self.fishermen = []
        self.player = None
        self.setup_game()
        self.daily_goal = 4

    def setup_game(self):
        pond_locations = [
            (self.game.GAME_W // 4, self.game.GAME_H // 3),
            (3 * self.game.GAME_W // 4, self.game.GAME_H // 3),
            (self.game.GAME_W // 4, 2 * self.game.GAME_H // 3),
            (3 * self.game.GAME_W // 4, 2 * self.game.GAME_H // 3)
        ]
        
        for loc in pond_locations:
            fish_count = random.randint(3, 8)
            self.ponds.append(Pond(loc, fish_count))
        
        player_x = self.game.GAME_W // 2
        player_y = self.game.GAME_H // 2
        self.player = Fisherman(player_x, player_y, self.player_color, is_player=True)
        self.fishermen.append(self.player)
        
        for i in range(5):
            x = random.randint(20, self.game.GAME_W - 20)
            y = random.randint(20, self.game.GAME_H - 20)
            self.fishermen.append(Fisherman(x, y, self.ai_color))
        
        self.assign_random_targets()
    
    def assign_random_targets(self):
        for fisherman in self.fishermen:
            if not fisherman.day_complete:
                fisherman.target_pond = random.choice(self.ponds)
    
    def update(self, delta_time):
        if self.game.selfishmode and not self.selfish_mode:
            self.selfish_mode = True
            self.message = "Selfish mode activated! All fishermen will take as many fish as possible."
            
        if self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.__init__(self.game)
            return
        
        if not self.day_in_progress:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_1]:
                self.selfish_mode = False
                self.day_in_progress = True
                self.message = "Day " + str(self.day) + " in progress: Taking 1 fish each"
            elif keys[pygame.K_s]:
                self.selfish_mode = True
                self.game.selfishmode = True
                self.day_in_progress = True
                self.message = "Day " + str(self.day) + " in progress: Taking as many fish as possible!"
            return
        
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
            self.message = f"GAME OVER: All fish are gone after {self.day} days! The ecosystem has collapsed."
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
        for fisherman in self.fishermen:
            fisherman.display(surface)
        self.draw_game_info(surface)
    
    def draw_game_info(self, surface):
        self.game.draw_text(surface, self.message, (0, 0, 0), self.game.GAME_W // 2, 20)
        player_text = f"Your fish: {self.player.fish_count}"
        self.game.draw_text(surface, player_text, (0, 0, 0), self.game.GAME_W // 2, 40)
        total_fish = sum(pond.fish for pond in self.ponds)
        fish_text = f"Fish remaining: {total_fish}"
        self.game.draw_text(surface, fish_text, (0, 0, 0), self.game.GAME_W // 2, 60)
        if self.game_over:
            self.game.draw_text(surface, "Press R to restart", (0, 0, 0), self.game.GAME_W // 2, self.game.GAME_H - 30)
