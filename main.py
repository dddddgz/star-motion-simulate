from __future__ import annotations

import pygame.mouse
import pyini
import os
import tkinter as tk
import tkinter.filedialog as fd
import numpy as np
from rich.console import Console
from math import isclose, dist
from time import sleep
from threading import Timer
from objects import *

pygame.init()
pygame.key.set_repeat(1000, 50)

# Constant of gravitation
G = 6

# current path
PATH = os.path.dirname(__file__)

# rich Console
console = Console()

d_id = 0

def disappear_message():
    global d_id
    Timer(1, disappear_function, args=[d_id]).start()
    d_id += 1

def disappear_function(real_id):
    try:
        while running and  message.text and d_id - 1 == real_id:
            message.text = message.text[:-1]
            sleep(0.05)
    except pygame.error:
        return

def get_distance(sprite1: Star, sprite2: Star):
    x1, x2 = sprite1.x, sprite2.x
    y1, y2 = sprite1.y, sprite2.y
    z1, z2 = sprite1.z, sprite2.z
    return dist((x1, y1, z1), (x2, y2, z2))

def move(t):
    sprites_to_delete = []
    for sprite1 in stars:
        sprite1: Star
        x1, y1, z1, vx1, vy1, vz1, m1 = sprite1.info
        ax1, ay1, az1 = 0, 0, 0
        if sprite1 in sprites_to_delete:
            continue
        for sprite2 in stars:
            sprite2: Star
            if sprite1 in sprites_to_delete or sprite2 in sprites_to_delete:
                break
            if sprite1 is sprite2:
                continue
            x2, y2, z2, vx2, vy2, vz2, m2 = sprite2.info
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1
            r = get_distance(sprite1, sprite2)
            if is_collide(sprite1, sprite2):
                heavier = sprite1 if sprite1.mass > sprite2.mass else sprite2
                lighter = sprite2 if heavier is sprite1 else sprite1
                sprites_to_delete.append(lighter)
                heavier.vx += lighter.vx
                heavier.vy += lighter.vy
                heavier.vz += lighter.vz
                temp = language["star"]["collide"] % (repr(heavier), repr(lighter))
                message.text = temp
                console.log(temp)
                del temp
                disappear_message()
                break
            f = G * m1 * m2 / (r ** 2)
            if isclose(f, 0):
                continue
            accel = f / m1
            ax1 += accel * (dx / r)
            ay1 += accel * (dy / r)
            az1 += accel * (dz / r)
        x, y, z = (
            x1 + vx1 * t + 0.5 * ax1 * (t ** 2),
            y1 + vy1 * t + 0.5 * ay1 * (t ** 2),
            z1 + vz1 * t + 0.5 * az1 * (t ** 2)
        )
        tempx, tempy, tempz = sprite1.x, sprite1.y, sprite1.z
        if not sprite1.locked:
            sprite1.x, sprite1.y, sprite1.z = x, y, z
            sprite1.vx = (x - tempx) / t
            sprite1.vy = (y - tempy) / t
            sprite1.vz = (z - tempz) / t
        sprite1.flush()
    for sprite in sprites_to_delete:
        stars.remove(sprite)
    for sprite in stars:
        sprite.add_to_trail()

def is_collide(sprite1, sprite2):
    """
    Check if 2 sprites is collided
    :param sprite1: sprite1
    :param sprite2: sprite2
    :return: None
    """
    r1, r2 = sprite1.radius, sprite2.radius
    return r1 + r2 > get_distance(sprite1, sprite2)

def get_desc(star):
    """
    Get the description surface of a star.
    :param star: Star object
    :return: A surface
    """
    surf = pygame.Surface((200, 150)).convert_alpha()
    surf.fill((64, 64, 128, 64))
    t1 = Config.font.render(language["description"]["name"] % star.name, False, (255, 255, 255))
    t2 = Config.font.render(language["description"]["x"] % star.x, False, (255, 255, 255))
    t3 = Config.font.render(language["description"]["y"] % star.y, False, (255, 255, 255))
    surf.blit(t1, (0, 0))
    surf.blit(t2, (0, t1.get_height()))
    surf.blit(t3, (0, t1.get_height() + t2.get_height()))
    return surf

