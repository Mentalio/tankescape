import pygame
import sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
import math
import random
import json
import platform

coins_special = 0
coins_special_pure = 0

pygame.init()
pygame.mixer.init()
screen_width = 1280
screen_height = 736
current_height = pygame.display.Info().current_h
current_width = pygame.display.Info().current_w

window_info = pygame.display.get_desktop_sizes()
window_w = window_info[0][0]
window_h = window_info[0][1]

key_binds = []

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
clock = pygame.time.Clock()

selected_level = 1

player_dead = pygame.image.load('assets/player_dead.png')
player_dead = pygame.transform.scale(player_dead, (32, 32)).convert_alpha()

wall = pygame.image.load('assets/base_block.png')
wall = pygame.transform.scale(wall, (32, 32)).convert_alpha()

start_button = pygame.image.load('assets/start_game_button.png')
start_button = pygame.transform.scale(start_button, (500, 100)).convert_alpha()

floor_safe = pygame.image.load('assets/base_block_safe.png')
floor_safe = pygame.transform.scale(floor_safe, (32, 32)).convert_alpha()

floor_win = pygame.image.load('assets/base_block_win.png')
floor_win = pygame.transform.scale(floor_win, (32, 32)).convert_alpha()

rebirth_sphere = pygame.image.load('assets/rebirth_sphere.png')
rebirth_sphere = pygame.transform.scale(rebirth_sphere, (20, 20)).convert_alpha()


bg_menu = pygame.image.load('assets/background_menu.png')
bg_menu_draw = bg_menu

level_banner_1 = pygame.image.load('assets/item_button1.png')
level_banner_1 = pygame.transform.scale(level_banner_1, (300, 120)).convert_alpha()

level_banner_2 = pygame.image.load('assets/item_button2.png')
level_banner_2 = pygame.transform.scale(level_banner_2, (300, 120)).convert_alpha()

level_banner_3 = pygame.image.load('assets/item_button3.png')
level_banner_3 = pygame.transform.scale(level_banner_3, (300, 120)).convert_alpha()

confirm_button = pygame.image.load('assets/item_button_confirm.png')
confirm_button = pygame.transform.scale(confirm_button, (300, 90)).convert_alpha()

font = pygame.font.Font('assets/droid-sans.regular.ttf', 64)
font_sml = pygame.font.Font('assets/droid-sans.regular.ttf', 23)
font_lrg = pygame.font.Font('assets/droid-sans.regular.ttf', 128)

font_alt = pygame.font.Font('assets/libre.ttf', 64)

hunting_alert = pygame.mixer.Sound('assets/hunting_notification.mp3')

player = pygame.image.load('assets/tank.png')
radar_tank = pygame.image.load('assets/radar_tank.png')
sneak_tank = pygame.image.load('assets/sneak_tank.png')

select_blue = pygame.image.load('assets/select_blue.png')
select_blue = pygame.transform.scale(select_blue, (32, 32)).convert_alpha()

floor = pygame.image.load('assets/base_floor.png')
floor = pygame.transform.scale(floor, (32, 32)).convert_alpha()

hotbar_tank = pygame.transform.scale(player, (20, 20))
hotbar_tank_radar = pygame.transform.scale(radar_tank, (20, 20)).convert_alpha()

hotbar_tank_missile = pygame.transform.scale(pygame.image.load('assets/missile_tank.png'), (20, 20)).convert_alpha()

font_sml_h = font.render('QWERTYUIOPASDFGHJKLZXCVBNM', True, (255, 255, 255)).get_rect().h
research_points = pygame.image.load('assets/science.png')
research_points = pygame.transform.scale(research_points, (20, 20)).convert_alpha()

no = pygame.image.load('assets/nono.png')
no = pygame.transform.scale(no, (16, 16)).convert_alpha()

arrow = pygame.image.load('assets/arrow.png')
arrow = pygame.transform.scale(arrow, (64, 64)).convert_alpha()
arrow_left = arrow
arrow_right = pygame.transform.flip(arrow, True, False)

start_button_text = font.render('Start Game', True, (255, 255, 255))
start_button_text = pygame.transform.scale_by(start_button_text, 1)

main_menu_text = font_lrg.render('Tank Escape', True, (255, 255, 255))

mentalio = font_sml.render('A game by Mentalio', True, (255, 255, 255))

skins = []
shop_items = []
shop_items_classes = []
missiles = []
player_speed = 3
max_dashes = 1
hunt_frequency = 360
hunting_offset = 1
prompt_shop_item = None


def lerp(start, end, time):
    return start + (end - start) * time


def angle_to(angle_from, angle, step=5):
    angle_from %= 360
    angle %= 360

    diff_clockwise = (angle - angle_from) % 360
    diff_anticlockwise = (angle_from - angle) % 360

    if diff_clockwise < diff_anticlockwise:
        if diff_clockwise < step:
            angle_from = angle
        else:
            angle_from = (angle_from + step) % 360
    else:
        if diff_anticlockwise < step:
            angle_from = angle
        else:
            angle_from = (angle_from - step) % 360

    return angle_from


def skin(image_path: str):
    path_found = False
    global skins
    image_path = f'assets/{image_path}'
    for path in skins:
        if image_path in path:
            path_found = True
    if not path_found:
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (32, 32))
        skins.append([image_path, image])


def reset_data():
    global coins
    un_level_all()
    un_shop_all()
    shop_items_classes[16].unlocked = False
    shop_items_classes[1].unlocked = False
    shop_items_classes[3].unlocked = False
    shop_items_classes[4].unlocked = False
    shop_items_classes[6].unlocked = False
    shop_items_classes[7].unlocked = False
    shop_items_classes[9].unlocked = False
    shop_items_classes[10].unlocked = False
    skins.clear()
    skin('player_tank.png')
    coins = 0


def reset_data_full():
    global coins, coins_special, coins_special_pure
    un_level_all()
    un_shop_all()
    shop_items_classes[16].unlocked = False
    shop_items_classes[3].unlocked = False
    shop_items_classes[4].unlocked = False
    shop_items_classes[6].unlocked = False
    shop_items_classes[7].unlocked = False
    shop_items_classes[9].unlocked = False
    shop_items_classes[10].unlocked = False
    skins.clear()
    skin('player_tank.png')
    coins = 0
    coins_special = 0
    coins_special_pure = 0


def update_items():
    item_count = -1
    for item in shop_items_classes:
        item_count += 1
        if item.bought:
            if item.unlocked:
                global player_speed, dash_distance, hunting_offset, coins_special, coins_special_pure, max_dashes
                if item_count == 0:
                    max_dashes = 2
                    shop_items_classes[1].unlock()
                if item_count == 1:
                    max_dashes = 3
                if item_count == 2:
                    player_speed = 3.3
                    shop_items_classes[3].unlock()
                if item_count == 3:
                    player_speed = 3.8
                    shop_items_classes[4].unlock()
                if item_count == 4:
                    player_speed = 4.5
                if item_count == 5:
                    shop_items_classes[6].unlock()
                    dash_distance = 140
                if item_count == 6:
                    dash_distance = 150
                    shop_items_classes[7].unlock()
                if item_count == 7:
                    dash_distance = 170
                if item_count == 8:
                    shop_items_classes[9].unlock()
                    hunting_offset = 2
                if item_count == 9:
                    shop_items_classes[10].unlock()
                    hunting_offset = 2.5
                if item_count == 10:
                    hunting_offset = 3.5
                if item_count == 11:
                    skin('sneak_tank.png')
                if item_count == 12:
                    skin('radar_tank.png')
                if item_count == 13:
                    skin('healing_tank.png')
                if item_count == 14:
                    skin('tank.png')
                if item_count == 15:
                    skin('missile_tank.png')
                if item_count == 16:
                    coins_special_pure += 5
                    coins_special = coins_special_pure
                    reset_data()
                if item_count == 17:
                    skin('super_tank.png')
                if item_count == 18:
                    skin('drone_tank.png')


