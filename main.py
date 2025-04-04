import pygame
import pygame.freetype
import random
import map
import creature
import pickle
import item

# CONSTANTS
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
SPRITE_SIZE = 64
ITEM_SIZE = 64
INVENTORY_SLOT_BORDER = ITEM_SIZE//16
INVENTORY_SLOT_SIZE = ITEM_SIZE+INVENTORY_SLOT_BORDER*2
INVENTORY_UI_WIDTH = 12+(INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*8
INVENTORY_UI_HEIGHT = 12+(INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*5
FPS = 0
FONT_SIZE = 16
LIGHT_LEVEL = 175
MAP_WIDTH = 30
MAP_HEIGHT = 30
ROOMS = 2

# COLORS
BACKGROUND_COLOR = (30, 30, 30)
BORDER_COLOR_1 = (40, 40, 40)
BORDER_COLOR_2 = (166, 0, 255)
BORDER_COLOR_3 = (100, 100, 100)

rarity_colors = {
    "common": (200, 200, 200),
    "uncommon": (0, 175, 70),
    "rare": (0, 70, 255),
    "epic": (125, 0, 230),
    "legendary": (230, 160, 0)
}


def colorkey(surf, color):
    surf.set_colorkey(color)
    return surf

def mouse_over(rect, x, y):
    if rect.x <= x < rect.x + rect.width and rect.y <= y < rect.y + rect.height:
        return True
    return False

def generate_vision_tiles(vision_radius, player_x, player_y):
    for x in range(-vision_radius+player_x, vision_radius+1+player_x):
        for y in range(-vision_radius+player_y, vision_radius+1+player_y):
            yield [x, y]

# This function takes a Map object as an argument and displays it
def display_map(map, player_x, player_y, vision_radius, full=False):
    screen.fill((0, 0, 0))
    vision_tiles = [coord for coord in generate_vision_tiles(vision_radius, player_x, player_y)]
    if full:
        for y_tile in range(map.height):
            for x_tile in range(map.width):
                if map.map[y_tile][x_tile]["tile"] != 'void':
                    screen.blit(sprites[map.map[y_tile][x_tile]["tile"]], (x_tile * SPRITE_SIZE+camera_pos[0], y_tile * SPRITE_SIZE+camera_pos[1]))
                    if [x_tile, y_tile] not in vision_tiles:
                        screen.blit(dark_tile, [x_tile*SPRITE_SIZE+camera_pos[0], y_tile*SPRITE_SIZE+camera_pos[1]])
    else:
        for y_tile in range(player_y-vision_radius-1, min(player_y+vision_radius+2, map.height)):
            for x_tile in range(player_x - vision_radius - 1, min(player_x + vision_radius + 2, map.width)):
                if map.map[y_tile][x_tile]["tile"] == 'floor':
                    screen.blit(floor_surface, [x_tile * SPRITE_SIZE+camera_pos[0], y_tile * SPRITE_SIZE+camera_pos[1]])
                elif map.map[y_tile][x_tile]["tile"] == 'wall':
                    screen.blit(wall_surface, [x_tile * SPRITE_SIZE+camera_pos[0], y_tile * SPRITE_SIZE+camera_pos[1]])
                elif map.map[y_tile][x_tile]["tile"] == 'door':
                    screen.blit(door_surface, [x_tile * SPRITE_SIZE+camera_pos[0], y_tile * SPRITE_SIZE+camera_pos[1]])
                if [x_tile, y_tile] not in vision_tiles:
                    screen.blit(dark_tile, [x_tile*SPRITE_SIZE+camera_pos[0], y_tile*SPRITE_SIZE+camera_pos[1]])

# This function will update map inside a certain rectangle
def update_map(map, player_x, player_y, vision_radius, rect):
    vision_tiles = [coord for coord in generate_vision_tiles(vision_radius, player_x, player_y)]
    for y_tile in range(rect.y//32, (rect.y+rect.height)//32+1):
        for x_tile in range(rect.x//32, (rect.x+rect.width)//32+1):
            if x_tile >= map.width or y_tile >= map.height:
                continue
            if map.map[y_tile][x_tile]["tile"] == 'floor':
                screen.blit(floor_surface, [x_tile * SPRITE_SIZE+camera_pos[0], y_tile * SPRITE_SIZE+camera_pos[1]])
            elif map.map[y_tile][x_tile]["tile"] == 'wall':
                screen.blit(wall_surface, [x_tile * SPRITE_SIZE+camera_pos[0], y_tile * SPRITE_SIZE+camera_pos[1]])
            elif map.map[y_tile][x_tile]["tile"] == 'door':
                screen.blit(door_surface, [x_tile * SPRITE_SIZE+camera_pos[0], y_tile * SPRITE_SIZE+camera_pos[1]])
            elif map.map[y_tile][x_tile]["tile"] == 'void':
                screen.blit(void_surface, [x_tile * SPRITE_SIZE+camera_pos[0], y_tile * SPRITE_SIZE+camera_pos[1]])
            if [x_tile, y_tile] not in vision_tiles:
                screen.blit(dark_tile, [x_tile * SPRITE_SIZE+camera_pos[0], y_tile * SPRITE_SIZE+camera_pos[1]])



def display_UI(hp, max_hp, stamina, max_stamina, inventory=False):
    global screen, FONT_SIZE
    bar_thickness = 28 # must be more than font size
    border_width = 4
    point_width = 5
    health_background_color = (80, 0, 0)
    health_color = (190, 0, 0)
    stamina_background_color = (0, 80, 0)
    stamina_color = (0, 190, 0)
    experience_background_color = (80, 80, 0)
    experience_color = (160, 160, 0)

    # health
    pygame.draw.rect(screen, BACKGROUND_COLOR,
                     pygame.Rect(0, 0, max_hp*point_width+border_width*2, bar_thickness+2*border_width), int(border_width))
    pygame.draw.rect(screen, health_background_color, pygame.Rect(border_width, border_width, max_hp * point_width, bar_thickness))
    pygame.draw.rect(screen, health_color, pygame.Rect(border_width, border_width, hp*point_width, bar_thickness))
    font.render_to(screen,
                   (border_width + (bar_thickness - FONT_SIZE) // 2, border_width + (bar_thickness - FONT_SIZE) // 2),
                   f"{int(hp)}/{int(max_hp)}", (255, 255, 255))
    # Stamina bar render
    pygame.draw.rect(screen, BACKGROUND_COLOR,
                     pygame.Rect(0, bar_thickness+border_width, max_stamina * point_width + border_width*2, bar_thickness+2*border_width), border_width)  # Rect(coordx, coordy, width, height)
    pygame.draw.rect(screen, stamina_background_color, pygame.Rect(border_width, border_width*2+bar_thickness, max_stamina * point_width, bar_thickness))
    pygame.draw.rect(screen, stamina_color, pygame.Rect(border_width, border_width*2+bar_thickness, stamina * point_width, bar_thickness))
    font.render_to(screen,
                   (border_width + (bar_thickness - FONT_SIZE) // 2, bar_thickness + border_width*2 + (bar_thickness - FONT_SIZE) // 2),
                   f"{int(stamina)}/{int(max_stamina)}", (255, 255, 255))

    # Turn
    font.render_to(screen,
                   (SCREEN_WIDTH-100, 10), f"Turn: {int(turn)}", (255, 255, 255))
    # FPS
    font.render_to(screen,
                   (SCREEN_WIDTH - 100, 30), f"FPS: {round(clock.get_fps(), 2)}", (255, 255, 255))
    # Experience
    experience_rect = pygame.Rect(0, SCREEN_HEIGHT-12, SCREEN_WIDTH, 10)
    if mouse_over(experience_rect, mouse_x, mouse_y):
        pygame.draw.rect(screen, BACKGROUND_COLOR,
                         pygame.Rect(0, SCREEN_HEIGHT-24, SCREEN_WIDTH, 24), 4)
        pygame.draw.rect(screen, experience_background_color,
                         pygame.Rect(4, SCREEN_HEIGHT-20, SCREEN_WIDTH-8, 20))
        pygame.draw.rect(screen, experience_color,
                         pygame.Rect(4, SCREEN_HEIGHT-20, (SCREEN_WIDTH-8)*(player.experience/player.experience_for_level_up), 20))
        font_rect = font.get_rect(f"{int(player.experience)}/{int(player.experience_for_level_up)}")
        font.render_to(screen,
                       (SCREEN_WIDTH/2-font_rect.width/2, SCREEN_HEIGHT-18), f"{int(player.experience)}/{int(player.experience_for_level_up)}", (255, 255, 255))
        font.render_to(screen,
                       (4, SCREEN_HEIGHT-42), f"Level {player.level}", (255, 255, 255))
    else:
        pygame.draw.rect(screen, BACKGROUND_COLOR,
                         experience_rect, 4)
        pygame.draw.rect(screen, experience_background_color,
                         pygame.Rect(4, SCREEN_HEIGHT-8, SCREEN_WIDTH-8, 8))
        pygame.draw.rect(screen, experience_color,
                         pygame.Rect(4, SCREEN_HEIGHT-8, (SCREEN_WIDTH-8)*(player.experience/player.experience_for_level_up), 8))
        font.render_to(screen,
                       (4, SCREEN_HEIGHT - 28), f"Level {player.level}", (255, 255, 255))

    # Inventory display
    if inventory:
        # Border drawing
        pygame.draw.rect(screen, BORDER_COLOR_3,
                         pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT, INVENTORY_UI_WIDTH, INVENTORY_UI_HEIGHT))
        pygame.draw.rect(screen, BORDER_COLOR_1,
                         pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH+4, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT+4, INVENTORY_UI_WIDTH+4, INVENTORY_UI_HEIGHT+4))
        pygame.draw.rect(screen, BACKGROUND_COLOR,
                         pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH+8, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT+8, INVENTORY_UI_WIDTH+8, INVENTORY_UI_HEIGHT+8))
        # Slots draw
        for x in range(player.inventory_size//5):
            for y in range(5):
                screen.blit(inventory_slot, (SCREEN_WIDTH - INVENTORY_UI_WIDTH+12 + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER) * x, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT+12 + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER) * y))
        # Items draw
        x = 0
        y = 0
        for item1 in player.inventory:
            pygame.draw.rect(screen, rarity_colors[item1.rarity],
                             pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH+12 + INVENTORY_SLOT_BORDER + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER) * x,
                                         SCREEN_HEIGHT - INVENTORY_UI_HEIGHT+12 + INVENTORY_SLOT_BORDER + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER) * y,
                                         INVENTORY_SLOT_SIZE-8, INVENTORY_SLOT_SIZE-8), 4)
            screen.blit(sprites[item1.name], (SCREEN_WIDTH - INVENTORY_UI_WIDTH+12 + INVENTORY_SLOT_BORDER + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER) * x,
                                             SCREEN_HEIGHT - INVENTORY_UI_HEIGHT+12 + INVENTORY_SLOT_BORDER + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER) * y))
            x += 1
            if x >= 8:
                x = 0
                y += 1
        # Equipment draw
        # Borders
        pygame.draw.rect(screen, BORDER_COLOR_3,
                         pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 20, INVENTORY_UI_WIDTH, INVENTORY_SLOT_SIZE+20))
        pygame.draw.rect(screen, BORDER_COLOR_1,
                         pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH + 4, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 16,
                                     INVENTORY_UI_WIDTH, INVENTORY_SLOT_SIZE+16))
        pygame.draw.rect(screen, BACKGROUND_COLOR,
                         pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH + 8, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 12,
                                     INVENTORY_UI_WIDTH, INVENTORY_SLOT_SIZE+8))
        # Slots
        screen.blit(sprites["main_hand_slot"], (SCREEN_WIDTH-INVENTORY_UI_WIDTH+12, SCREEN_HEIGHT-INVENTORY_UI_HEIGHT-INVENTORY_SLOT_SIZE-8))
        if player.equipment["main_hand"] != None:
            screen.blit(sprites[player.equipment["main_hand"].name], (SCREEN_WIDTH-INVENTORY_UI_WIDTH+16, SCREEN_HEIGHT-INVENTORY_UI_HEIGHT-INVENTORY_SLOT_SIZE-4))
            pygame.draw.rect(screen, rarity_colors[player.equipment["main_hand"].rarity],
                             pygame.Rect(SCREEN_WIDTH-INVENTORY_UI_WIDTH+16, SCREEN_HEIGHT-INVENTORY_UI_HEIGHT-INVENTORY_SLOT_SIZE-4,
                                         INVENTORY_SLOT_SIZE-8, INVENTORY_SLOT_SIZE-8), 4)

        screen.blit(sprites["off_hand_slot"], (
        SCREEN_WIDTH - INVENTORY_UI_WIDTH + INVENTORY_SLOT_SIZE + INVENTORY_SLOT_BORDER + 12, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 8))
        if player.equipment["off_hand"] != None:
            screen.blit(sprites[player.equipment["off_hand"].name], (SCREEN_WIDTH - INVENTORY_UI_WIDTH + INVENTORY_SLOT_SIZE + INVENTORY_SLOT_BORDER + 16,
                                                                     SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4))
            pygame.draw.rect(screen, rarity_colors[player.equipment["off_hand"].rarity],
                             pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH + INVENTORY_SLOT_SIZE + INVENTORY_SLOT_BORDER + 16,
                                                                     SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4,
                                         INVENTORY_SLOT_SIZE-8, INVENTORY_SLOT_SIZE-8), 4)

        screen.blit(sprites["glove_slot"], (
        SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*2 + 12, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 8))
        if player.equipment["gloves"] != None:
            screen.blit(sprites[player.equipment["gloves"].name], (SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*2 + 16, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4))
            pygame.draw.rect(screen, rarity_colors[player.equipment["gloves"].rarity],
                             pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*2 + 16, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4,
                                         INVENTORY_SLOT_SIZE-8, INVENTORY_SLOT_SIZE-8), 4)

        screen.blit(sprites["head_slot"], (
        SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*3 + 12, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 8))
        if player.equipment["head"] != None:
            screen.blit(sprites[player.equipment["head"].name], (SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*3 + 16, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4))
            pygame.draw.rect(screen, rarity_colors[player.equipment["head"].rarity],
                             pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*3 + 16, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4,
                                         INVENTORY_SLOT_SIZE-8, INVENTORY_SLOT_SIZE-8), 4)

        screen.blit(sprites["torso_slot"], (
        SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*4 + 12, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 8))
        if player.equipment["torso"] != None:
            screen.blit(sprites[player.equipment["torso"].name], (SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*4 + 16, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4))
            pygame.draw.rect(screen, rarity_colors[player.equipment["torso"].rarity],
                             pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*4 + 16, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4,
                                         INVENTORY_SLOT_SIZE-8, INVENTORY_SLOT_SIZE-8), 4)

        screen.blit(sprites["legs_slot"], (
        SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*5 + 12, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 8))
        if player.equipment["legs"] != None:
            screen.blit(sprites[player.equipment["legs"].name], (SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*5 + 16, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4))
            pygame.draw.rect(screen, rarity_colors[player.equipment["legs"].rarity],
                             pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*5 + 16, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4,
                                         INVENTORY_SLOT_SIZE-8, INVENTORY_SLOT_SIZE-8), 4)

        screen.blit(sprites["feet_slot"], (
        SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*6 + 12, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 8))
        if player.equipment["feet"] != None:
            screen.blit(sprites[player.equipment["feet"].name], (SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*6 + 16, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4))
            pygame.draw.rect(screen, rarity_colors[player.equipment["feet"].rarity],
                             pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*6 + 16, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4,
                                         INVENTORY_SLOT_SIZE-8, INVENTORY_SLOT_SIZE-8), 4)

        screen.blit(sprites["back_slot"], (
        SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*7 + 12, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 8))
        if player.equipment["back"] != None:
            screen.blit(sprites[player.equipment["back"].name], (SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*7 + 16, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4))
            pygame.draw.rect(screen, rarity_colors[player.equipment["back"].rarity],
                             pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH + (INVENTORY_SLOT_SIZE+INVENTORY_SLOT_BORDER)*7 + 16, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT - INVENTORY_SLOT_SIZE - 4,
                                         INVENTORY_SLOT_SIZE-8, INVENTORY_SLOT_SIZE-8), 4)

        # Tooltip drawing
        if mouse_over(pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT, INVENTORY_UI_WIDTH, INVENTORY_UI_HEIGHT), mouse_x, mouse_y):  #check if the mouse is on the inventory! not equipment for optimisation
            for row in range(5):
                if mouse_over(pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH + 12, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT + 12 + 76*row, INVENTORY_UI_WIDTH, 76), mouse_x, mouse_y): # check if the mouse is on the needed row
                    print(row)
                    for slot in range(player.inventory_size//5):  # Iterate through slots in the row
                        if mouse_over(pygame.Rect(SCREEN_WIDTH - INVENTORY_UI_WIDTH+16 + 76*slot, SCREEN_HEIGHT - INVENTORY_UI_HEIGHT+16 + 76 * row, 64, 64), mouse_x, mouse_y):  # Mouse is over the slot
                            if len(player.inventory) > slot+row*8:  # Item is in the slot
                                if player.inventory[slot].type == "weapon":  # Tooltip for weapons
                                    height_adjustment = 300 - min(300, (SCREEN_HEIGHT-mouse_y))
                                    width_adjustment = 300 - min(300, (SCREEN_WIDTH-mouse_x))
                                    pygame.draw.rect(screen, BORDER_COLOR_3,
                                                     pygame.Rect(mouse_x-width_adjustment, mouse_y-height_adjustment,
                                                                 300, 300))
                                    pygame.draw.rect(screen, BACKGROUND_COLOR,
                                                     pygame.Rect(mouse_x+4-width_adjustment, mouse_y+4-height_adjustment,
                                                                 292, 292))
                                    # Enchantments render
                                    frect = font.get_rect(f"{player.inventory[slot+row*8].title}")
                                    font.render_to(screen, (mouse_x+8-width_adjustment+143-frect.width/2, mouse_y+8-height_adjustment), f"{player.inventory[slot+row*8].title}", rarity_colors[player.inventory[slot+row*8].rarity])
                                    used = -1
                                    for ench in range(len(player.inventory[slot+row*8].enchantments)):
                                        font.render_to(screen, (mouse_x+8-width_adjustment, mouse_y+26+ench*18-height_adjustment), f"-{player.inventory[slot+row*8].enchantments[ench]}", (200, 200, 200))
                                        used = ench
                                    for ench in range(item.rarities.index(player.inventory[slot+row*8].rarity)-used-1):
                                        font.render_to(screen, (mouse_x+8-width_adjustment, mouse_y+26+(ench+used+1)*18-height_adjustment), "---Empty slot---", (100, 100, 100))
                                    # Stats render
                                    lines = 0
                                    for type in player.inventory[slot+row*8].damage.keys():
                                        font.render_to(screen, (mouse_x+8-width_adjustment, mouse_y+26+18*lines+item.rarities.index(player.inventory[slot+row*8].rarity)*18-height_adjustment), f"{type.capitalize()} damage: {player.inventory[slot+row*8].damage[type]}", (200, 200, 200))
                                        lines += 1
                                    font.render_to(screen, (mouse_x+8-width_adjustment, mouse_y+26+18*lines+item.rarities.index(player.inventory[slot+row*8].rarity)*18-height_adjustment),
                                                   f"Accuracy: {round(player.inventory[slot+row*8].accuracy*100)}%", (200, 200, 200))
                                    lines += 1
                                    font.render_to(screen, (mouse_x + 8 - width_adjustment,
                                                            mouse_y + 26 + 18 * lines + item.rarities.index(
                                                                player.inventory[
                                                                    slot + row * 8].rarity) * 18 - height_adjustment),
                                                   f"Strength need: {player.inventory[slot + row * 8].strength}",
                                                   (200, 200, 200))
                                    lines += 1
                                    font.render_to(screen, (mouse_x + 8 - width_adjustment,
                                                            mouse_y + 26 + 18 * lines + item.rarities.index(
                                                                player.inventory[
                                                                    slot + row * 8].rarity) * 18 - height_adjustment),
                                                   f"Level: {player.inventory[slot + row * 8].level}",
                                                   (200, 200, 200))

    # Log
    if attack_result != "Miss":
        dmg_string = []
        for type in damage_done.keys():
            dmg_string.append(f"{type} {round(damage_done[type], 2)}")
        string = "Done damage: " + " and ".join(dmg_string)
        font.render_to(screen, (4, SCREEN_HEIGHT-62), string, (255, 255, 255))
    else:
        font.render_to(screen, (4, SCREEN_HEIGHT-62), "Missed", (255, 255, 255))


def display_stats(stats, stats_bonus):
    # Draw borders
    pygame.draw.rect(screen, BORDER_COLOR_1,
                     pygame.Rect(SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 300, 400, 600), 6)
    pygame.draw.rect(screen, BORDER_COLOR_2,
                     pygame.Rect(SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 300, 400, 600), 3)
    pygame.draw.rect(screen, BORDER_COLOR_3,
                     pygame.Rect(SCREEN_WIDTH / 2 - 200, SCREEN_HEIGHT / 2 - 300, 400, 600), 1)
    # Draw corners
    screen.blit(cornerTR, (SCREEN_WIDTH / 2 + 194, SCREEN_HEIGHT / 2 - 306))
    screen.blit(cornerTL, (SCREEN_WIDTH / 2 - 206, SCREEN_HEIGHT / 2 - 306))
    screen.blit(cornerBR, (SCREEN_WIDTH / 2 - 206, SCREEN_HEIGHT / 2 + 294))
    screen.blit(cornerBL, (SCREEN_WIDTH / 2 + 194, SCREEN_HEIGHT / 2 + 294))
    # Draw background
    pygame.draw.rect(screen, BACKGROUND_COLOR,
                     pygame.Rect(SCREEN_WIDTH/2-194, SCREEN_HEIGHT/2-294, 388, 588))
    # Print text
    font.render_to(screen,
                   (SCREEN_WIDTH / 2 - 192, SCREEN_HEIGHT / 2 - 292),
                   f"Health regen: {round(stats['health_regeneration']-stats_bonus['health_regeneration'], 2)}+{stats_bonus['health_regeneration']}", (255, 255, 255))
    font.render_to(screen,
                   (SCREEN_WIDTH / 2 - 192, SCREEN_HEIGHT / 2 - 272),
                   f"Stamina regen: {round(stats['stamina_regeneration'], 2)}", (255, 255, 255))
    font.render_to(screen,
                   (SCREEN_WIDTH / 2 - 192, SCREEN_HEIGHT / 2 - 252),
                   f"Dodge: {round(stats['dodge']*100, 2)}%", (255, 255, 255))
    font.render_to(screen,
                   (SCREEN_WIDTH / 2 - 192, SCREEN_HEIGHT / 2 - 232),
                   f"Accuracy: {round(stats['accuracy'] * 100, 2)}%", (255, 255, 255))
    font.render_to(screen,
                   (SCREEN_WIDTH / 2 - 192, SCREEN_HEIGHT / 2 - 212),
                   f"Melee damage: {round(stats['melee_weapon_damage']*100, 2)}%", (255, 255, 255))
    font.render_to(screen,
                   (SCREEN_WIDTH / 2 - 192, SCREEN_HEIGHT / 2 - 192),
                   f"Ranged damage: {round(stats['ranged_weapon_damage']*100, 2)}%", (255, 255, 255))
    font.render_to(screen,
                   (SCREEN_WIDTH / 2 - 192, SCREEN_HEIGHT / 2 - 172),
                   f"Crit chance: {round(stats['crit_chance']*100, 2)}%", (255, 255, 255))
    font.render_to(screen,
                   (SCREEN_WIDTH / 2 - 192, SCREEN_HEIGHT / 2 - 152),
                   f"Crit damage: {round(stats['crit_damage']*100, 2)}%", (255, 255, 255))

map = map.Map(MAP_WIDTH, MAP_HEIGHT, ROOMS, 7, 7, 1)

player = creature.Player(map.room_dictionary["room1"]["center"])
enemy = creature.Creature(map.room_dictionary["room2"]["center"])
turn = 0
camera_pos = [0, 0]


pygame.init()

clock = pygame.time.Clock()

font = pygame.freetype.Font("fonts\\pixel_font.TTF", FONT_SIZE)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
dark_tile = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE))
dark_tile.set_alpha(LIGHT_LEVEL)
dark_tile.fill((0, 0, 0))
screen.fill((255, 255, 255))
pygame.display.set_caption("dung_rogue")

