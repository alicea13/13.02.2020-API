import os
import sys

import pygame
import requests

coord_x = '37.490971'
cord_y = '55.829152'
delta = '0.02'


def request():
    global delta, coord_x, cord_y
    response = None
    map_request = "http://static-maps.yandex.ru/1.x/?"

    map_params = {
        "ll": ",".join([coord_x, cord_y]),
        "spn": ",".join([delta, delta]),
        "l": "map"
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
screen = pygame.display.set_mode((600, 450))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_DOWN:
                print("pageup")
                if float(delta) + 0.005 != 17:
                    delta = str(float(delta) + 0.005)
                    request()
            if event.key == pygame.K_UP:
                print('pagedown')
                if float(delta) - 0.005 != 0:
                    delta = str(float(delta) + 0.005)
                    request()
    pygame.display.flip()
    screen.blit(pygame.image.load(map), (0, 0))


pygame.quit()


os.remove(map)