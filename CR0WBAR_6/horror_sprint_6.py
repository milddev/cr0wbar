import arcade
import os

# --- Constants ---
SPRITE_SCALING_BOX = 0.5
SPRITE_SCALING_PLAYER = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "cr0wb4r"

# Physics
MOVEMENT_SPEED = 2
JUMP_SPEED = 10
GRAVITY = 0.5

# constants for left and right facing
PLAYER_TEXTURE_LEFT = 1
PLAYER_TEXTURE_RIGHT = 0
# ------------------

class GameView(arcade.View):
    def __init__(self):
        # Call the parent class initializer
        super().__init__()

        # Sprite lists
        self.wall_list = None

        # This variable holds our simple "physics engine"
        self.physics_engine = None

        # Bools for keys
        self.left_pressed = False
        self.right_pressed = False
        self.down_pressed = False
        self.up_pressed = False

        self.all_sprites_list = None

        self.window.set_mouse_visible(False)

        self.player_list = None
        self.player_sprite = None

        self.setup()
        
    def setup(self):

        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.AnimatedTimeSprite()
        self.player_sprite.texture_change_frames = 10
        self.player_sprite.textures = []

        #getting error for this no clue why
        for i in range (12):
            self.player_sprite.textures.append(arcade.load_texture("animations/man_idle_calm/spritesheet.png", x = i*258, y = 0, width = 256, height = 256, hit_box_algorithm="Simple"))

        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 79

        self.player_list.append(self.player_sprite)

        arcade.set_background_color(arcade.color.WHITE_SMOKE)

        self.map = arcade.tilemap.read_tmx('map/my-map.tmx')
        self.background = arcade.tilemap.process_layer(self.map, 'wall_wood', hit_box_algorithm='None', scaling = 0.3)

        # sprite list
        self.all_sprites_list = arcade.SpriteList()

        # Sprite lists
        self.wall_list = arcade.SpriteList()

        # Create the player
        self.player_sprite = Player()
        # Player pos
        self.all_sprites_list.append(self.player_sprite)

        # --- Place boxes inside a loop
        for x in range(-200, 800, 64):
            wall = arcade.Sprite("wall.png", SPRITE_SCALING_BOX)
            wall.center_x = x
            wall.center_y = -30
            self.wall_list.append(wall)

    def on_draw(self):
        arcade.start_render()

        self.background.draw()

        self.wall_list.draw()

        self.player_list.draw()

        self.all_sprites_list.draw()

    def on_key_press(self, key, modifiers):
        # Called whenever a key is pressed
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
    
    def update(self, delta_time):

        self.player_sprite.change_x = 0

        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
            self.player_sprite.facing_right = False
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED
            self.player_sprite.facing_right = True

        # Create the physics engine. Give it a reference to the player, and
        # the walls we can't run into.
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY)

        # Call update to move the sprite
        # If using a physics engine, call update on it instead of the sprite
        # list.
        
        self.physics_engine.update()

        self.all_sprites_list.update()
        
        self.player_list.update_animation()

    def on_mouse_press(self, _x, _y, _button, _modifers):
        game_view = OldHouse()
        game_view.setup()
        self.window.show_view(game_view)

class OldHouse(arcade.View):
    def on_show(self):
        self.map = arcade.tilemap.read_tmx('map/my-map_2.tmx')
        self.background = arcade.tilemap.process_layer(self.map, 'wall_wood_old', hit_box_algorithm='None', scaling = 0.3)
        
    def on_old_draw(self):
        arcade.start_render()

    def setup(self):
        pass

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.textures = []
        # Load a left facing texture and a right facing texture.
        # flipped_horizontally=True will mirror the image we load.
        player_texture = arcade.load_texture("player.png")
        self.textures.append(player_texture)
        player_texture = arcade.load_texture("player.png", flipped_horizontally=True)
        self.textures.append(player_texture)
        
        self.scale = SPRITE_SCALING_PLAYER

        #By default face right
        self.facing_right = True
        self.set_texture(PLAYER_TEXTURE_RIGHT)

        #make var to create facing right  = true, see if player faces right when starts, if keypress is left set to false etc

    def update(self):
        # Figure out if we should face left or right
        if self.facing_right:
            self.set_texture(PLAYER_TEXTURE_RIGHT)
        else:
            self.set_texture(PLAYER_TEXTURE_LEFT)

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()