update_items()
skin('player_tank.png')

pygame.display.set_caption('Tank Escape')
pygame.display.set_icon(player)

enemies_count = 0
radar_enemies_count = 0
healer_enemies_count = 0
sneak_enemies_count = 0
missile_enemies_count = 0

characters = []
notifications = []

world_offset = [0, 0]

current_soundtrack = 0

level_names = {
    0: 'Humble beginnings',
    1: 'Broken base',
    2: 'Twisted turns',
    3: 'The long way out',
    4: 'The rumble road',
    5: 'No where is hidden',
    6: 'You can hide but you cant run',
    7: 'Meet the team',
    8: 'A balanced diet, with a long road',
    9: 'Fully ramped up',
    10: 'Legalise nuclear bombs',
    11: 'Twisted base A',
    12: 'Walls everywhere',
    13: 'Double Dash',
    14: 'Twisted base B',
    15: 'Humble Endings',
    16: 'The end...?'
}

soundtracks = {
    0: 'assets/st0.mp3',
    1: 'assets/st1.mp3',
    2: 'assets/st2.mp3',
}


def level_won():
    global coins
    coins += round((game_loaded + 1) ** 1.5, 2)


def play_soundtrack():
    if not pygame.mixer.music.get_busy():
        global current_soundtrack
        if current_soundtrack != len(soundtracks) - 1:
            current_soundtrack += 1
        else:
            current_soundtrack = 0
        pygame.mixer.music.load(soundtracks[current_soundtrack])
        pygame.mixer.music.play()


def load_json(filepath: str):
    json_file = None
    with open(filepath, 'r') as file:
        json_file = dict(json.load(file))
    global enemies_count
    global radar_enemies_count
    global healer_enemies_count
    global sneak_enemies_count
    global missile_enemies_count
    enemies_count = int(json_file['Normal'])
    radar_enemies_count = int(json_file['Radar'])
    healer_enemies_count = int(json_file['Healer'])
    sneak_enemies_count = int(json_file['Sneak'])
    missile_enemies_count = int(json_file['Missile'])
    return json_file['Player'], json_file['Enemy']


def blitset(surface, position):
    position_pointerless = [0, 0]
    if isinstance(position, pygame.rect.Rect):
        position_pointerless = [position.x + world_offset[0], position.y + world_offset[1], position.w, position.h]
    elif isinstance(position, list):
        position_pointerless = [position[0] + world_offset[0], position[1] + world_offset[1]]
    elif isinstance(position, tuple):
        position_pointerless = [position[0] + world_offset[0], position[1] + world_offset[1]]
    screen.blit(surface, position_pointerless)


class ShopItem:
    def __init__(self, name: str, cost, image: str, bought: bool, unlocked: bool, level: int):
        self.image_path = image
        self.name = name
        self.cost = cost
        self.image = pygame.transform.scale(pygame.image.load(image), (32, 32)).convert_alpha()
        self.bought = bought
        self.unlocked = unlocked
        self.highlighted_color = 0
        self.level = level
        if self.level == 0:
            self.image_banner = level_banner_1
        elif self.level == 1:
            self.image_banner = level_banner_2
        elif self.level == 2:
            self.image_banner = level_banner_3
        else:
            self.image_banner = pygame.Surface((0, 0))
        shop_items_classes.append(self)

    def lock(self):
        self.unlocked = False

    def unlock(self):
        if not self.unlocked:
            self.unlocked = True
            Notification(f'{self.name}\nUnlocked', False, self.image)

    def buy(self):
        global coins, coins_special, shop_items, shop_items_classes
        if self.level == 2:
            if coins_special >= self.cost:
                coins_special -= self.cost
                coins_special = round(coins_special, 2)

                self.bought = True
        else:
            if coins >= self.cost:
                coins -= self.cost
                coins = round(coins, 2)

                self.bought = True

    def draw(self, offset_x, offset_y):
        if not self.bought:
            if self.unlocked:
                global prompt_shop_item, shop_item_offset, mouse_pressed
                item_font = font_sml.render(self.name, True, (255, 255, 255))
                item_font_cost = font_sml.render(str(self.cost), True, (255, 255, 255))
                item_rect = pygame.Rect(0, 0, 300, 120)
                item_rect.center = (current_width / 2 + offset_x, offset_y + 48 + shop_item_offset)
                self.highlighted_color = 0
                if item_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    buy_prompt_rect_test = pygame.Rect(0, 0, 300, 90)
                    buy_prompt_rect_test.center = (current_width / 2, current_height - 100)
                    no_prompt_rect_test = pygame.Rect(0, 0, 16, 16)
                    if not buy_prompt_rect_test.collidepoint(mouse_pos[0], mouse_pos[1]) or not no_prompt_rect_test.collidepoint(mouse_pos[0], mouse_pos[1]):
                        self.highlighted_color = 20
                        if mouse_pressed:
                            prompt_shop_item = self
                banner_changed = self.image_banner.copy()
                banner_changed.fill((self.highlighted_color, self.highlighted_color, self.highlighted_color), special_flags=pygame.BLEND_RGB_ADD)
                screen.blit(banner_changed, item_rect)
                screen.blit(item_font, (
                    current_width / 2 - item_font.get_rect().w / 2 + offset_x, offset_y + shop_item_offset))
                screen.blit(item_font_cost, (
                    current_width / 2 - item_font_cost.get_rect().w - 5 + offset_x,
                    offset_y + 30 + shop_item_offset))
                if self.level == 2:
                    screen.blit(rebirth_sphere,
                                (current_width / 2 + 5 + offset_x, offset_y + 32 + shop_item_offset))
                else:
                    screen.blit(research_points,
                            (current_width / 2 + 5 + offset_x, offset_y + 32 + shop_item_offset))
                screen.blit(self.image, (
                    current_width / 2 - self.image.get_rect().w / 2 + offset_x, offset_y + 60 + shop_item_offset))


