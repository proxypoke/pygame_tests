#! /usr/bin/env python2
# -*- coding: utf-8 -*-

# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is free software under the non-terms
# of the Anti-License. Do whatever the fuck you want.

import os
import pygame

pygame.init()

# size of the game window
WIDTH, HEIGHT = 640, 480

# Directions
DOWN = 0
LEFT = 1
RIGHT = 2
UP = 3

DATADIR = "."

SPRITE_WIDTH = 32
SPRITE_HEIGHT = 48

ARROW_KEYS = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)


def load_spritemap(name):
    '''Load a spritemap.'''
    path = os.path.join(DATADIR, name)
    try:
        image = pygame.image.load(path)
    except pygame.error as e:
        print("Error: can't load image: {0}".format(path))
        raise SystemExit(e)
    image = image.convert()
    colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey)
    return image, image.get_rect()


class Spritemap(pygame.sprite.Sprite):
    '''A spritemap represents a collection of individual sprites in a single
    image, accessed through subsurfaces.'''

    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_spritemap(name)
        self._spriterect = pygame.Rect(0, 0, SPRITE_WIDTH, SPRITE_HEIGHT)

    def _get_sprite_gen(self, direction):
        '''Get a sprite generator for the appropriate direction.'''
        if not direction in (LEFT, RIGHT, UP, DOWN):
            raise ValueError("Invalid direction.")
        # which row of the spritemap to use
        y_offset = direction * SPRITE_HEIGHT
        position = pygame.Rect(0, y_offset, SPRITE_WIDTH, SPRITE_HEIGHT)
        while True:
            yield self.image.subsurface(position)
            position = pygame.Rect(
                ((position[0] + SPRITE_WIDTH) % 128, y_offset),
                (SPRITE_WIDTH, SPRITE_HEIGHT))

    def down(self):
        return self._get_sprite_gen(DOWN)

    def up(self):
        return self._get_sprite_gen(UP)

    def left(self):
        return self._get_sprite_gen(LEFT)

    def right(self):
        return self._get_sprite_gen(RIGHT)


class Player(pygame.sprite.Sprite):
    '''A sprite representing the player, capable of moving around.'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._spritemap = Spritemap("KOS-MOS_spritemap.bmp")
        self.image = self._spritemap.image.subsurface(
            self._spritemap._spriterect)
        self.rect = self.image.get_rect()
        self._direction = DOWN
        self._spritegen = self._spritemap.down()
        self._moving = False
        self._movement = (0, 0)

    def update(self, key=None):
        if key:
            if key.key not in ARROW_KEYS:
                return
            elif key.type == pygame.KEYUP:
                self._moving = False
            elif key.type == pygame.KEYDOWN:
                self._set_direction(key)
                self._moving = True
        if self._moving:
            self._move()

    def _set_direction(self, key):
        if key.key == pygame.K_UP:
            newdirection = UP
            self._movement = (0, -4)
        elif key.key == pygame.K_DOWN:
            newdirection = DOWN
            self._movement = (0, 4)
        elif key.key == pygame.K_LEFT:
            newdirection = LEFT
            self._movement = (-4, 0)
        else:
            newdirection = RIGHT
            self._movement = (4, 0)
        if newdirection != self._direction:
            self._direction = newdirection
            self._spritegen = self._spritemap._get_sprite_gen(self._direction)

    def _move(self):
        self.image = next(self._spritegen)
        self.rect = self.rect.move(self._movement)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player = Player()
    allsprites = pygame.sprite.RenderPlain()
    allsprites.add(player)

    allsprites.draw(screen)

    clock = pygame.time.Clock()

    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.KEYDOWN:
                allsprites.update(event)
            elif event.type == pygame.KEYUP:
                allsprites.update(event)

        screen.fill((255, 255, 255))
        allsprites.draw(screen)
        allsprites.update()
        pygame.display.flip()


if __name__ == "__main__":
    main()