def zoom(direction, each=0.02):
    """
    Zoom size
    :param direction: nagative (zoom out) / positive (zoom in) / zero (reset)
    :param each: zoom size
    :return: None
    """
    if direction > 0:
        Config.scale += each
        if Config.scale > 10:
            Config.scale = 10
    elif direction < 0:
        Config.scale -= each
        if Config.scale < 0.02:
            Config.scale = 0.02
    elif direction == 0:
        Config.scale = 1
    message.text = language["game"]["zoom"] % Config.scale
    disappear_message()

def change_view(move_x, move_y):
    """
    change view (rel)
    :param move_x: rel x
    :param move_y: rel y
    :return: None
    """
    Config.rel[0] += int(round(move_x))
    Config.rel[1] += int(round(move_y))
    message.text = language["game"]["rel"] % str(tuple(Config.rel))
    disappear_message()

def pause_game():
    """
    Change game pause status (paused or not paused)
    :return: None
    """
    Config.pause = not Config.pause

# Read main config file
with open("config/config.ini", "r", encoding="utf-8") as f:
    config = pyini.ConfigParser(f.read())

# Read config file with language
with open(f"config/language_{config['language']['default']}.ini", "r", encoding="utf-8") as f:
    language = pyini.ConfigParser(f.read())

# Window size
size = width, height = (1000, 1000)

# fps manager
clock:   pygame.time.Clock = pygame.time.Clock()
# MOUSEBUTTONDOWN + MOUSEMOTION = MOUSEDRAG
drag:    bool              = False

# Main screen
screen = pygame.display.set_mode(size)

# Tkinter window for save file
root = tk.Tk()
root.withdraw()

movement: number = 10
pygame.display.set_icon(pygame.image.load(config["window"]["icon"]))
pygame.display.set_caption(language["game"]["title"])
pygame.mouse.set_visible(False)

with open(f"simulation/{config['simulation']['file']}.simulation", "r", encoding="utf-8") as f:
    stars = eval(f.read())

message     : Message        = Message()
pause       : Button         = Button("pause.png" , pause_game, language["button"]["pause"])
follow      : Button         = Button("follow.png", None,       language["button"]["follow"])

showing     : Any           = None
showing_pos: tuple[int, ...]= (0, 0)
following   : Any           = None
screenshot  : bool          = False

mouse_normal: pygame.Surface = pygame.image.load("normal.png")
mouse_click : pygame.Surface = pygame.image.load("click.png")
mouse       : pygame.Surface = mouse_normal

