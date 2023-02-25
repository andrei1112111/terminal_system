import pygame
from pygame.locals import *

START_TEXT = [
    'Welcome to the new Level 1 terminal software'
    'created by Tishkin Andrei ',
    '          |          ',
    '          |          ',
    '          |          ',
    '          |          ',
]

DISPLAY_SIZE = (1920, 1080)
DEFAULT_BACKGROUND_COLOUR = (4, 3, 0)
SYMBOLS_OFFSET = (20, 15)
FPS = 85

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
        self.lock = [5, 0]

    def render(self, offset):
        offset = SYMBOLS_OFFSET[1] - offset
        for string in self.data:
            if offset + self.SYMBOL_SIZE[1] >= 0:
                screen_surface.blit(
                    self.FONT.render(string, True, self.DEFAULT_FONT_COLOUR),
                    (SYMBOLS_OFFSET[0], offset)
                )
            offset += self.SYMBOL_SIZE[1]

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

    def new_line(self):
        print(self.data, '--')
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

ONE_PER_SECOND = pygame.USEREVENT + 1
pygame.time.set_timer(ONE_PER_SECOND, 1000)
TEN_PER_SECOND = pygame.USEREVENT + 2
pygame.time.set_timer(TEN_PER_SECOND, 80)

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
            elif event.key == K_RETURN:
                console.new_line()
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

    # print(console.get('all'))

    screen_surface.fill(DEFAULT_BACKGROUND_COLOUR)
    console.render(screen_offset)
    pygame.display.flip()
    clock.tick(FPS)
