#!/usr/bin/env python3.9

import pygame as py
import pygame.mouse
from pygame.locals import *
from math import ceil, log, sin
from time import time, perf_counter
from cmath import sin as csin


py.init()
print(py.display.get_wm_info())

surf = py.display.set_mode((1280, 720))
py.display.set_caption("Mandelbrot set")
surf.fill('white')
res = 1  # size of each pixel
ratio = surf.get_width()/surf.get_height()


def binet(num):
    golden = (1 + 5 ** 0.5) / 2
    return pow(golden, num) - pow(-golden, -num)/5 ** 0.5


class Unit:
    # -2.5, 1.5
    # 78, 20, 5, 2, 1
    # from (-2.5, y) & (1.5, y) to (-0.61429469466266, 0.6765739345925285) & (-0.6142946946626515, 0.6765739345925238)
    turns = None
    x_start, x_end = -2.5, 1.5
    length = (x_end-x_start) * (1/ratio)
    y_start, y_end = 0+length/2, 0-length/2

    def __init__(self, x, y):
        self.x, self.y = x, y

    def get_rel(self):
        a = self.get_pixel()
        return a[0] / surf.get_width(), a[1] / surf.get_height()

    def get_pixel(self):
        return res * self.x, res * self.y

    def get_on_grid(self):
        b = self.get_rel()
        return self.x_start + (self.x_end - self.x_start) * b[0], \
            self.y_start + (self.y_end - self.y_start) * b[1]

    def draw(self, surface, colour):
        py.draw.rect(surface, colour, (self.get_pixel()[0], self.get_pixel()[1], res, res))


def in_set(num: Unit, turns=None):
    try:
        num = (complex(*num.get_on_grid()))
        z = 0  # initial value
        #  int(50*2**(log(float(Unit.x_end-Unit.x_start)/10, 1/5)))
        if turns is None:
            turns = int(50*1.75**(log(float(Unit.x_end-Unit.x_start)/10, 1/5)))

        for x in range(turns):
            if abs(z) > 4:
                break
            z = z**2 + num
        else:
            return py.Color(0, 0, 0)

        c = int(127 * (sin((1/16)*x + 1.6)**5) + 127)

        # c = int((x / turns) * 255)
        # print(c)
        # py.Color(c, c, c)

        return py.Color(255-c, 0, c)
    except ZeroDivisionError:
        return py.Color(255, 255, 255)
    except OverflowError:
        return py.Color(255, 255, 255)


frame_size = 1/5
once = False
i = 0
s1 = py.Surface((surf.get_width(), surf.get_height()))
s1.fill('white')

running = True
while running:
    for event in py.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_s:
                py.image.save(s1, f"images/{time()}.png")
            if event.key == K_a:
                Unit.turns = 5000
                res = 1
                i = 0
        if event.type == MOUSEBUTTONDOWN:
            u1 = Unit(rect.left / res, rect.top / res).get_on_grid()
            u2 = Unit(rect.right / res, rect.bottom / res).get_on_grid()
            print(u1, u2)
            Unit.x_start = u1[0]
            Unit.x_end = u2[0]
            Unit.y_start = u1[1]
            Unit.y_end = u2[1]
            i = 0
    # surf.fill('black')
    if i < ceil(surf.get_width() / res):
        for j in range(ceil(surf.get_height() / res)):
            u = Unit(i, j)
            c = in_set(u, Unit.turns)
            u.draw(s1, c)

        i += 1

    surf.blit(s1, (0, 0))

    rect = Rect(0, 0, surf.get_width()*frame_size, surf.get_height()*frame_size)
    rect.center = py.mouse.get_pos()
    py.draw.rect(surf, 'white', rect, width=1)

    pygame.display.update()

