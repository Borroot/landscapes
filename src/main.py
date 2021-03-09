from opensimplex import OpenSimplex
import time
import math
import pygame
from pygame.locals import *


WATER    = pygame.Color(50,  100, 200)
BEACH    = pygame.Color(250, 240, 25)
FOREST   = pygame.Color(40,  180, 10)
JUNGLE   = pygame.Color(20,  120, 0)
MOUNTAIN = pygame.Color(135, 135, 135)
SNOW     = pygame.Color(255, 255, 255)


def draw_layers(pixels, width, height, zoom):
    s1 = OpenSimplex(seed=int(time.time()))
    s2 = OpenSimplex(seed=int(time.time()))
    s3 = OpenSimplex(seed=int(time.time()))

    for x, y in [(x, y) for x in range(width) for y in range(height)]:
        nx, ny = x / width, y / height
        value = 1    * s1.noise2d(1 * nx * zoom, 1 * ny * zoom) \
              + 0.5  * s2.noise2d(2 * nx * zoom, 2 * ny * zoom) \
              + 0.25 * s3.noise2d(4 * nx * zoom, 4 * ny * zoom)
        pixels[y][x] = (value / (1 + 0.5 + 0.25) + 1) / 2


def draw_mask(pixels, width, height):
    max_dist = math.sqrt((width / 2) ** 2 + (height / 2) ** 2)
    for x, y in [(x, y) for x in range(width) for y in range(height)]:
        distx, disty = width / 2 - x, height / 2 - y
        dist = math.sqrt(distx ** 2 + disty ** 2)
        pixels[y][x] *= 1 - dist / max_dist


def draw_pixels(pixels, width, height):
    for x, y in [(x, y) for x in range(width) for y in range(height)]:
        color = draw_biome(pixels[y][x])
        pygame.display.get_surface().set_at((x, y), color)

    pygame.display.update()


def draw_biome(value):
    if   value < 0.30: return WATER
    elif value < 0.35: return BEACH
    elif value < 0.50: return FOREST
    elif value < 0.60: return JUNGLE
    elif value < 0.70: return MOUNTAIN
    else:              return SNOW


def draw(width, height, zoom):
    pixels = [[0] * width for _ in range(height)]
    draw_layers(pixels, width, height, zoom)
    draw_mask(pixels, width, height)
    draw_pixels(pixels, width, height)


def main():
    width, height = 500, 500
    zoom = 5.0

    pygame.init()

    pygame.display.set_caption('Landscape generation!')
    pygame.display.set_mode((width, height))

    draw(width, height, zoom)

    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                finished = True


if __name__ == "__main__":
    main()
