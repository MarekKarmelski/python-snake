#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Prize class."""

import random


class Prize:

    types = {10: '#a50000', 20: '#e19500', 30: '#02acff', 40: '#9500d2', 50: '#30f1ff'}

    value = None

    pos = None

    box = None

    life_time = 50

    current_life_time = 0

    game_board_canvas = None

    def __init__(self, game_board_canvas, snake, traps):
        self.game_board_canvas = game_board_canvas
        self.value = random.randrange(10, 60, 10)
        color = self.types[self.value]

        all_x_pos = all_y_pos = []

        for snake_part in snake:
            c = self.game_board_canvas.coords(snake_part.body_part)
            all_x_pos.append(int(c[0]))
            all_y_pos.append(int(c[1]))

        for trap in traps:
            c = self.game_board_canvas.coords(trap.get())
            all_x_pos.append(int(c[0]))
            all_y_pos.append(int(c[1]))

        x_pos = random.randrange(0, 400, 10)
        y_pos = random.randrange(0, 300, 10)

        while x_pos in all_x_pos and y_pos in all_y_pos:
            x_pos = random.randrange(0, 400, 10)
            y_pos = random.randrange(0, 300, 10)

        self.box = self.game_board_canvas.create_rectangle(x_pos, y_pos, x_pos + 10, y_pos + 10, outline=color, fill=color, tags=('prize'))
        self.game_board_canvas.tag_lower(self.box)

    def get(self):
        return self.box

    def increase_current_life_time(self):
        self.current_life_time += 1

    def can_remove(self):
        return self.life_time == self.current_life_time

    def remove(self):
        self.game_board_canvas.delete(self.box)
        pass

