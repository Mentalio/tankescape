import pygame, sys, json

pygame.init()
pygame.mixer.init()
screen_width = 1280
screen_height = 736
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

selection = pygame.image.load('assets/select.png')
selection = pygame.transform.scale(selection, (32, 32))

name = input('Load or create level: ')
font = pygame.font.Font('assets/Handjet-Regular.ttf', 16)

main_st = pygame.mixer.music.load('assets/st0.mp3')

grid = [[1 for _ in range(40)] for _ in range(23)]

grid_player = [[1 for _ in range(40)] for _ in range(23)]

grid_enemy = [[1 for _ in range(40)] for _ in range(23)]

Tanks = [0, 0, 0, 0, 0]

try: 
    open(f'levels/{name}.json', 'r')
    with open(f'levels/{name}.json', 'r') as file:
        json_test_loaded = dict(json.load(file))
        grid_player = json_test_loaded['Player']
        grid_enemy = json_test_loaded['Enemy']
        Tanks[0] = json_test_loaded['Healer']
        Tanks[1] = json_test_loaded['Normal']
        Tanks[2] = json_test_loaded['Radar']
        Tanks[3] = json_test_loaded['Sneak']
        Tanks[4] = json_test_loaded['Missile']
except:
    pass

mouse_pressed = False

blocks = {
    0: pygame.transform.scale(pygame.image.load('assets/base_block.png'), (32, 32)),
    2: pygame.transform.scale(pygame.image.load('assets/base_block_win.png'), (32, 32)),
    3: pygame.transform.scale(pygame.image.load('assets/base_block_safe.png'), (32, 32))
}

map_select = 0

maps = {
    0: grid_player,
    1: grid_enemy
}

map_name = {
    0: 'Player grid',
    1: 'Enemy Grid'
}

selected_tank = 0

running = True
type = 0

copied_grid = grid

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Tanks[selected_tank] += 1
            if event.key == pygame.K_DOWN:
                if Tanks[selected_tank] > 0:
                    Tanks[selected_tank] -= 1

            if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_META or event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_ALT:
                copied_grid = map_selected
            if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_META or event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_ALT:
                grid_pointerless_row = []
                grid_pointerless = []
                for col in copied_grid:
                    for row in col:
                        grid_pointerless_row.append(row)
                    grid_pointerless.append(grid_pointerless_row)
                    grid_pointerless_row = []
                maps[map_select] = grid_pointerless
            if event.key == pygame.K_ESCAPE:
                if map_select != 1:
                    map_select += 1
                else:
                    map_select -= 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_0]:
        type = 1
    if keys[pygame.K_1]:
        type = 0
    if keys[pygame.K_2]:
        type = 2
    if keys[pygame.K_3]:
        type = 3

    if keys[pygame.K_6]:
        selected_tank = 0
    if keys[pygame.K_7]:
        selected_tank = 1
    if keys[pygame.K_8]:
        selected_tank = 2
    if keys[pygame.K_9]:
        selected_tank = 3
    if keys[pygame.K_0]:
        selected_tank = 4

    mouse_pos = list(pygame.mouse.get_pos())
    screen.fill((0, 0, 0))

    mouse_pressed = pygame.mouse.get_pressed()[0]

    map_selected = maps[map_select]

    selected_render = font.render(f'Map Selected: {map_name[map_select]}', True, (255, 255, 255))

    for col in range(len(map_selected)):
        for row in range(len(map_selected[0])):
            cell = map_selected[col][row]
            pygame.draw.rect(screen, (255, 0, 0), (row * 32, col * 32, 32, 32), 1)
            if mouse_pressed and mouse_pos[0] // 32 == row and mouse_pos[1] // 32 == col:
                maps[map_select][col][row] = type
            if cell != 1:
                screen.blit(blocks[cell], (row * 32, col * 32))

    screen.blit(selected_render, (screen_width / 2 - selected_render.get_rect().w / 2, 10))
    screen.blit(selection, (mouse_pos[0] // 32 * 32, mouse_pos[1] // 32 * 32))

    Healer_count_render = font.render(f'Healer Tank Count: {Tanks[0]}', True, (255, 255, 255))
    Normal_count_render = font.render(f'Normal Tank Count: {Tanks[1]}', True, (255, 255, 255))
    Radar_count_render = font.render(f'Radar Tank Count: {Tanks[2]}', True, (255, 255, 255))
    Sneak_count_render = font.render(f'Sneak Tank Count: {Tanks[3]}', True, (255, 255, 255))
    Missile_count_render = font.render(f'Missile Tank Count: {Tanks[4]}', True, (255, 255, 255))

    screen.blit(Healer_count_render, ((screen_width / 6) * 1 - Healer_count_render.get_rect().w / 2, screen_height - 25))
    screen.blit(Normal_count_render, ((screen_width / 6) * 2 - Normal_count_render.get_rect().w / 2, screen_height - 25))
    screen.blit(Radar_count_render, ((screen_width / 6) * 3 - Radar_count_render.get_rect().w / 2, screen_height - 25))
    screen.blit(Sneak_count_render, ((screen_width / 6) * 4 - Sneak_count_render.get_rect().w / 2, screen_height - 25))
    screen.blit(Missile_count_render, ((screen_width / 6) * 5 - Missile_count_render.get_rect().w / 2, screen_height - 25))

    mouse_pressed = False

    pygame.display.flip()
    clock.tick(60)
            
with open(f'levels/{name}.json', 'w') as file:
    file.write('{\n    ')
    file.write('"Player": ')
    json.dump(maps[0], file)
    file.write(',\n    ')
    file.write('"Enemy": ')
    json.dump(maps[1], file)

    file.write(',\n    ')
    file.write('"Healer": ')
    file.write(str(Tanks[0]))
    file.write(',\n    ')
    file.write('"Normal": ')
    file.write(str(Tanks[1]))
    file.write(',\n    ')
    file.write('"Radar": ')
    file.write(str(Tanks[2]))
    file.write(',\n    ')
    file.write('"Sneak": ')
    file.write(str(Tanks[3]))
    file.write(',\n    ')
    file.write('"Missile": ')
    file.write(str(Tanks[4]))

    file.write('\n}')

pygame.quit()