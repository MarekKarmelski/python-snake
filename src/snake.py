#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Snake class."""


class Snake:

    moves = None
    id = None
    body_part = None
    x_pos = None
    y_pos = None

    def __init__(self):
        self.moves = []
        self.id = None
        self.body_part = None
        self.x_pos = 10
        self.y_pos = 0

    def add_move(self, move):
        self.moves.append(move)
