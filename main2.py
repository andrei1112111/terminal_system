import pygame
from pygame.locals import *
import requests
import time
import json

json_data = json.load(open('data.json'))
DISPLAY_SIZE = (1920, 1080)
DEFAULT_BACKGROUND_COLOUR = (4, 3, 0)
SYMBOLS_OFFSET = (20, 15)
SCROLL_SPEED = 1.5
FPS = 85
# 84 символа в строке
DEFAULT_LOCK = [0, 15]
START_TEXT = [
    f'      Welcome to the new Level {json_data["software"]} terminal software created by Tishkin Andrei',
    '',
    'The Python version is Python 3.11.0',
    'Pygame is used to render the terminal',
    'And also: Requests, Time, Json',
    f'Last update: {json_data["last_update"]}',
    '',
    '',
    '',
    '               Github repository: https://github.com/andrei1112111/terminal_system',
    '',
    '',
    f'{33 * " "}---PRESS A KEY---'
]

trans_kirill = ["йцукенгшщзхъфывапролджэёячсмитьбю", "qwertyuiop[]asdfghjkl;'\zxcvbnm,."]

pygame.init()
flags = FULLSCREEN | SCALED | DOUBLEBUF

DISPLAY_SIZE = (1920 // 2, 1080 // 2)
flags = DOUBLEBUF

screen_surface = pygame.display.set_mode(size=DISPLAY_SIZE, flags=flags)
clock = pygame.time.Clock()


class Console:
    def __init__(self, s_size, default_data):
        self.DEFAULT_NORMAL_FONT = "VT323-Regular.ttf"
        self.DEFAULT_FONT_SIZE = 28
        self.DEFAULT_FONT_COLOUR = 255, 191, 0
        self.S_SIZE = s_size
        self.data = default_data
        self.FONT = pygame.font.Font(self.DEFAULT_NORMAL_FONT, self.DEFAULT_FONT_SIZE)
        self.SYMBOL_SIZE = (self.DEFAULT_FONT_SIZE, self.DEFAULT_FONT_SIZE)
        self.lock = DEFAULT_LOCK

    def render(self, offset):
        offset = SYMBOLS_OFFSET[1] - offset
        for string in self.data:
            if offset + self.SYMBOL_SIZE[1] >= 0:
                screen_surface.blit(
                    self.FONT.render(string, True, self.DEFAULT_FONT_COLOUR),
                    (SYMBOLS_OFFSET[0], offset)
                )
            offset += self.SYMBOL_SIZE[1]
        if offset >= DISPLAY_SIZE[1] - self.DEFAULT_FONT_SIZE * 2 - SYMBOLS_OFFSET[1]:
            return True

    def append(self, string, blocked: bool = False):
        self.data.append(string)
        if blocked:
            self.lock = [len(string), len(self.data)]

    def add(self, symbol):
        if self.data == ['']:
            self.data[-1] += symbol
        elif self.FONT.render(
                self.data[-1], True, self.DEFAULT_FONT_COLOUR
        ).get_rect().bottomright[0] + SYMBOLS_OFFSET[0] < DISPLAY_SIZE[0] - SYMBOLS_OFFSET[0]:
            self.data[-1] += symbol
        else:
            self.data.append(symbol)

    def remove(self, b: bool = True, perm: bool = False):
        if len(self.data[-1]) == 0 and len(self.data) <= self.lock[1]:
            return
        elif len(self.data) == self.lock[1] and len(self.data[-1]) <= self.lock[0]:
            return
        if perm:
            self.data[-1] = self.data[-1][:-1]
            return
        if len(self.data[-1]) == 0:
            del self.data[-1]
        else:
            if b and self.data[-1] == cursor_symbol[0]:
                self.data[-1] = self.data[-1][:-1]
            if len(self.data[-1]) == 0:
                del self.data[-1]
            else:
                self.data[-1] = self.data[-1][:-1]
        if not self.data:
            self.data = ['']

    def new_line(self, n):
        if n == 1:
            return self.data[-1][self.lock[0]:].replace('¦', '')
        if self.data == ['']:
            self.data.append(cursor_symbol[0])
        if self.data[-1] and self.data[-1][-1] == cursor_symbol[0]:
            console.remove(perm=True)
        self.data.append('')

    def get(self, el: int | str = -1):
        if type(el) == int:
            if self.data == [''] or self.data[-1] == '':
                return None
            return self.data[-1][el]
        elif type(el) == str:
            if el == 'all':
                return self.data


console = Console(DISPLAY_SIZE, START_TEXT)
cursor_symbol = "¦"
screen_offset = 0
current_system_pos = 'wait_key'
lines_for_answer = 1

ONE_PER_SECOND = pygame.USEREVENT + 1
pygame.time.set_timer(ONE_PER_SECOND, 1000)
TEN_PER_SECOND = pygame.USEREVENT + 2
pygame.time.set_timer(TEN_PER_SECOND, 80)

while True:
    for event in pygame.event.get():
        if current_system_pos == 'typing':
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
                elif event.key == K_RETURN:
                    answer = console.new_line(lines_for_answer)
                    print(answer)
            if event.type == TEN_PER_SECOND:
                keys = pygame.key.get_pressed()
                if keys[K_BACKSPACE]:
                    if console.get() == cursor_symbol[0]:
                        console.remove()
                    console.remove()
            if event.type == TEXTINPUT:
                if console.get() == cursor_symbol[0]:
                    console.remove(perm=True)
                if event.text[0] in trans_kirill[0]:
                    event.text = ''.join([trans_kirill[1][trans_kirill[0].index(i)] for i in event.text])
                console.add(event.text)
            if event.type == ONE_PER_SECOND:
                if console.get() == cursor_symbol[0]:
                    console.remove(False)
                else:
                    console.add(cursor_symbol[0])
        elif current_system_pos == 'wait_key':
            if event.type == KEYDOWN:
                system_start = True
                current_system_pos = 'select_hot'
        elif current_system_pos == 'select_hot':
            counter = 1
            [console.append('') for i in range(5)]
            for hot_function in json_data["hot_functions"]:
                console.append(f'| {counter} |      {hot_function[0]: <12}      {hot_function[1]}')
                counter += 1
            console.append('')
            console.append('Select: ', blocked=True)
            current_system_pos = 'typing'

    screen_surface.fill(DEFAULT_BACKGROUND_COLOUR)
    if console.render(screen_offset):
        screen_offset += SCROLL_SPEED
    pygame.display.flip()
    clock.tick(FPS)
