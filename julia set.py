#!/usr/bin/env python3.9

import pygame as py
import pygame.mouse
from pygame.locals import *
from math import ceil, log


py.init()
py.font.init()

surf = py.display.set_mode((1280, 720))
surf.fill('white')
res = 1  # size of each pixel
ratio = surf.get_width()/surf.get_height()


class Unit:
    # -2.5, 1.5
    # 78, 20, 5, 2, 1
    const = complex(0, 0)
    x_start, x_end = -2.5, 2.5
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


def in_set(num: Unit):
    try:
        num = complex(*num.get_on_grid())
        z = num  # initial value
        x = 0
        #  int(50*2**(log(float(Unit.x_end-Unit.x_start)/10, 1/5)))
        turns = 25
        while x < turns:
            if abs(z) > 1e100:
                break
            z = z**2 + Unit.const
            x += 1

        if x == turns:
            return py.Color(0, 0, 0)

        c = 255 - int((x / turns) * 255)
        # print(c)
        # py.Color(c, c, c)

        return py.Color(255-c, 0, c)
    except ZeroDivisionError:
        return py.Color(0, 0, 255)
    except OverflowError:
        return py.Color(255, 255, 255)
    except ValueError:
        return py.Color(255, 0, 0)


frame_size = 1/5
once = False
i = 0
s1 = py.Surface((surf.get_width(), surf.get_height()))
s1.fill('white')

vel_font = pygame.font.SysFont('arial', 30)

running = True
while running:
    for event in py.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_s:
                py.image.save(s1, "images/screenshot.png")
        if event.type == MOUSEBUTTONDOWN:
            u = Unit(py.mouse.get_pos()[0]/res, py.mouse.get_pos()[1]/res)
            print(u.get_on_grid())
            Unit.const = complex(*u.get_on_grid())
            i = 0
    # surf.fill('black')
    if i < ceil(surf.get_width() / res):
        for j in range(ceil(surf.get_height() / res)):
            u = Unit(i, j)
            u.draw(s1, in_set(u))

        i += 1

    surf.blit(s1, (0, 0))
    m_pos = Unit(py.mouse.get_pos()[0]/res, py.mouse.get_pos()[1]/res).get_on_grid()
    vel_text = vel_font.render(f"{round(m_pos[0], 2)} + {round(m_pos[1], 2)}i", False, (0, 0, 0))
    surf.blit(vel_text, (0, 0))

    pygame.display.update()