# SPRITES
cornerTL = pygame.image.load("sprites\\ui\\corner.png").convert_alpha()
cornerTL.set_colorkey((255, 0, 255))
cornerTR = pygame.transform.rotate(cornerTL, 270)
cornerTR.set_colorkey((255, 0, 255))
cornerBL = pygame.transform.rotate(cornerTL, 180)
cornerBL.set_colorkey((255, 0, 255))
cornerBR = pygame.transform.rotate(cornerTL, 90)
cornerBR.set_colorkey((255, 0, 255))
axe_surface = pygame.image.load("sprites\\items\\hatchet.png").convert_alpha()
axe_surface = pygame.transform.scale(axe_surface, (ITEM_SIZE, ITEM_SIZE))
axe_surface.set_colorkey((255, 0, 255))
inventory_slot = pygame.image.load("sprites\\ui\\inv_slot.png").convert_alpha()
inventory_slot = pygame.transform.scale(inventory_slot, (INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE))
floor_surface = pygame.image.load("sprites\\map\\floor.png").convert_alpha()
floor_surface = pygame.transform.scale(floor_surface, (SPRITE_SIZE, SPRITE_SIZE))
wall_surface = pygame.image.load("sprites\\map\\wall.png").convert_alpha()
wall_surface = pygame.transform.scale(wall_surface, (SPRITE_SIZE, SPRITE_SIZE))
door_surface = pygame.image.load("sprites\\map\\door.png").convert_alpha()
door_surface = pygame.transform.scale(door_surface, (SPRITE_SIZE, SPRITE_SIZE))  # !!!!!!
void_surface = pygame.image.load("sprites\\map\\void.png").convert_alpha()
void_surface = pygame.transform.scale(void_surface, (SPRITE_SIZE, SPRITE_SIZE))
player_surface = pygame.image.load("sprites\\creatures\\player.png").convert_alpha()
player_surface = pygame.transform.scale(player_surface, (SPRITE_SIZE, SPRITE_SIZE))
player_surface.set_colorkey((255, 0, 255))
hand_slot = pygame.transform.scale(pygame.image.load("sprites\\ui\\hand_slot.png").convert_alpha(), (INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE))