running = True
while running:
    screen.fill((0, 0, 0))
    clock.tick(30)
    if not Config.pause:
        move(Config.speed)
    for star, trail in map(lambda xxx: (xxx, xxx.trail), stars):
        if len(trail) < 2:
            continue
        trail = list(map(
            lambda point: ((np.array(point[:2]) + np.array(Config.rel)) * Config.scale).tolist(), trail
        ))
        pygame.draw.lines(screen, star.color, False, trail, 2)
    stars.sort(key=lambda star: star.z)
    for star in stars:
        if showing:
            screen.blit(get_desc(showing), showing_pos)
        star: Star
        star.flush()
        image = star.image
        temp_scale = star.radius * 2 * Config.scale
        temp_scale *= max(1 - star.z / 1000, 0.02)
        temp_scale = (temp_scale, temp_scale)
        image = pygame.transform.scale(image, temp_scale)
        new_rect = pygame.Rect(star.rect.topleft, image.get_size())
        screen.blit(image, new_rect)
        screen.blit(star.text, new_rect.topright)
        pos = pygame.mouse.get_pos()
        if showing is None:
            # No star description is showing
            # Mouse hovered on it
            if new_rect.collidepoint(pos):
                # Draw description surface
                showing = star
                showing_pos = pos
        elif showing is star:
            if not (new_rect.collidepoint(pos) or pygame.Rect(showing_pos, (200, 150)).collidepoint(pos)):
                showing = None
    try:
        screen.blit(message.image, message.rect)
    except pygame.error:
        pass
    if screen.get_width() > width:
        # Pause/Resume button
        if Config.pause:
            pause.image = pygame.image.load("resume.png")
            pause.title = language["button"]["resume"]
        else:
            pause.image = pygame.image.load("pause.png")
            pause.title = language["button"]["pause"]
        screen.blit(pause.image, pause.rect)
        pos = pygame.mouse.get_pos()
        if pause.rect.collidepoint(pos):
            mouse = mouse_click
            screen.blit(pause.prompt, pos)
        else:
            mouse = mouse_normal
    if pygame.mouse.get_focused() != 0:
        pos = pygame.mouse.get_pos()
        if mouse == mouse_click:
            screen.blit(mouse, (pos[0] - 5, pos[1]))
        else:
            screen.blit(mouse, pos)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drag = True
            elif event.button == 3:
                show_rk = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drag = False
                if pause.rect.collidepoint(event.pos):
                    pause()
            elif event.button == 4:
                zoom(1)
            elif event.button == 5:
                zoom(-1)
        elif event.type == pygame.MOUSEMOTION:
            if drag:
                change_view(*map(lambda x: x / Config.scale, event.rel))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Config.pause = not Config.pause
                message.text = [
                    language["game"]["resume"],
                    language["game"]["pause"]
                ][Config.pause]
                disappear_message()
            elif event.key == pygame.K_p:
                if screen.get_width() > width:
                    screen = pygame.display.set_mode(size)
                else:
                    screen = pygame.display.set_mode((width + 100, height))
            elif event.key == pygame.K_f:
                screen = pygame.display.set_mode()
            elif event.key in (pygame.K_LEFT, pygame.K_KP_4):
                change_view(movement / Config.scale, 0)
            elif event.key in (pygame.K_RIGHT, pygame.K_KP_6):
                change_view(-movement / Config.scale, 0)
            elif event.key in (pygame.K_UP, pygame.K_KP_8):
                change_view(0, movement / Config.scale)
            elif event.key in (pygame.K_DOWN, pygame.K_KP_2):
                change_view(0, -movement / Config.scale)
            elif event.key == pygame.K_1:
                Config.speed = 1
                message.text = f"Speed: {Config.speed}"
                disappear_message()
            elif event.key == pygame.K_2:
                Config.speed = 2
                message.text = f"Speed: {Config.speed}"
                disappear_message()
            elif event.key == pygame.K_3:
                Config.speed = 3
                message.text = f"Speed: {Config.speed}"
                disappear_message()
            elif event.key == pygame.K_4:
                Config.speed = 4
                message.text = f"Speed: {Config.speed}"
                disappear_message()
            elif event.key == pygame.K_5:
                Config.speed = 5
                message.text = f"Speed: {Config.speed}"
                disappear_message()
            elif event.key == pygame.K_6:
                Config.speed = 6
                message.text = f"Speed: {Config.speed}"
                disappear_message()
            elif event.key == pygame.K_7:
                Config.speed = 7
                message.text = f"Speed: {Config.speed}"
                disappear_message()
            elif event.key == pygame.K_8:
                Config.speed = 8
                message.text = f"Speed: {Config.speed}"
                disappear_message()
            elif event.key == pygame.K_9:
                Config.speed = 9
                message.text = f"Speed: {Config.speed}"
                disappear_message()
            elif event.key == pygame.K_0:
                Config.speed = 10
                message.text = f"Speed: {Config.speed}"
                disappear_message()
            elif event.mod & pygame.KMOD_CTRL:
                # Clicked ctrl key
                if event.key == pygame.K_d:
                    filepath = fd.asksaveasfilename(
                        initialdir=PATH,
                        defaultextension=".png",
                        filetypes=[
                            (language["save"]["picture"] % "PNG", "*.png"),
                            (language["save"]["picture"] % "JPG", "*.jpg"),
                            (language["save"]["picture"] % "BMP", "*.bmp"),
                            (language["save"]["other"], "*.*")
                        ]
                    )
                    if filepath:
                        pygame.image.save(screen, filepath)
                elif event.key == pygame.K_s:
                    filepath = fd.asksaveasfilename(
                        initialdir=os.path.join(PATH, "simulation"),
                        defaultextension=".simulation",
                        filetypes=[
                            (language["save"]["simulation"], "*.simulation"),
                            (language["save"]["other"], "*.*")
                        ]
                    )
                    if filepath:
                        with open(filepath, "w") as f:
                            f.write("[\n")
                            for star in stars:
                                f.write(f"    {str(star)},\n")
                            f.write("]")
                elif event.key == pygame.K_0:
                    zoom(0)
                elif event.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                    zoom(1)
                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    zoom(-1)
                elif event.key == pygame.K_w:
                    running = False
pygame.quit()
