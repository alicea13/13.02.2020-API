import os
import sys

import pygame
import requests


coord_x = '37.490971'
coord_y = '55.829152'
delta = '0.02'
tip = "map"


class InputWindow:
    def __init__(self, screen, par):
        global coord_x, coord_y, delta, tip

        self.text = ''
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 600 + 2, 40)
        self.text_surf = pygame.font.Font(None, 32).render(self.text, True, (0, 0, 0))
        # self.run_input = False
        self.parent = par

        self.color = "black"

        self.x = 0
        self.y = 0
        self.width = 600
        self.height = 40

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
                self.parent.place_find = True
                # print(self.search(self.text))
                request(self.parent.coord, self.delta, self.tip, self.parent.place_find, self.search(self.text))
                self.parent.coord_x, self.parent.coord_y = self.search(self.text)
                self.parent.coord = [self.parent.coord_x, self.parent.coord_y]
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            else:
                self.text += event.unicode
            self.text_surf = pygame.font.Font(None, 32).render(self.text, True, (0, 0, 0))
        return self.parent.coord

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color("white"), self.rect, 0)
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
    def __init__(self):
        global coord_x, coord_y, delta, tip

        pygame.init()
        screen = pygame.display.set_mode((720, 490))
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 40)

        self.coord_y = coord_y
        self.coord_x = coord_x
        self.coord = [coord_x, coord_y]
        self.delta = delta
        self.tip = tip

        self.place_find = False
        self.coord_pl = []

        text_map = font.render("Схема", 1, (0, 0, 0))
        text_x_map = 620
        text_y_map = 50
        text_w_map = text_map.get_width()
        text_h_map = text_map.get_height()

        pygame.draw.rect(screen, (0, 0, 0), (600, text_y_map - 10,
                                             630, text_h_map + 20), 2)
        self.color_gibr = (0, 0, 0)

        font = pygame.font.Font(None, 40)
        text_spn = font.render("Спутник", 1, (0, 0, 0))
        text_x_spn = 605
        text_y_spn = 98
        text_w_spn = text_spn.get_width()
        text_h_spn = text_spn.get_height()

        pygame.draw.rect(screen, (0, 0, 0), (600, text_y_spn - 10,
                                             text_w_spn + 20, text_h_spn + 20), 2)
        self.color_spn = (0, 0, 0)

        font = pygame.font.Font(None, 40)
        text_gibr = font.render("Гибрид", 1, (0, 0, 0))
        text_x_gibr = 610
        text_y_gibr = 146
        text_w_gibr = text_gibr.get_width()
        text_h_gibr = text_gibr.get_height()
        pygame.draw.rect(screen, (0, 0, 0), (600, text_y_gibr - 10,
                                             text_w_gibr + 20, text_h_gibr + 20), 2)
        self.color_map = (0, 0, 0)

        pygame.draw.rect(screen, (0, 0, 0), (601, 0, 120, 40), 2)
        font = pygame.font.Font(None, 40)
        text_find = font.render("Искать", 1, (0, 0, 0))

        running = True

        self.search_line = InputWindow(screen, self)

        map = request([self.coord_x, self.coord_y], self.delta, self.tip, self.place_find)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    self.search_line.run_text = True
                    if event.key == 280:
                        if float(self.delta) + 2 < 17:
                            self.delta = str(float(self.delta) + 2)
                            print(self.delta)
                            map = request([self.coord_x, self.coord_y], self.delta, self.tip, self.place_find, self.coord_pl)
                    if event.key == 281:
                        if float(self.delta) - 2 > 0:
                            self.delta = str(float(self.delta) - 2)
                            print(self.delta)
                            map = request([self.coord_x, self.coord_y], self.delta, self.tip, self.place_find, self.coord_pl)
                    if event.key == pygame.K_UP:
                        if float(self.coord_y) + 1 < 80:
                            self.coord_y = str(float(self.coord_y) + 0.001)
                            # self.coord[1] = str(float(self.coord_y) + 0.001)
                            print(self.coord_y)
                            map = request([self.coord_x, self.coord_y], self.delta, self.tip, self.place_find, self.coord_pl)
                    if event.key == pygame.K_DOWN:
                        if float(self.coord_y) - 1 > -80:
                            self.coord_y = str(float(self.coord_y) - 0.001)
                            # self.coord[1] = str(float(self.coord_y) - 0.001)
                            print(self.coord_y)
                            map = request([self.coord_x, self.coord_y], self.delta, self.tip, self.place_find, self.coord_pl)
                    if event.key == pygame.K_LEFT:
                        if float(self.coord_x) - 1 > -180:
                            self.coord_x = str(float(self.coord_x) - 0.001)
                            # self.coord[0] = str(float(self.coord_x) - 0.001)
                            print(self.coord_x)
                            map = request([self.coord_x, self.coord_y], self.delta, self.tip, self.place_find, self.coord_pl)
                    if event.key == pygame.K_RIGHT:
                        if float(self.coord_x) + 1 < 180:
                            self.coord_x = str(float(self.coord_x) + 0.001)
                            # self.coord[0] = str(float(self.coord_x) + 0.001)
                            print("coord_x", self.coord_x)
                            print(f'right {self.coord}')
                            map = request([self.coord_x, self.coord_y], self.delta, self.tip, self.place_find, self.coord_pl)
                    # if event.key == pygame.K_1:
                    if event.key in [pygame.K_1, pygame.KMOD_ALT]:
                        self.tip = "map"
                        map = request([self.coord_x, self.coord_y], self.delta, self.tip, self.place_find, self.coord_pl)
                        self.search_line.run_text = False
                    # if event.key == pygame.K_2:
                    if event.key in [pygame.K_2, pygame.KMOD_ALT]:
                        self.tip = "sat"
                        map = request([self.coord_x, self.coord_y], self.delta, self.tip, self.place_find, self.coord_pl)
                        self.search_line.run_text = False
                    # if event.key == pygame.K_3:
                    if event.key in [pygame.K_3, pygame.KMOD_ALT]:
                        self.tip = "sat,skl"
                        map = request([self.coord_x, self.coord_y], self.delta, self.tip, self.place_find, self.coord_pl)
                        self.search_line.run_text = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.on_click(event.pos)
                self.search_line.events(event)
            self.search_line.draw(screen)
            pygame.draw.rect(screen, self.color_map, (601, text_y_map - 10,
                                                 630, text_h_map + 20), 2)
            screen.blit(text_map, (text_x_map, text_y_map))
            pygame.draw.rect(screen, self.color_spn, (601, text_y_spn - 10,
                                                 text_w_spn + 20, text_h_spn + 20), 2)
            screen.blit(text_spn, (text_x_spn, text_y_spn))
            pygame.draw.rect(screen, self.color_gibr, (601, text_y_gibr - 10,
                                                 text_w_gibr + 20, text_h_gibr + 20), 2)
            screen.blit(text_gibr, (text_x_gibr, text_y_gibr))
            screen.blit(text_find, (612, 8))
            screen.blit(pygame.image.load(map), (0, 40))
            pygame.display.flip()
        pygame.quit()

        os.remove(map)

    def on_click(self, cell_coords):
        # global delta, coord_x, coord_y, tip
        if cell_coords[0] > 600 and cell_coords[1] <= 40:
            self.coord = InputWindow.search(InputWindow, self.search_line.text)
            request(InputWindow.search(InputWindow, self.search_line.text), self.delta, self.tip)
            self.text = ''
        if cell_coords[0] > 600 and 40 < cell_coords[1] <= 90:
            self.color_map, self.color_spn, self.color_gibr = (0, 255, 0), (0, 0, 0), (0, 0, 0)
            self.tip = "map"
            map = request([self.coord_x, self.coord_y], self.delta, self.tip, self.place_find, self.coord_pl)
        if cell_coords[0] > 600 and 90 < cell_coords[1] <= 140:
            self.color_map, self.color_spn, self.color_gibr = (0, 0, 0), (0, 255, 0), (0, 0, 0)
            self.tip = "sat"
            map = request([self.coord_x, self.coord_y], self.delta, self.tip, self.place_find, self.coord_pl)
        if cell_coords[0] > 600 and 140 < cell_coords[1] <= 190:
            self.color_map, self.color_spn, self.color_gibr = (0, 0, 0), (0, 0, 0), (0, 255, 0)
            self.tip = "sat,skl"
            map = request([self.coord_x, self.coord_y], self.delta, self.tip, self.place_find, self.coord_pl)


def request(coord, delta, tip, find, *coords_pl):   # def request(coord, delta, tip, find):
    # global delta, coord_x, coord_y, tip
    coords = "{0},{1}".format(coord[0], coord[1])

    response = None
    map_request = "http://static-maps.yandex.ru/1.x/?"

    if find:
        place_coords, = coords_pl
        print(place_coords)
        # place_coord = "{0},{1}".format(coords_pl[0], coords_pl[1])
        map_params = {
                "ll": ",".join([coords_pl[0][0], coords_pl[0][1]]),
                "spn": ",".join([delta, delta]),
                "l": tip,
                "pt":  "{0},pm2dbl".format(coords)
            }
    else:
        map_params = {
            "ll": ",".join([coord[0], coord[1]]),
            "spn": ",".join([delta, delta]),
            "l": tip,

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


Window()
