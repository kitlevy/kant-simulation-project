import arcade
import random
import math
import os

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Kantian Ethics Simulation"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "assets")

NUM_TREES = 5
NUM_AGENTS = 4
APPLE_REGEN_TIME = 180  # frames

class Tree(arcade.Sprite):
    def __init__(self, position):
        image_path = os.path.join(ASSET_PATH, "tree.png")
        super().__init__(image_path, 0.2)
        self.center_x, self.center_y = position
    def update(self):
        if self.apples < 3:
            self.regen_timer += 1
            if self.regen_timer >= APPLE_REGEN_TIME:
                self.apples += 1
                self.regen_timer = 0

class Agent(arcade.Sprite):
    def __init__(self, position, strategy):
        image_path = os.path.join(ASSET_PATH, "apple.png")
        super().__init__(image_path, 0.2)
        self.center_x, self.center_y = position
        self.strategy = strategy  # "kantian" or "selfish"
        self.target_tree = None
        self.speed = 1.5

    def update(self, tree_list):
        if not self.target_tree or self.target_tree.apples == 0:
            self.target_tree = self.choose_tree(tree_list)

        if self.target_tree:
            self.move_toward_target()
            if self.collides_with_sprite(self.target_tree):
                self.take_apples()

    def choose_tree(self, tree_list):
        trees_with_apples = [tree for tree in tree_list if tree.apples > 0]
        if trees_with_apples:
            return random.choice(trees_with_apples)
        return None

    def move_toward_target(self):
        if not self.target_tree:
            return
        dx = self.target_tree.center_x - self.center_x
        dy = self.target_tree.center_y - self.center_y
        angle = math.atan2(dy, dx)
        self.center_x += math.cos(angle) * self.speed
        self.center_y += math.sin(angle) * self.speed

    def take_apples(self):
        if self.strategy == "kantian":
            if self.target_tree.apples >= 1:
                self.target_tree.apples -= 1
        elif self.strategy == "selfish":
            self.target_tree.apples = 0
        self.target_tree = None

class KantianSim(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)

        self.tree_list = arcade.SpriteList()
        self.agent_list = arcade.SpriteList()

    def setup(self):
        for _ in range(NUM_TREES):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 100)
            tree = Tree((x, y))
            self.tree_list.append(tree)

        for i in range(NUM_AGENTS):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            strategy = "kantian" if i % 2 == 0 else "selfish"
            agent = Agent((x, y), strategy)
            self.agent_list.append(agent)

    def on_draw(self):
        arcade.start_render()
        self.tree_list.draw()
        self.agent_list.draw()

        # Draw apple count
        for tree in self.tree_list:
            arcade.draw_text(f"{tree.apples}", tree.center_x - 10, tree.center_y + 30,
                             arcade.color.WHITE, 14, bold=True)

    def on_update(self, delta_time):
        self.tree_list.update()
        for agent in self.agent_list:
            agent.update(self.tree_list)

if __name__ == "__main__":
    sim = KantianSim()
    sim.setup()
    arcade.run()