class Notification:
    def __init__(self, text: str, speaker: bool, image=None):
        self.text = text
        self.image = image
        self.speaker_enabled = speaker
        self.extended = False
        self.pos = [current_width - 350, 0]
        self.rect = pygame.Rect(0, 0, 300, 100)
        self.time = 0
        self.is_done = False  # New attribute to track completion

        # Scaling the image to fit inside the rectangle
        if self.image:
            self.image = pygame.transform.scale(self.image, (90, 90))  # Adjust the size as needed
        notifications.append(self)

    def draw(self):
        if not self.is_done:
            # Draw the rectangle
            pygame.draw.rect(screen, (20, 20, 20), self.rect)

            # Draw the image on the right side inside the rectangle
            if self.image:
                image_rect = self.image.get_rect()
                image_rect.midright = self.rect.midright
                image_rect.x -= 10  # Padding from the right edge
                screen.blit(self.image, image_rect)

            # Render and draw each line of text
            lines = self.text.splitlines()
            y_offset = 20  # Starting y-offset for the text
            for line in lines:
                text_surface = font_sml.render(line, True, (255, 255, 255))
                text_rect = text_surface.get_rect()
                text_rect.midleft = (self.rect.x + 10, self.rect.y + y_offset)
                screen.blit(text_surface, text_rect)
                y_offset += font_sml.get_height()  # Move to the next line position

    def update(self):
        if not self.is_done:
            self.time += 0.005
            self.rect.midbottom = self.pos
            if not self.extended:
                self.pos[1] = lerp(self.pos[1], 100, self.time)
            else:
                self.pos[1] = lerp(self.pos[1], 0, self.time)

            if self.time >= 1:
                self.time = 0
                self.extended = not self.extended

                # Set is_done to True when the notification retracts
                if not self.extended:
                    self.is_done = True

            self.draw()


