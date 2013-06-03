#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

pygame.init()

# Directions
DOWN = 0
LEFT = 1
RIGHT = 2
UP = 3

WIDTH, HEIGHT = 160, 120


def get_sprite_gen(spritemap, player, direction):
    if not direction in (LEFT, RIGHT, UP, DOWN):
        raise ValueError("Invalid direction.")
    height = direction * 48

    pos = player.get_offset()
    while True:
        pos = pygame.Rect(((pos[0] + 32) % 128, height),
                          player.get_size())
        yield spritemap.subsurface(pos)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # load the spritemap and set the player surface to an initial value
    spritemap = pygame.image.load('KOS-MOS_spritemap.bmp').convert()
    spritepos = pygame.Rect(0, 0, 32, 48)
    player = spritemap.subsurface(spritepos)
    position = player.get_rect()
    screen.blit(player, position)

    # create a background and set it
    background = pygame.image.frombuffer(
        '0' * HEIGHT * WIDTH, (WIDTH, HEIGHT), "P")
    screen.blit(background, (0, 0))

    pygame.display.update()

    sprite = get_sprite_gen(spritemap, player, DOWN)
    direction = (0, 2)

    while NotImplemented:
        for event in pygame.event.get():
            if (event.type is QUIT or
                    (event.type is KEYDOWN and event.scancode == 66)):  # ESC
                exit(0)

        # erase the screen
        screen.blit(background, position, position)

        # take the next sprite
        player = next(sprite)
        position = position.move(direction)

        if position[1] + 48 >= HEIGHT and position[0] == 0:
            print("Lower left corner reached.")
            direction = (2, 0)
            sprite = get_sprite_gen(spritemap, player, RIGHT)
        elif position[0] + 32 >= WIDTH and position[1] == HEIGHT - 48:
            print("Lower right corner reached.")
            direction = (0, -2)
            sprite = get_sprite_gen(spritemap, player, UP)
        elif position[1] <= 0 and position[0] == WIDTH - 32:
            print("Upper right corner reached.")
            direction = (-2, 0)
            sprite = get_sprite_gen(spritemap, player, LEFT)
        elif position[0] <= 0 and position[1] == 0:
            print("Upper left corner reached")
            direction = (0, 2)
            sprite = get_sprite_gen(spritemap, player, DOWN)
        screen.blit(player, position)
        pygame.display.update()
        pygame.time.delay(100)

if __name__ == "__main__":
    main()
