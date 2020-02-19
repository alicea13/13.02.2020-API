import os
import sys

import pygame
import requests


class InputWindow:
    def __init__(self, x, y, width, height, delta, tip, screen, par):

        self.text = ''
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.text_surf = pygame.font.Font(None, 32).render(self.text, True, (0, 0, 0))
        # self.run_input = False
        self.parent = par

        self.color = "black"

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.delta = delta
        self.tip = tip

        self.run_text = False

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.run_text = True
                self.color = "grey"
            else:
                self.run_text = False
                self.color = "black"

        if event.type == pygame.KEYDOWN and self.run_text:
            if event.key == pygame.K_RETURN:
                self.parent.coord = self.search(self.text)
                request(self.search(self.text), self.delta, self.tip)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            else:
                self.text += event.unicode
            self.text_surf = pygame.font.Font(None, 32).render(self.text, True, (0, 0, 0))
        return self.parent.coord

    def draw(self, screen):
        screen.blit(self.text_surf, (self.rect.x + 5, self.rect.y + 5))

        pygame.draw.rect(screen, pygame.Color(self.color), self.rect, 3)

    def search(self, toponym):
        if toponym:
            geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": toponym,
                "format": "json"}

            response = requests.get(geocoder_api_server, params=geocoder_params)

            json_response = response.json()

            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]

            toponym_coodrinates = toponym["Point"]["pos"]
            toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

            return [toponym_longitude, toponym_lattitude]


class Window:
    def __init__(self, coord_x, coord_y, delta, tip):

        pygame.init()
        screen = pygame.display.set_mode((720, 490))
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 40)

        self.coord_y = coord_y
        self.coord_x = coord_x
        self.coord = [coord_x, coord_y]
        self.delta = delta
        self.tip = tip

        text = font.render("Схема", 1, (0, 0, 0))
        text_x = 620
        text_y = 50
        text_w = text.get_width()
        text_h = text.get_height()

        pygame.draw.rect(screen, (0, 0, 0), (600, text_y - 10,
                                             630, text_h + 20), 2)

        screen.blit(text, (text_x, text_y))
        font = pygame.font.Font(None, 40)
        text = font.render("Спутник", 1, (0, 0, 0))
        text_x = 605
        text_y = 98
        text_w = text.get_width()
        text_h = text.get_height()
        pygame.draw.rect(screen, (0, 0, 0), (600, text_y - 10,
                                             text_w + 20, text_h + 20), 2)
        screen.blit(text, (text_x, text_y))
        font = pygame.font.Font(None, 40)
        text = font.render("Гибрид", 1, (0, 0, 0))
        text_x = 610
        text_y = 146
        screen.blit(text, (text_x, text_y))
        text_w = text.get_width()
        text_h = text.get_height()
        pygame.draw.rect(screen, (0, 0, 0), (600, text_y - 10,
                                             text_w + 20, text_h + 20), 2)

        '''pygame.draw.rect(screen, (0, 0, 0), (600, 0, 120, 40), 2)
        font = pygame.font.Font(None, 40)
        text = font.render("Искать", 1, (0, 0, 0))
        screen.blit(text, (612, 8))'''

        running = True

        search_line = InputWindow(0, 0, 600, 40, self.delta, self.tip, screen, self)

        map = request(self.coord, self.delta, self.tip)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == 280:
                        if float(self.delta) + 2 < 17:
                            self.delta = str(float(self.delta) + 2)
                            print(self.delta)
                            map = request(self.coord, self.delta, self.tip)
                    if event.key == 281:
                        if float(self.delta) - 2 > 0:
                            self.delta = str(float(self.delta) - 2)
                            print(self.delta)
                            map = request(self.coord, self.delta, self.tip)
                    if event.key == pygame.K_UP:
                        if float(self.coord_y) + 1 < 80:
                            self.coord_y = str(float(self.coord_y) + 0.001)
                            print(self.coord_y)
                            map = request(self.coord, self.delta, self.tip)
                    if event.key == pygame.K_DOWN:
                        if float(self.coord_y) - 1 > -80:
                            self.coord_y = str(float(self.coord_y) - 0.001)
                            print(self.coord_y)
                            map = request(self.coord, self.delta, self.tip)
                    if event.key == pygame.K_LEFT:
                        if float(self.coord_x) - 1 > -180:
                            self.coord_x = str(float(self.coord_x) - 0.001)
                            print(self.coord_x)
                            map = request(self.coord, self.delta, self.tip)
                    if event.key == pygame.K_RIGHT:
                        if float(self.coord_x) + 1 < 180:
                            self.coord_x = str(float(self.coord_x) + 0.001)
                            print(self.coord_x)
                            map = request(self.coord, self.delta, self.tip)
                    if event.key == pygame.K_1:
                        self.tip = "map"
                        map = request(self.coord, self.delta, self.tip)
                    if event.key == pygame.K_2:
                        self.tip = "sat"
                        map = request(self.coord, self.delta, self.tip)
                    if event.key == pygame.K_3:
                        self.tip = "sat,skl"
                        map = request(self.coord, self.delta, self.tip)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.on_click(event.pos)
                search_line.events(event)
            search_line.draw(screen)
            screen.blit(pygame.image.load(map), (0, 40))
            pygame.display.flip()
        pygame.quit()

        os.remove(map)

    def on_click(self, cell_coords):
        # global delta, coord_x, coord_y, tip
        if cell_coords[0] > 600 and cell_coords[1] <= 40:
            self.coord = InputWindow.search(InputWindow.text)
            request(InputWindow.search(InputWindow.text), self.delta, self.tip)
            self.text = ''
        if cell_coords[0] > 600 and 40 < cell_coords[1] <= 90:
            self.tip = "map"
            map = request(self.coord, self.delta, self.tip)
        if cell_coords[0] > 600 and 90 < cell_coords[1] <= 140:
            self.tip = "sat"
            map = request(self.coord, self.delta, self.tip)
        if cell_coords[0] > 600 and 140 < cell_coords[1] <= 190:
            self.tip = "sat,skl"
            map = request(self.coord, self.delta, self.tip)


def request(coord, delta, tip):
    # global delta, coord_x, coord_y, tip
    coords = "{0},{1}".format(coord[0], coord[1])
    response = None
    map_request = "http://static-maps.yandex.ru/1.x/?"

    map_params = {
            "ll": ",".join([coord[0], coord[1]]),
            "spn": ",".join([delta, delta]),
            "l": tip,
            "pt":  "{0},pm2dbl".format(coords)
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