#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Trap class."""

import random


class Trap:

    value = None

    pos = None

    box = None

    life_time = 50

    current_life_time = 0

    game_board_canvas = None

    def __init__(self, game_board_canvas, snake, prize):
        self.game_board_canvas = game_board_canvas
        self.value = random.randrange(10, 60, 10)

        all_x_pos = all_y_pos = []

        for snake_part in snake:
            c = self.game_board_canvas.coords(snake_part.body_part)
            all_x_pos.append(int(c[0]))
            all_y_pos.append(int(c[1]))

        if prize is not None:
            tc = self.game_board_canvas.coords(prize.get())
            all_x_pos.append(int(tc[0]))
            all_y_pos.append(int(tc[1]))

        x_pos = random.randrange(0, 400, 10)
        y_pos = random.randrange(0, 300, 10)

        while x_pos in all_x_pos and y_pos in all_y_pos:
            x_pos = random.randrange(0, 400, 10)
            y_pos = random.randrange(0, 300, 10)

        self.box = self.game_board_canvas.create_rectangle(x_pos, y_pos, x_pos + 10, y_pos + 10,
                                                           outline='black',
                                                           fill='black'
                                                           )
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

