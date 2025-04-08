import arcade

class MenuView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_BLUE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Kantian Ethics Simulator", 100, 400, arcade.color.WHITE, 36)
        arcade.draw_text("Press ENTER to start", 100, 300, arcade.color.LIGHT_GRAY, 24)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_view = SimulationView()
            self.window.show_view(game_view)

class SimulationView(arcade.View):
    def __init__(self):
        super().__init__()
        self.tree_list = arcade.SpriteList()
        self.agent_list = arcade.SpriteList()
        
    def on_draw(self):
        arcade.start_render()
        self.tree_list.draw()
        self.agent_list.draw()
        
    def on_update(self, delta_time):
        self.tree_list.update()
        for agent in self.agent_list:
            agent.update(self.tree_list)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(MenuView())