sprites = {"hatchet": axe_surface,
           "dagger": door_surface,
           "hand_axe": colorkey(pygame.transform.scale(pygame.image.load("sprites\\items\\hand_axe.png").convert_alpha(), (ITEM_SIZE, ITEM_SIZE)), (255, 0, 255)),
           "war_axe": colorkey(pygame.transform.scale(pygame.image.load("sprites\\items\\war_axe.png").convert_alpha(), (ITEM_SIZE, ITEM_SIZE)), (255, 0, 255)),
           "nordic_axe": colorkey(pygame.transform.scale(pygame.image.load("sprites\\items\\nordic_axe.png").convert_alpha(), (ITEM_SIZE, ITEM_SIZE)), (255, 0, 255)),
           "main_hand_slot": hand_slot,
           "off_hand_slot": pygame.transform.flip(hand_slot, True, False),
           "head_slot": pygame.transform.scale(pygame.image.load("sprites\\ui\\head_slot.png").convert_alpha(), (INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)),
           "torso_slot": pygame.transform.scale(pygame.image.load("sprites\\ui\\torso_slot.png").convert_alpha(), (INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)),
           "legs_slot": pygame.transform.scale(pygame.image.load("sprites\\ui\\legs_slot.png").convert_alpha(), (INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)),
           "feet_slot": pygame.transform.scale(pygame.image.load("sprites\\ui\\feet_slot.png").convert_alpha(), (INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)),
           "back_slot": pygame.transform.scale(pygame.image.load("sprites\\ui\\back_slot.png").convert_alpha(), (INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)),
           "glove_slot": pygame.transform.scale(pygame.image.load("sprites\\ui\\glove_slot.png").convert_alpha(), (INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)),
           "floor": floor_surface,
           "wall": wall_surface,
           "door": door_surface,
           "void": void_surface}

