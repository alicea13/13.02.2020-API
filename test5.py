import os
import sys

import pygame
import requests


class InputWindow:
    def __init__(self):
        self.text_surf = pygame.font.Font(None, 32).render("", True, (0, 0, 0))
        self.tun_input = False

    # def events(self, event):


class Window:
    def __init__(self, coord_x, coord_y, delta, tip):

        pygame.init()
        self.screen = pygame.display.set_mode((720, 450))
        self.screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 40)

        self.coord_x = self.request
        self.coord_y = coord_y
        self.delta = delta
        self.tip = tip

        text = font.render("Схема", 1, (0, 0, 0))
        text_x = 620
        text_y = 1
        text_w = text.get_width()
        text_h = text.get_height()
        pygame.draw.rect(self.screen, (0, 0, 0), (600, text_y - 10,
                                             630, text_h + 20), 3)
        self.screen.blit(text, (text_x, text_y))
        font = pygame.font.Font(None, 40)
        text = font.render("Спутник", 1, (0, 0, 0))
        text_x = 600
        text_y = 48
        text_w = text.get_width()
        text_h = text.get_height()
        pygame.draw.rect(self.screen, (0, 0, 0), (600, text_y - 10,
                                             text_w + 20, text_h + 20), 3)
        self.screen.blit(text, (text_x, text_y))
        font = pygame.font.Font(None, 40)
        text = font.render("Гибрид", 1, (0, 0, 0))
        text_x = 610
        text_y = 97
        self.screen.blit(text, (text_x, text_y))
        text_w = text.get_width()
        text_h = text.get_height()
        pygame.draw.rect(self.screen, (0, 0, 0), (600, text_y - 10,
                                             text_w + 20, text_h + 20), 3)

        running = True

        map = self.request()


        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == 280:
                        if float(delta) + 2 < 17:
                            delta = str(float(delta) + 2)
                            print(delta)
                            map = self.request()
                    if event.key == 281:
                        if float(delta) - 2 > 0:
                            delta = str(float(delta) - 2)
                            print(delta)
                            map = self.request()
                    if event.key == pygame.K_UP:
                        if float(coord_y) + 1 < 80:
                            coord_y = str(float(coord_y) + 0.001)
                            print(coord_y)
                            map = self.request()
                    if event.key == pygame.K_DOWN:
                        if float(coord_y) - 1 > -80:
                            coord_y = str(float(coord_y) - 0.001)
                            print(coord_y)
                            map = self.request()
                    if event.key == pygame.K_LEFT:
                        if float(coord_x) - 1 > -180:
                            coord_x = str(float(coord_x) - 0.001)
                            print(coord_x)
                            map = self.request()
                    if event.key == pygame.K_RIGHT:
                        if float(coord_x) + 1 < 180:
                            coord_x = str(float(coord_x) + 0.001)
                            print(coord_x)
                            map = self.request()
                    if event.key == pygame.K_1:
                        tip = "map"
                        map = self.request()
                    if event.key == pygame.K_2:
                        tip = "sat"
                        map = self.request()
                    if event.key == pygame.K_3:
                        tip = "sat,skl"
                        map = self.request()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.on_click(event.pos)

            pygame.display.flip()
            self.screen.blit(pygame.image.load(map), (0, 0))
        pygame.quit()

        os.remove(map)

    def on_click(self, cell_coords):
        global delta, coord_x, coord_y, tip
        if cell_coords[0] > 600 and cell_coords[1] < 40:
            tip = "map"
            map = self.request()
        if cell_coords[0] > 600 and 40 < cell_coords[1] < 80:
            tip = "sat"
            map = self.request()
        if cell_coords[0] > 600 and 80 < cell_coords[1] < 120:
            tip = "sat,skl"
            map = self.request()

    def request(self):
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
            print("Http статус:", response.status_code, "(", response.reason,
                  ")")
            sys.exit(1)

        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        return map_file

Window('37.490971', '55.829152', '0.02', "map")