class Pathfinder:
    image_path: str = ''
    npc_pos = [48, 48]
    hunting_icon = pygame.image.load('assets/hunting_icon.png').convert_alpha()
    hunting_icon = pygame.transform.scale(hunting_icon, (32, 32))
    seeking_icon = pygame.image.load('assets/seeking_icon.png').convert_alpha()
    seeking_icon = pygame.transform.scale(seeking_icon, (32, 32))

    def __init__(self, matrix):

        self.kill_radius = 20

        if not self.image_path:
            self.image_path = 'tank.png'

        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.select_surf = pygame.image.load('assets/select.png').convert_alpha()
        self.select_surf = pygame.transform.scale(self.select_surf, (32, 32))
        self.target_surf = pygame.image.load('assets/path_end.png').convert_alpha()
        self.target_surf = pygame.transform.scale(self.target_surf, (32, 32))

        self.hunting = False

        self.delay = 360

        self.idle_timer = 0
        self.target = None
        self.hunting_chance = 1
        self.hunting_chance_floor = 400
        self.seeking = False

        self.path = []

        self.spark_radius = 0

        # noinspection PyTypeChecker
        self.player = pygame.sprite.GroupSingle(Player(self.empty_path, self.image_path, self.npc_pos))

        if isinstance(self, Pathfinder) and not isinstance(self, Pathfinderplayer):
            while True:
                random_pos = (
                    random.randint(32, screen_width - 32) // 32 * 32, random.randint(32, screen_height - 32) // 32 * 32)
                pathfindable = self.create_path(random_pos)
                if pathfindable is not False:
                    self.player.sprite.pos = random_pos
                    self.player.sprite.direction = pygame.math.Vector2(0, 0)
                    self.player.sprite.rect.center = random_pos
                    break

        characters.append(self)

    def empty_path(self):
        self.path = []

    def draw_active_cell(self):
        mouse_pos = list(pygame.mouse.get_pos())
        mouse_pos = [mouse_pos[0] - world_offset[0], mouse_pos[1] - world_offset[1]]
        row = mouse_pos[1] // 32
        col = mouse_pos[0] // 32
        try:
            current_cell_value = self.matrix[row][col]
            if current_cell_value != 0:
                rect = pygame.rect.Rect((col * 32, row * 32), (32, 32))
                blitset(self.select_surf, rect)
        except:
            pass

    def create_path(self, ending):

        start_x, start_y = self.player.sprite.get_coord()

        if self.matrix[start_y][start_x] != 3:
            start = self.grid.node(start_x, start_y)

            ending_pos = list(ending)
            end_x, end_y = ending_pos[0] // 32, ending_pos[1] // 32
            try:
                end = self.grid.node(end_x, end_y)
            except:
                end = self.grid.node(1, 1)

            finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
            self.path, _ = finder.find_path(start, end, self.grid)
            self.grid.cleanup()
            self.player.sprite.set_path(self.path)
            self.target = (end_x * 32, end_y * 32)

            if len(self.path) == 0:
                return False

    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                x = (point.x * 32) + 16 + world_offset[0]
                y = (point.y * 32) + 16 + world_offset[1]
                points.append((x, y))
                pygame.draw.circle(screen, (50, 50, 50), (x, y), 1)
            if len(points) > 1:
                pygame.draw.lines(screen, (50, 50, 50), False, points, 3)

    def draw_target(self):
        if self.target:
            if self.player.sprite.collision_rects:
                blitset(self.target_surf, self.target)

    def draw_path_objects(self):
        self.draw_path()
        self.draw_target()

    def check_idle(self):
        if random.randint(0, 20 * self.hunting_chance) == 1:
            self.idle_timer = random.randint(self.delay, self.delay * 3)
            try:
                self.create_path([int(player.player.sprite.pos[0]), int(player.player.sprite.pos[1])])
            except:
                pass
            self.hunting = True
            hunting_alert.play()

        if self.hunting and self.idle_timer < 120:
            self.seeking = True
            if self.idle_timer % 10:
                try:
                    self.create_path([int(player.player.sprite.pos[0]), int(player.player.sprite.pos[1])])
                except:
                    pass
        else:
            self.seeking = False

        if self.idle_timer > 0:
            self.idle_timer -= 1
        else:
            self.hunting = False
            try:
                path_check = self.create_path((
                    random.randint(32 + world_offset[0], screen_width - 32 + world_offset[0]),
                    random.randint(32 + world_offset[1],
                                   screen_height - 32 + world_offset[1])))
                if path_check is not False:
                    self.idle_timer = random.randint(self.delay, self.delay * 3)
            except:
                pass

    def draw_hunting(self):
        # hunting_chance_render = font_sml.render(f'{str(self.hunting_chance)}', True, (255, 0, 0))
        # blitset(hunting_chance_render, [self.player.sprite.rect.center[0] - hunting_chance_render.get_rect().w / 2,
        # 						 self.player.sprite.rect.center[1] - 90])
        if self.hunting:
            if self.seeking:
                hunting_ai = self.seeking_icon
            else:
                hunting_ai = self.hunting_icon
            blitset(hunting_ai, [self.player.sprite.rect.center[0] - hunting_ai.get_rect().w / 2,
                                 self.player.sprite.rect.center[1] - 50])

    def update(self):
        self.hunting_chance = int(math.dist(self.player.sprite.pos, player.player.sprite.pos) * 0.5 * hunting_offset)
        if self.hunting_chance > self.hunting_chance_floor:
            self.hunting_chance = self.hunting_chance_floor
        global paused
        if not paused:
            self.check_idle()
        self.player.update()
        self.draw_hunting()
        self.player.sprite.draw()


class Pathfinderplayer(Pathfinder):
    image_path = 'player_tank.png'
    npc_pos = [screen_width - 48, screen_height - 48]

    def __init__(self, matrix):
        super().__init__(matrix)

    def create_path(self, ending):

        start_x, start_y = self.player.sprite.get_coord()

        start = self.grid.node(start_x, start_y)

        ending_pos = list(ending)
        end_x, end_y = ending_pos[0] // 32, ending_pos[1] // 32
        try:
            end = self.grid.node(end_x, end_y)
        except:
            end = self.grid.node(1, 1)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()
        self.player.sprite.set_path(self.path)
        self.target = (end_x * 32, end_y * 32)

        if len(self.path) == 0:
            return False

    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                x = (point.x * 32) + 16 + world_offset[0]
                y = (point.y * 32) + 16 + world_offset[1]
                points.append((x, y))
                pygame.draw.circle(screen, (50, 50, 50), (x, y), 1)
            if len(points) > 1:
                pygame.draw.lines(screen, (50, 50, 50), False, points, 3)

    def update(self):
        self.hunting_chance = int(math.dist(self.player.sprite.pos, player.player.sprite.pos) * 0.5 * hunting_offset)
        if self.hunting_chance > self.hunting_chance_floor:
            self.hunting_chance = self.hunting_chance_floor
        self.player.update()
        self.draw_active_cell()
        self.draw_path_objects()
        global player_speed
        self.player.sprite.speed = player_speed
        self.player.sprite.draw()


class Pathfinder_radar(Pathfinder):
    hunting_started = False
    image_path = 'radar_tank.png'
    npc_pos = [48, 48]

    def __init__(self, matrix):
        super().__init__(matrix)

    def update(self):
        self.hunting_chance = int(math.dist(self.player.sprite.pos, player.player.sprite.pos) * 0.5 * hunting_offset)
        if self.hunting_chance > self.hunting_chance_floor:
            self.hunting_chance = self.hunting_chance_floor
        self.player.sprite.speed = 1.5
        global paused
        if not paused:
            self.check_idle()
        self.player.update()

        self.draw_hunting()
        self.player.sprite.draw()

    def check_idle(self):
        if self.hunting and self.idle_timer % 10:
            path_check = self.create_path([int(player.player.sprite.pos[0]), int(player.player.sprite.pos[1])])
            if self.hunting_started:
                self.idle_timer = random.randint(self.delay * 1, self.delay * 2)
                self.hunting_started = False

        if self.idle_timer > 0:
            self.idle_timer -= 1
        else:
            self.hunting = False
            try:
                path_check = self.create_path((
                    random.randint(32 + world_offset[0], screen_width - 32 + world_offset[0]),
                    random.randint(32 + world_offset[1],
                                   screen_height - 32 + world_offset[1])))
                if path_check is not False:
                    self.idle_timer = random.randint(self.delay, self.delay * 3)
            except:
                pass

    def draw_hunting(self):
        if self.hunting:
            if self.seeking:
                hunting_ai = self.seeking_icon
            else:
                hunting_ai = self.hunting_icon
            blitset(hunting_ai, [self.player.sprite.rect.center[0] - hunting_ai.get_rect().w / 2,
                                 self.player.sprite.rect.center[1] - 50])


class Pathfinder_healer(Pathfinder):
    image_path = 'healing_tank.png'
    npc_pos = [48, 48]

    def __init__(self, matrix):
        super().__init__(matrix)

    def update(self):
        self.hunting_chance = int(math.dist(self.player.sprite.pos, player.player.sprite.pos) * 0.5 * hunting_offset)
        if self.hunting_chance > self.hunting_chance_floor:
            self.hunting_chance = self.hunting_chance_floor
        global paused
        if not paused:
            self.check_idle()
        self.player.update()
        self.draw_hunting()
        self.player.sprite.draw()

    def check_idle(self):
        if random.randint(0, 60 * self.hunting_chance * hunt_frequency) == 1:
            self.idle_timer = random.randint(int(self.delay / 2), self.delay)
            try:
                path_check = self.create_path([int(player.player.sprite.pos[0]), int(player.player.sprite.pos[1])])
            except:
                pass
            self.hunting = True
            hunting_alert.play()

        if self.hunting and self.idle_timer < 120 and self.idle_timer % 10:
            try:
                path_check = self.create_path([int(player.player.sprite.pos[0]), int(player.player.sprite.pos[1])])
            except:
                pass

        if self.idle_timer > 0:
            self.idle_timer -= 1
        else:
            self.hunting = False
            try:
                global characters
                healing_choice = random.choice(characters)
                path_check = self.create_path(
                    [int(healing_choice.player.sprite.pos[0]), int(healing_choice.player.sprite.pos[1])])
                if path_check is not False:
                    self.idle_timer = random.randint(int(self.delay / 2), self.delay)
            except:
                pass


class Pathfinder_sneak(Pathfinder):
    image_path = 'sneak_tank.png'
    npc_pos = [48, 48]

    def __init__(self, matrix):
        super().__init__(matrix)
        self.player.sprite.image_base.set_alpha(50)

    def draw_hunting(self):
        if self.hunting:
            if self.seeking:
                hunting_ai = self.seeking_icon
            else:
                hunting_ai = self.hunting_icon
            blitset(hunting_ai, [self.player.sprite.rect.center[0] - hunting_ai.get_rect().w / 2,
                                 self.player.sprite.rect.center[1] - 50])

    def update(self):
        self.hunting_chance = int(math.dist(self.player.sprite.pos, player.player.sprite.pos) * 0.5 * hunting_offset)
        if self.hunting_chance > self.hunting_chance_floor:
            self.hunting_chance = self.hunting_chance_floor
        global paused
        if not paused:
            self.player.update()
            self.check_idle()
        self.player.sprite.draw()
        self.draw_hunting()


class Pathfinder_missile(Pathfinder):
    missile_delay = 120
    image_path = 'missile_tank.png'
    npc_pos = [48, 48]

    def __init__(self, matrix):
        super().__init__(matrix)

    def shoot_missiles(self):
        if self.hunting:
            if self.missile_delay > 0:
                self.missile_delay -= 1
            else:
                Missile(self.player.sprite.pos)
                self.missile_delay = 120

    def draw_hunting(self):
        if self.hunting:
            hunting_ai = font_sml.render('LOCKED ON', True, 'pink')
            blitset(hunting_ai, [self.player.sprite.rect.center[0] - hunting_ai.get_rect().w / 2,
                                 self.player.sprite.rect.center[1] - 60])

    def check_idle(self):
        if random.randint(0, 5 * int(math.dist(self.player.sprite.pos, player.player.sprite.pos))) == 1:
            self.idle_timer = random.randint(self.delay, self.delay * 3)
            self.hunting = True
            hunting_alert.play()

        if self.idle_timer > 0:
            self.idle_timer -= 1
        else:
            self.hunting = False
            try:
                path_check = self.create_path((
                    random.randint(32 + world_offset[0], screen_width - 32 + world_offset[0]),
                    random.randint(32 + world_offset[1],
                                   screen_height - 32 + world_offset[1])))
                if path_check is not False:
                    self.idle_timer = random.randint(self.delay, self.delay * 3)
            except:
                pass

    def update(self):
        super().update()
        self.shoot_missiles()


class Player(pygame.sprite.Sprite):
    def __init__(self, empty_path, image_path: str, pos: list):

        super().__init__()
        image_path = f'assets/{image_path}'
        self.image_base = pygame.image.load(image_path)
        self.image_base = pygame.transform.scale(self.image_base, (32, 32)).convert_alpha()
        self.image = self.image_base
        self.rect = self.image.get_rect(center=(60, 60))

        self.pos = self.rect.center
        self.pos = pos
        self.speed = 3
        self.direction = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.current_angle = self.angle

        self.path = []
        self.collision_rects = []
        self.empty_path = empty_path

    def get_coord(self):
        col = self.rect.centerx // 32
        row = self.rect.centery // 32
        return (col, row)

    def set_path(self, path):
        self.path = path[1:]
        self.create_collision_rects()
        self.get_direction()

    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = (point.x * 32) + 16
                y = (point.y * 32) + 16
                rect = pygame.Rect((x - 4, y - 4), (8, 8))
                self.collision_rects.append(rect)

    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
            self.angle = round(self.direction.angle_to(pygame.math.Vector2(1, 0)))
        else:
            self.direction = pygame.math.Vector2(0, 0)
            self.path = []

    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.empty_path()

    def draw(self):
        blitset(self.image, self.rect)

    def get_pos(self):
        return self.pos

    def update(self):
        global paused
        if not paused:
            self.current_angle = angle_to(self.current_angle, self.angle)
            self.pos += self.direction * self.speed
            self.check_collisions()
            self.image = pygame.transform.rotate(self.image_base, self.current_angle)
            self.rect.center = self.get_pos()
            self.rect = self.image.get_rect(center=self.rect.center)


class Missile():
    def __init__(self, positon):
        self.pos = [positon[0], positon[1]]
        self.target = [player.player.sprite.pos[0] // 32 * 32 + 16, player.player.sprite.pos[1] // 32 * 32 + 16]
        self.target_image = pygame.transform.scale(pygame.image.load('assets/missile_lock.png'), (32, 32))
        self.image_base = pygame.transform.scale(pygame.image.load('assets/missile.png'), (32, 32))
        self.image_top = self.image_base
        self.image_bottom = pygame.transform.flip(self.image_base, False, True)
        self.image = self.image_top
        self.rect = pygame.rect.Rect(0, 0, 32, 32)
        self.rect.center = self.pos
        self.launching = True
        self.shot = False
        self.velocity = 40
        self.target_rect = pygame.rect.Rect(0, 0, 32, 32)
        self.target_rect.center = self.target
        missiles.append(self)

    def draw(self):
        blitset(self.target_image, ((self.target[0] // 32) * 32, (self.target[1] // 32) * 32))
        blitset(self.image, self.rect)

    def update(self):
        self.target_rect.center = self.target
        self.rect.center = self.pos
        self.draw()
        if self.launching:
            self.pos[1] -= self.velocity
            if self.pos[1] < -400:
                self.launching = False
                self.image = self.image_bottom
        else:
            self.pos[0] = self.target[0]
            self.pos[1] += self.velocity
            if self.pos[1] > self.target[1]:
                self.shot = True
        if self.shot:
            player_dist = math.dist(player.player.sprite.pos,
                                    [(self.target[0] // 32) * 32, (self.target[1] // 32) * 32])
            if player_dist <= 30:
                kill_player()
            missiles.remove(self)


class key_bind_manager:
    def __init__(self):
        global key_binds
        self.keys = key_binds

    def draw(self):
        key_offset = 0
        for key in self.keys:
            key.draw(key_offset)
            key_offset += 1


class key_bind:
    def __init__(self, name: str, key):
        self.name = name
        self.key = key
        global key_binds
        key_binds.append(self)
        self.rect = pygame.Rect(0, 0, 0, 0)

    def draw(self, key_offset):
        rect = pygame.Rect(10, key_offset * 50 + 10, 150, 50)
        self.rect = rect
        pygame.draw.rect(screen, (50, 50, 50), rect, 0, 8)

    def change_key(self, key):
        self.key = key

    def check_collision(self, key_pressed):
        if pygame.mouse.get_pressed():
            mouse_position = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_position[0], mouse_position[1]):
                self.change_key(key_pressed)

    def update(self, offset, key_pressed):
        self.check_collision(key_pressed)
        self.draw(offset)


with open('save.json', 'r') as file:
    json_loaded = dict(json.load(file))
    game_loaded = int(json_loaded['Level'])
    coins = round(float(json_loaded['Coins']), 2)
    coins_special = round(float(json_loaded['CoinsSpecial']), 2)
    coins_special_pure = round(float(json_loaded['CoinsSpecialPure']), 2)
    game_loaded_max = int(json_loaded['Level Unlocked'])
    for item in list(json_loaded['Shop']):
        ShopItem(str(item[0]), int(item[1]), str(item[2]), bool(item[3]), bool(item[4]), int(item[5]))

player_matrix, matrix_enemy = load_json(f'levels/{game_loaded}.json')

player = Pathfinderplayer(player_matrix)


def shop_all():
    for x in shop_items_classes:
        x.bought = True
    update_items()


def floor_all():
    for x in characters:
        if random.choice([False, True]):
            x.player.sprite.image_base = floor_win
        else:
            x.player.sprite.image_base = floor_safe


def level_all():
    global game_loaded_max, levels, level_names
    game_loaded_max = len(level_names) - 1
    levels = [f"{level_names[x]}, level {str(x)}" for x in range(game_loaded_max + 1)]


def un_level_all():
    global game_loaded_max, levels, level_names, game_loaded
    game_loaded_max = 0
    game_loaded = 0
    global player_matrix, matrix_enemy, dashes, max_dashes, death_points
    level_won()
    if game_loaded > game_loaded_max:
        game_loaded_max = game_loaded
    player_matrix, matrix_enemy = load_json(f'levels/{game_loaded}.json')
    dashes = max_dashes
    death_points = []
    reset()
    levels = [f"{level_names[x]}, level {str(x)}" for x in range(game_loaded_max + 1)]


def un_shop_all():
    for x in shop_items_classes:
        x.bought = False
    update_items()


for _ in range(enemies_count):
    Pathfinder(matrix_enemy)

for _ in range(healer_enemies_count):
    Pathfinder_healer(matrix_enemy)

for _ in range(radar_enemies_count):
    Pathfinder_radar(matrix_enemy)

for _ in range(sneak_enemies_count):
    Pathfinder_sneak(matrix_enemy)

for _ in range(missile_enemies_count):
    Pathfinder_missile(matrix_enemy)

shift_pressed = False
mouse_shift_pressed = False
buy_prompt = False
window_fullscreened = 0

win_points = []
hunting = []
ui_alpha = 0
ui_fade = 3
mouse_pressed = False
item = None
item_selected = None

level_name_alpha = 0
level_name_fade = 3
fullscreen = True
shop_opened = False
bought_item = None
player_image = None
dash_distance = 110
console_underscore = False
console_timer = 0
death_points = []
# def 110

mission = 'Get to the end without getting caught'

levels = [f"{level_names[x]}, level {str(x)}" for x in range(game_loaded_max + 1)]


def kill_player():
    global dashes, player_dead, player
    killed = False
    x = player.player.sprite.pos[0]
    y = player.player.sprite.pos[1]
    for row in range(len(player_matrix)):
        for col in range(len(player_matrix[row])):
            cell_value = player_matrix[row][col]
            if cell_value != 3 and x // 32 == col and y // 32 == row:
                killed = True
                break
        if killed:
            break
    if killed:
        death_points_pos = player.player.sprite.rect.topleft
        death_points_pos = list(death_points_pos)
        death_points_pos.append(pygame.transform.rotate(player_dead, random.randint(0, 360)))
        death_points.append(death_points_pos)
        player.player.sprite.path = []
        player.player.sprite.collision_rects = []
        player.player.sprite.target = [screen_width - 64, screen_height - 64]
        player.player.sprite.direction = pygame.math.Vector2(0, 0)
        player.player.sprite.pos = [screen_width - 64, screen_height - 64]
        dashes = max_dashes


def reset():
    global levels, death_points
    levels = [f"{level_names[x]}, level {str(x)}" for x in range(game_loaded_max + 1)]
    global enemies_count
    global radar_enemies_count
    global healer_enemies_count
    global sneak_enemies_count
    characters.clear()
    global player
    player = Pathfinderplayer(player_matrix)
    player.path.clear()
    player.player.sprite.collision_rects.clear()
    global level_name_alpha
    global level_name_fade
    level_name_alpha = 0
    level_name_fade = 3
    death_points = []

    for _ in range(enemies_count):
        Pathfinder(matrix_enemy)

    for _ in range(healer_enemies_count):
        Pathfinder_healer(matrix_enemy)

    for _ in range(radar_enemies_count):
        Pathfinder_radar(matrix_enemy)

    for _ in range(sneak_enemies_count):
        Pathfinder_sneak(matrix_enemy)

    for _ in range(missile_enemies_count):
        Pathfinder_missile(matrix_enemy)


dashes = max_dashes

running = True
paused = False
shop_item_offset = 0
game_started = False
tick = 100

new_width = screen_width
new_height = screen_height
size_changed = False
hover_color = (50, 50, 50)
console_error_timer = 0

update_items()
console_input = ''
console_open = False
console_errored = False
rebirth_available = False
rebirth_available_old = rebirth_available


def win_game():
    global game_loaded_max, game_loaded, player_matrix, matrix_enemy, dashes, max_dashes, death_points
    level_won()
    game_loaded += 1
    if game_loaded > game_loaded_max:
        game_loaded_max = game_loaded
    player_matrix, matrix_enemy = load_json(f'levels/{game_loaded}.json')
    dashes = max_dashes
    death_points = []
    reset()


while running:

    current_height = pygame.display.Info().current_h
    current_width = pygame.display.Info().current_w

    world_offset[0] = int((current_width - screen_width) / 2)
    world_offset[1] = int((current_height - screen_height) / 2)

    mouse_pos = pygame.mouse.get_pos()

    maximized = (current_width, current_height) == (window_w, window_h)

    if game_started:

        rebirth_available_old = rebirth_available

        coins = round(coins, 2)
        # world_offset = [-(player.player.sprite.pos[0] - current_width / 2), -(player.player.sprite.pos[1] - current_height / 2)]

        clock.tick(60)

        screen.fill((20, 20, 20))

        if game_loaded_max >= 16:
            rebirth_available = True

        if player_image:
            player.player.sprite.image_base = player_image

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('save.json', 'w') as file:
                    shop_items_save = []
                    for shop_i in shop_items_classes:
                        shop_items_save.append([shop_i.name, shop_i.cost, shop_i.image_path, shop_i.bought, shop_i.unlocked, shop_i.level])
                    file.write('{\n    "Level": %s,' % game_loaded)
                    file.write('\n    "Coins": %s,' % round(coins, 2))
                    file.write('\n    "CoinsSpecial": %s,' % round(coins_special, 2))
                    file.write('\n    "CoinsSpecialPure": %s,' % round(coins_special_pure, 2))
                    file.write('\n    "Shop": '), json.dump(shop_items_save, file, indent=2)
                    file.write(',')
                    file.write('\n    "Level Unlocked": %s\n}' % game_loaded_max)
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if console_open:
                    if event.key != pygame.K_RETURN:
                        if event.key != pygame.K_BACKSPACE:
                            console_input += event.unicode
                        else:
                            console_input = console_input[:-1]
                    else:
                        try:
                            exec(console_input)
                        except Exception:
                            console_errored = True
                            console_error_timer = 255
                            pass
                        console_input = ''
                if event.key == pygame.K_BACKQUOTE:
                    console_open = not console_open
                    console_input = ''
                if not console_open:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                if event.key == pygame.K_ESCAPE:
                    if not maximized:
                        if not fullscreen:
                            screen = pygame.display.set_mode((screen_height, screen_width), pygame.FULLSCREEN)
                            window_fullscreened = 255
                            fullscreen = True
                        elif fullscreen:
                            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                            window_fullscreened = 255
                            fullscreen = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
                if not paused:
                    if pygame.key.get_mods() and pygame.KMOD_SHIFT:
                        mouse_shift_pressed = True
                    else:
                        try:
                            player.create_path([event.pos[0] - world_offset[0], event.pos[1] - world_offset[1]])
                        except:
                            pass

        for row in range(len(player_matrix)):
            for col in range(len(player_matrix[row])):
                cell_value = player_matrix[row][col]
                if cell_value == 1:
                    blitset(floor, (col * 32, row * 32))
                elif cell_value == 2:
                    blitset(floor_win, (col * 32, row * 32))
                    win_points.append(pygame.rect.Rect(col * 32, row * 32, 32, 32))
                elif cell_value == 3:
                    blitset(floor_safe, (col * 32, row * 32))

        for death_pos in death_points:
            blitset(death_pos[2], [death_pos[0], death_pos[1]])

        for row in range(len(player_matrix)):
            for col in range(len(player_matrix[row])):
                cell_value = player_matrix[row][col]
                if cell_value == 0:
                    blitset(wall, (col * 32, row * 32))

        for char in characters:
            char.kill_radius = 20
            char_pos = char.player.sprite.pos
            if isinstance(char, Pathfinder_healer):
                healer_pos = char.player.sprite.pos
                pygame.draw.circle(screen, (255, 255, 255),
                                   [char_pos[0] + world_offset[0], char_pos[1] + world_offset[1]], 80, 1)
                for char_healed in characters:
                    if not isinstance(char_healed, Pathfinderplayer) and not isinstance(char_healed,
                                                                                        Pathfinder_healer):
                        char_selected_pos = char_healed.player.sprite.pos
                        distance = math.dist(char_selected_pos, healer_pos)
                        if distance <= 80:
                            char_healed.kill_radius = 50
                            pygame.draw.circle(screen, (255, 255, 255), [char_selected_pos[0] + world_offset[0],
                                                                         char_selected_pos[1] + world_offset[1]],
                                               char_healed.kill_radius, 1)

        for char in characters:
            if not isinstance(char, Pathfinderplayer):
                char_pos = char.player.sprite.pos
                char.delay = hunt_frequency
                player_offset_pos = player.player.sprite.pos
                distance = math.dist(char.player.sprite.pos, player_offset_pos)

                if distance <= char.kill_radius:
                    kill_player()
                if isinstance(char, Pathfinder_radar):
                    pygame.draw.circle(screen, (0, 255, 0),
                                       [char_pos[0] + world_offset[0], char_pos[1] + world_offset[1]],
                                       150, 1)
                    player_offset_pos = player.player.sprite.pos
                    distance = math.dist(char.player.sprite.pos, player_offset_pos)
                    if distance <= 150:
                        if not char.hunting:
                            char.hunting = True
                            char.hunting_started = True
                            hunting_alert.play()

            char.update()
            if char.hunting:
                hunting.append(char)

        for missile in missiles:
            missile.update()

        for win in win_points:
            if win.collidepoint(player.player.sprite.pos):
                win_game()

        play_soundtrack()

        if window_fullscreened > 0:
            window_fullscreened -= 3
        if platform.system() == 'Darwin':
            if pygame.key.get_mods() and pygame.KMOD_SHIFT:
                shift_pressed = True
        elif platform.system() == 'Windows':
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shift_pressed = True

        if shift_pressed and dashes > 0:
            mouse_pos = pygame.math.Vector2(mouse_pos)
            player_pos = pygame.math.Vector2(
                [player.player.sprite.pos[0] + world_offset[0], player.player.sprite.pos[1] + world_offset[1]])
            try:
                direction = (mouse_pos - player_pos).normalize()
            except Exception:
                direction = (mouse_pos - player_pos)
            player.player.sprite.angle = round(direction.angle_to(pygame.math.Vector2(1, 0)))
            end_x = player.player.sprite.pos[0] + dash_distance * math.cos(
                math.radians(direction.angle_to(pygame.math.Vector2(1, 0))))
            end_y = player.player.sprite.pos[1] - dash_distance * math.sin(
                math.radians(direction.angle_to(pygame.math.Vector2(1, 0))))

            pygame.draw.line(screen, '#2cc8f5', list(player_pos), (end_x + world_offset[0], end_y + world_offset[1]), 4)
            for row in range(len(player_matrix)):
                for col in range(len(player_matrix[row])):
                    cell_value = player_matrix[row][col]
                    if cell_value != 0 and end_x // 32 == col and end_y // 32 == row:
                        blitset(select_blue, (end_x // 32 * 32, end_y // 32 * 32))

            if mouse_shift_pressed:
                for row in range(len(player_matrix)):
                    for col in range(len(player_matrix[row])):
                        cell_value = player_matrix[row][col]
                        if cell_value != 0 and end_x // 32 == col and end_y // 32 == row:
                            player.player.sprite.path = []
                            player.player.sprite.collision_rects = []
                            player.player.sprite.direction = pygame.math.Vector2(0, 0)
                            player.player.sprite.pos = end_x // 32 * 32 + 16, end_y // 32 * 32 + 16
                            dashes -= 1

        ## UI ##
        pause_control = font_sml.render('Space to pause/see controls', True, (50, 50, 50))
        pause_control_rect = pause_control.get_rect()
        pause_control_rect.topright = [screen_width - 5, 2]
        screen.blit(pause_control, pause_control_rect)
        if paused:
            paused_surface = pygame.surface.Surface((current_width, current_height))
            paused_surface.fill((0, 0, 0))
            paused_surface.set_alpha(150)
            screen.blit(paused_surface, (0, 0))
            if not shop_opened:
                control_1 = font_sml.render('---Controls---', True, (255, 255, 255))
                control_2 = font_sml.render('Space to pause', True, (255, 255, 255))
                control_3 = font_sml.render('Click to move', True, (255, 255, 255))
                control_4 = font_sml.render('Shift click to dash', True, (255, 255, 255))
                control_5 = font_sml.render('Escape to toggle Fullscreen', True, (255, 255, 255))
                paused_render = font.render('Paused', True, (255, 255, 255))
                levels_render = [font_sml.render(x, True, (255, 255, 255)) for x in levels]
                screen.blit(control_1, (10, 10))
                screen.blit(control_2, (10, 40))
                screen.blit(control_3, (10, 70))
                screen.blit(control_4, (10, 100))
                screen.blit(control_5, (10, 130))
                screen.blit(paused_render, (
                    current_width / 2 - paused_render.get_rect().w / 2,
                    current_height / 2 - paused_render.get_rect().h / 2))
                offset = -20
                skin_offset = 450

                skin_render = font_sml.render('Skins', True, (255, 255, 255))
                screen.blit(skin_render, (26 - skin_render.get_rect().w / 2, skin_offset - 10))
                for sk in skins:
                    skin_offset += 36
                    skin_rect = pygame.Rect(10, skin_offset - sk[1].get_rect().w / 2, 32, 32)
                    if skin_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                        player_image = sk[1]
                    screen.blit(sk[1], skin_rect)

                for lev in range(len(levels_render)):
                    color = (255, 255, 255)
                    lvl = font_sml.render(levels[lev], True, color)
                    offset += 30
                    rect = lvl.get_rect()
                    rect.topleft = (current_width - lvl.get_rect().w - 10, offset)
                    rect.h += 4
                    if rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                        color = (255, 255, 0)
                        if mouse_pressed:
                            game_loaded = lev
                            player_matrix, matrix_enemy = load_json(f'levels/{game_loaded}.json')
                            dashes = max_dashes
                            reset()
                    lvl = font_sml.render(levels[lev], True, color)
                    screen.blit(lvl, (current_width - lvl.get_rect().w - 10, offset))

                arrow_left_rect = pygame.Rect(0, 0, 64, 64)
                arrow_left_rect.center = (96, current_height / 2)
                screen.blit(arrow_left, arrow_left_rect)
                menu_render = font_sml.render('Shop', True, (255, 255, 255))
                screen.blit(menu_render,
                            (arrow_left_rect.x + arrow_left_rect.w, current_height / 2 - menu_render.get_rect().h / 2))
                if mouse_pressed:
                    if arrow_left_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                        shop_opened = True

            else:
                update_items()
                offset_y = -30
                item_count = -1
                offset_x = -320
                for item in shop_items_classes:
                    if not item.bought:
                        if item.unlocked:
                            offset_y += 130
                            if offset_y >= current_height - 200:
                                offset_x += 320
                                offset_y = 100
                            item.draw(offset_x, offset_y)
                if prompt_shop_item:
                    color_prompt = 0
                    buy_prompt_rect = pygame.Rect(0, 0, 300, 90)
                    buy_prompt_rect.center = (current_width / 2, current_height - 100)
                    no_prompt_rect = pygame.Rect(0, 0, 16, 16)
                    no_prompt_rect.center = (buy_prompt_rect.right, buy_prompt_rect.top)
                    if no_prompt_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                        if mouse_pressed:
                            prompt_shop_item = None
                    if buy_prompt_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                        color_prompt = 20
                        if mouse_pressed:
                            prompt_shop_item.buy()
                            prompt_shop_item = None
                    if prompt_shop_item:
                        confirm_button_draw = confirm_button.copy()
                        confirm_button_draw.fill((color_prompt, color_prompt, color_prompt), special_flags=pygame.BLEND_RGB_ADD)
                        screen.blit(confirm_button_draw, buy_prompt_rect)
                        item_font_b = font_sml.render(f'Buy {prompt_shop_item.name}?', True, (255, 255, 255))
                        yes_font = font_sml.render('Yes', True, (0, 255, 0))
                        screen.blit(item_font_b, (current_width / 2 - item_font_b.get_rect().w / 2, current_height - 130))
                        screen.blit(yes_font, (current_width / 2 - yes_font.get_rect().w / 2, current_height - 100))
                        screen.blit(no, no_prompt_rect)

                shop_title = font.render('Shop', True, (255, 255, 255))
                screen.blit(shop_title, (current_width / 2 - shop_title.get_rect().w / 2, 20))

                arrow_right_rect = pygame.Rect(0, 0, 64, 64)
                arrow_right_rect.center = (current_width - 96, current_height / 2)
                shop_render = font_sml.render('Menu', True, (255, 255, 255))
                screen.blit(arrow_right, arrow_right_rect)
                screen.blit(shop_render, (
                    arrow_right_rect.x - shop_render.get_rect().w, current_height / 2 - shop_render.get_rect().h / 2))
                if mouse_pressed:
                    if arrow_right_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                        shop_opened = False

        ui_alpha += ui_fade
        if ui_alpha == 255 * 2:
            ui_fade = -ui_fade
        ui_mission = font_sml.render(mission, True, (255, 255, 255))
        ui_mission.set_alpha(ui_alpha)
        ui_dashes = font_sml.render(f'You only have: {dashes} Dashes.', True, (255, 255, 255))
        ui_dashes.set_alpha(ui_alpha - round(255 / 2))
        ui_good_luck = font_sml.render('Shift click to dash. Click to move', True, (255, 255, 255))
        ui_good_luck.set_alpha(ui_alpha - 255)
        ui_fullscreen = font_sml.render('Press Escape to toggle Fullscreen', True, (255, 255, 255))
        ui_fullscreen.set_alpha(window_fullscreened)
        screen.blit(ui_good_luck, (current_width / 2 - ui_good_luck.get_rect().w / 2, 75))
        screen.blit(ui_dashes, (current_width / 2 - ui_dashes.get_rect().w / 2, 50))
        screen.blit(ui_mission, (current_width / 2 - ui_mission.get_rect().w / 2, 25))
        screen.blit(ui_fullscreen, (current_width / 2 - ui_fullscreen.get_rect().w / 2, 25))

        hotbar = pygame.surface.Surface((current_width, 50))
        hotbar.fill((0, 0, 0))
        hotbar.set_alpha(70)
        dashes_screen = font_sml.render(f'Dashes left: {dashes}', True, (255, 255, 255))
        screen.blit(hotbar, (0, current_height - 50))
        screen.blit(dashes_screen, (
            current_width / 2 - dashes_screen.get_rect().w / 2, current_height - 25 - dashes_screen.get_rect().h / 2))
        offset = current_width / 2 - 50
        for hunt in hunting:
            offset -= 45
            color = (0, 0, 0)
            if isinstance(hunt, Pathfinder_radar):
                hotbar_tank_rotated = pygame.transform.rotate(hotbar_tank_radar, hunt.player.sprite.angle)
                color = (0, 255, 0)
            elif isinstance(hunt, Pathfinder_missile):
                hotbar_tank_rotated = pygame.transform.rotate(hotbar_tank_missile, hunt.player.sprite.angle)
                color = 'pink'
            elif isinstance(hunt, Pathfinder):
                hotbar_tank_rotated = pygame.transform.rotate(hotbar_tank, hunt.player.sprite.angle)
                color = (255, 0, 0)
            # noinspection PyUnboundLocalVariable
            screen.blit(hotbar_tank_rotated, (
                offset - hotbar_tank_rotated.get_rect().w / 2,
                current_height - 25 - hotbar_tank_rotated.get_rect().h / 2))
            pygame.draw.circle(screen, color, (offset, current_height - 25), 20, 1)
        fps = font_sml.render(f'{str(int(clock.get_fps()))} fps', True, (50, 50, 50))
        coins_render = font_sml.render(str(coins), True, (255, 255, 255))
        screen.blit(coins_render,
                    (current_width - 10 - coins_render.get_rect().w,
                     current_height - 25 - coins_render.get_rect().h / 2))
        screen.blit(research_points, (
            current_width - 35 - coins_render.get_rect().w, current_height - 25 - research_points.get_rect().h / 2))
        if coins_special_pure != 0:
            rebirth_render = font_sml.render(str(coins_special), True, (255, 255, 255))
            screen.blit(rebirth_render, [10 + rebirth_sphere.get_rect().w, current_height - 25 - rebirth_render.get_rect().h / 2])
            screen.blit(rebirth_sphere, [5, current_height - 25 - rebirth_sphere.get_rect().h / 2])
        screen.blit(fps, [5, 2])

        level_name_alpha += level_name_fade
        if level_name_alpha == 255:
            level_name_fade = -level_name_fade
        level_name_render = font.render(level_names[game_loaded], True, (255, 255, 255))
        level_number = font_sml.render(f'Level: {game_loaded}', True, (255, 255, 255))
        level_name_render.set_alpha(level_name_alpha)
        level_number.set_alpha(level_name_alpha)
        screen.blit(level_name_render, (
            current_width / 2 - level_name_render.get_rect().w / 2,
            current_height / 2 - level_name_render.get_rect().h / 2))
        screen.blit(level_number, (
            current_width / 2 - level_number.get_rect().w / 2, current_height / 2 - level_number.get_rect().h / 2 + 50))

        if console_open:
            console_timer += 1
            if console_timer >= 20:
                console_underscore = not console_underscore
                console_timer = 0
            if console_underscore:
                console_input_showed = console_input + '_'
            else:
                console_input_showed = console_input
            console_render = font_sml.render(console_input_showed, True, (255, 255, 255))
            console_rect = console_render.get_rect()
            console_rect.midleft = [5, current_height - 25]
            screen.blit(console_render, console_rect)
        if console_errored:
            if console_error_timer > 0:
                console_error_timer -= 2
            else:
                console_errored = False
            console_error_alpha = console_error_timer
            console_error_render = font_sml.render('Error could not process command', True, (255, 0, 0))
            console_error_render.set_alpha(console_error_alpha)
            screen.blit(console_error_render, [10, 10])

        for note in notifications:
            note.update()

        if rebirth_available_old != rebirth_available:
            shop_items_classes[16].unlock()

        win_points = []
        hunting = []
        shift_pressed = False
        mouse_shift_pressed = False
        mouse_pressed = False
    else:
        mouse_pressed = False
        if new_width != current_width or new_height != current_height:
            size_changed = True
            new_width = current_width
            new_height = current_height
        if size_changed:
            bg_menu_draw = pygame.transform.scale(bg_menu, (current_width, current_height))
        screen.blit(bg_menu_draw, (0, 0))
        button_start = pygame.Rect(0, 0, 500, 100)
        button_start.center = (current_width / 2, current_height - 120)
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, hover_color, button_start, 0, 30)
        screen.blit(start_button_text, (current_width / 2 - start_button_text.get_rect().w / 2,
                                        current_height - 120 - start_button_text.get_rect().h / 2))
        screen.blit(main_menu_text, (current_width / 2 - main_menu_text.get_rect().w / 2, 10))
        screen.blit(mentalio, (current_width / 2 - mentalio.get_rect().w / 2, 150))
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_ESCAPE:
                    if not maximized:
                        if not fullscreen:
                            screen = pygame.display.set_mode((screen_height, screen_width), pygame.FULLSCREEN)
                            window_fullscreened = 255
                            fullscreen = True
                        elif fullscreen:
                            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                            window_fullscreened = 255
                            fullscreen = False
        hover_color = (50, 50, 50)
        if button_start.collidepoint(mouse_pos):
            hover_color = (100, 150, 100)
            if mouse_pressed:
                game_started = True

    pygame.display.flip()