# initial map drawing
screen.fill((0, 0, 0))
display_map(map, player.x, player.y, vision_radius=player.stats["vision_radius"], full=True)
pygame.display.flip()

stats_open = False
paused = False  # so that the player can't move while pause (inventory open or menu open for example)
inventory_open = False  # inventory open variable for consistency
game_active = True  # general game loop value
damage_done = 0
attack_result = "Miss"
while game_active:
    dt = clock.tick(FPS)
    # Checking for events
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_active = False
            elif event.key == pygame.K_UP and map.map[player.y-1][player.x]["tile"] != 'wall':
                player.addAction("moveUp")
            elif event.key == pygame.K_DOWN and map.map[player.y+1][player.x]['tile'] != "wall":
                player.addAction("moveDown")
            elif event.key == pygame.K_LEFT and map.map[player.y][player.x-1]['tile'] != "wall":
                player.addAction("moveLeft")
            elif event.key == pygame.K_RIGHT and map.map[player.y][player.x+1]['tile'] != "wall":
                player.addAction("moveRight")
            elif event.key == 98:  # key: "B"
                player.addBuff("health_regen_potion", 5)
                player.addExperience(400)
                player.addAttribute("strength", 1)
                player.addAttribute("vitality", 1)
                player.addAttribute("dexterity", 1)
                player.addAttribute("perception", 1)
            elif event.key == 113:  # key: "Q"
                attack_result = player.attack(enemy)
                if attack_result != "Miss":
                    damage_done = attack_result
                print(f"Enemy health: {round(enemy.health, 2)}")
            elif event.key == 115:  # key "S"
                if stats_open:
                    stats_open = False
                else:
                    stats_open = True
            elif event.key == 119: # key "W"
                player.addBuff("injury", 5)
            elif event.key == 101: # key "E"
                player.addBuff("stamina_regen_potion", 5)
            elif event.key == 114: # key "R"
                player.addBuff("strength", 5)
                print(player.attributes["strength"]+player.stats_bonus["strength"])
            elif event.key == 116: # key "T"
                player.equipment["main_hand"].addEnchantment("Frost")
                player.equipment["main_hand"].addEnchantment("Acid")
            elif event.key == 121: # key "Y"
                player.equipment["main_hand"].addEnchantment("Fire")
            elif event.key == 105: # key "I"
                if inventory_open:
                    inventory_open = False
                else:
                    inventory_open = True
            elif event.key == 97: # key "A"
                player.equipment["main_hand"].changeRarity("legendary")
                player.equipment["main_hand"].addEnchantment("Injuring")
            elif event.key == 100: # key "D"
                pass
            elif event.key == 102: # key "F"
                pass
            #print(event.key)  # for debug purposes

    if len(player.action_buffer) > 0:
        if player.action_buffer[0] == "moveUp":
            player.moveUp()
        elif player.action_buffer[0] == "moveDown":
            player.moveDown()
        elif player.action_buffer[0] == "moveLeft":
            player.moveLeft()
        elif player.action_buffer[0] == "moveRight":
            player.moveRight()
        turn += 1
        player.update()
        enemy.update()
        player.removeAction()

    # Mouse control
    mouse_actions = pygame.mouse.get_pressed()
    if mouse_actions[1]:
        camera_pos[0] += 1
        camera_pos[1] += 1

    # GRAPHICAL CONTROLS
    display_map(map, player.x, player.y, player.stats["vision_radius"], full=True)
    screen.blit(player_surface, [player.x*SPRITE_SIZE+camera_pos[0], player.y*SPRITE_SIZE+camera_pos[1]])  # Display player
    display_UI(player.health, player.stats["max_health"], player.stamina, player.stats["max_stamina"], inventory=inventory_open)

    if stats_open:
        display_stats(player.stats, player.stats_bonus)

    pygame.display.flip()

pygame.quit()
