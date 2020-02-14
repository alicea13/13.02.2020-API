import os
import sys

import pygame
import requests

coord_x = '37.490971'
coord_y = '55.829152'
delta = '0.02'
tip = "map"


def on_click(cell_coords):
    global delta, coord_x, coord_y, tip
    if cell_coords[0] > 600 and cell_coords[1] < 40:
        tip = "map"
        map = request()
    if cell_coords[0] > 600 and 40 < cell_coords[1] < 80:
        tip = "sat"
        map = request()
    if cell_coords[0] > 600 and 80 < cell_coords[1] < 120:
        tip = "sat,skl"
        map = request()


def request():
    global delta, coord_x, coord_y, tip
    response = None
    map_request = "http://static-maps.yandex.ru/1.x/?"

    map_params = {
        "ll": ",".join([coord_x, coord_y]),
        "spn": ",".join([delta, delta]),
        "l": tip
    }

    response = requests.get(map_request, params=map_params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


map = request()

pygame.init()
screen = pygame.display.set_mode((720, 450))
screen.fill((255, 255, 255))
font = pygame.font.Font(None, 40)
text = font.render("Схема", 1, (0, 0, 0))
text_x = 600
text_y = 0
screen.blit(text, (text_x, text_y))
font = pygame.font.Font(None, 40)
text = font.render("Спутник", 1, (0, 0, 0))
text_x = 600
text_y = 40
screen.blit(text, (text_x, text_y))
font = pygame.font.Font(None, 40)
text = font.render("Гибрид", 1, (0, 0, 0))
text_x = 600
text_y = 80
screen.blit(text, (text_x, text_y))




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 280:
                if float(delta) + 2 < 17:
                    delta = str(float(delta) + 2)
                    print(delta)
                    map = request()
            if event.key == 281:
                if float(delta) - 2 > 0:
                    delta = str(float(delta) - 2)
                    print(delta)
                    map = request()
            if event.key == pygame.K_UP:
                if float(coord_y) + 1 < 80:
                    coord_y = str(float(coord_y) + 1)
                    print(coord_y)
                    map = request()
            if event.key == pygame.K_DOWN:
                if float(coord_y) - 1 > -80:
                    coord_y = str(float(coord_y) - 1)
                    print(coord_y)
                    map = request()
            if event.key == pygame.K_LEFT:
                if float(coord_x) - 1 > -180:
                    coord_x = str(float(coord_x) - 1)
                    print(coord_x)
                    map = request()
            if event.key == pygame.K_RIGHT:
                if float(coord_x) + 1 < 180:
                    coord_x = str(float(coord_x) + 1)
                    print(coord_x)
                    map = request()
            if event.key == pygame.K_1:
                tip = "map"
                map = request()
            if event.key == pygame.K_2:
                tip = "sat"
                map = request()
            if event.key == pygame.K_3:
                tip = "sat,skl"
                map = request()
        if event.type == pygame.MOUSEBUTTONUP:
            on_click(event.pos)

    pygame.display.flip()
    screen.blit(pygame.image.load(map), (0, 0))

pygame.quit()

os.remove(map)
