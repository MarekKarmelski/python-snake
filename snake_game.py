#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""SNAKE GAME."""

from tkinter import *
from src.snake import Snake
from src.prize import Prize
from src.trap import Trap
import time
import copy

"""SnakeGame class."""


class SnakeGame:

    game_board = None

    game_board_canvas = None

    snake = []

    move_positions = []

    prize = None

    speed = 40

    game = True

    level = None

    score = 0

    score_label_text = None

    snake_length = None

    traps = []

    def __init__(self):
        self.init_game_board()
        self.init_game_board_canvas()
        self.init_snake()
        self.init_prize()
        self.init_traps()

    def init_game_board(self):
        self.game_board = Tk()
        self.game_board.wm_title('SNAKE GAME v1.0')
        self.game_board.resizable(width=False, height=False)

        self.score_label_text = StringVar()
        self.score_label_text.set('SCORE: 0')
        score_label = Label(self.game_board, textvariable=self.score_label_text)
        score_label.grid(column=0, row=1)

        self.snake_length = StringVar()
        self.snake_length.set('SNAKE LENGTH: 3')
        snake_length_label = Label(self.game_board, textvariable=self.snake_length)
        snake_length_label.grid(column=1, row=1)

        self.level = StringVar()
        self.level.set('LEVEL: 1')
        level_label = Label(self.game_board, textvariable=self.level)
        level_label.grid(column=2, row=1)

        exit_btn = Button(self.game_board, text='Exit', pady=10, command=self.game_board.destroy)
        exit_btn.grid(column=1, row=2)

    def init_game_board_canvas(self):
        self.game_board_canvas = Canvas(
            self.game_board,
            highlightthickness=0,
            bg='#6B8E23',
            width=400,
            height=300
        )
        self.game_board_canvas.grid(column=0, row=0, columnspan=3)

    def init_prize(self):
        self.prize = Prize(self.game_board_canvas, self.snake, self.traps)

    def init_traps(self):
        self.traps.append(Trap(self.game_board_canvas, self.snake, self.prize))
        self.traps.append(Trap(self.game_board_canvas, self.snake, self.prize))
        self.traps.append(Trap(self.game_board_canvas, self.snake, self.prize))

    def init_snake(self):
        head = Snake()
        head.body_part = self.game_board_canvas.create_rectangle(120, 100, 130, 110,
                                                                 outline='#006400',
                                                                 fill='#008000',
                                                                 tags='S1'
                                                                 )
        head.id = 'S1'
        body = Snake()
        body.body_part = self.game_board_canvas.create_rectangle(110, 100, 120, 110,
                                                                 outline='#006400',
                                                                 fill='#32CD32',
                                                                 tags='S2'
                                                                 )
        body.id = 'S2'
        tail = Snake()
        tail.body_part = self.game_board_canvas.create_rectangle(100, 100, 110, 110,
                                                                 outline='#006400',
                                                                 fill='#32CD32',
                                                                 tags='S3'
                                                                 )
        tail.id = 'S3'
        self.snake = [head, body, tail]

    def move_snake(self, event, current_snake):
        p = self.game_board_canvas.coords(current_snake[0].body_part)

        if current_snake[0].x_pos == 10 and current_snake[0].y_pos == 0:
            not_allowed_direction = 'Left'
        elif current_snake[0].x_pos == -10 and current_snake[0].y_pos == 0:
            not_allowed_direction = 'Right'
        elif current_snake[0].x_pos == 0 and current_snake[0].y_pos == -10:
            not_allowed_direction = 'Down'
        elif current_snake[0].x_pos == 0 and current_snake[0].y_pos == 10:
            not_allowed_direction = 'Up'
        else:
            not_allowed_direction = ''

        if event.keysym != not_allowed_direction:
            if len(self.move_positions) > 0:
                l = self.move_positions[len(self.move_positions) - 1]
                if l[0] == p[0] and l[1] == p[1] and l[2] == p[2] and l[3] == p[3]:
                    del self.move_positions[len(self.move_positions) - 1]

            if event.keysym == 'Right':
                self.move_positions.append([p[0], p[1], p[2], p[3], 10, 0])
            elif event.keysym == 'Left':
                self.move_positions.append([p[0], p[1], p[2], p[3], -10, 0])
            elif event.keysym == 'Up':
                self.move_positions.append([p[0], p[1], p[2], p[3], 0, -10])
            elif event.keysym == 'Down':
                self.move_positions.append([p[0], p[1], p[2], p[3], 0, 10])

    def update_level_label(self, level):
        self.level.set('LEVEL: ' + str(level))

    def str_coords(self, coords):
        return ''.join(list(map(lambda x: str(int(x)), coords)))

    def game_over_text(self):
        self.game_board_canvas.create_text(200, 150,
                                           text='GAME OVER!',
                                           font=('Purisa', 40, 'bold'),
                                           fill='orange'
                                           )

    def play(self):
        while self.game:
            level = len(self.snake) // 3
            snake_speed = (self.speed - level) / 100
            if self.speed <= 0.01:
                time.sleep(0.01)
            else:
                self.update_level_label(level)
                time.sleep(snake_speed)

            for trap in self.traps:
                trap.increase_current_life_time()
                if trap.can_remove():
                    trap.remove()
                    self.traps.remove(trap)
                    self.traps.append(Trap(self.game_board_canvas, self.snake, self.prize))

            if self.prize is not None:
                self.prize.increase_current_life_time()
                if self.prize.can_remove():
                    self.prize.remove()
                    self.prize = None
                    self.prize = Prize(self.game_board_canvas, self.snake, self.traps)

            if self.prize is not None:
                head = self.snake[0]
                tail = self.snake[len(self.snake) - 1]
                pc = self.game_board_canvas.coords(self.prize.get())
                hc = self.game_board_canvas.coords(head.body_part)
                tc = self.game_board_canvas.coords(tail.body_part)
                if pc[0] == hc[0] and pc[1] == hc[1] and pc[2] == hc[2] and pc[3] == hc[3]:
                    np = Snake()
                    np.body_part = self.game_board_canvas.create_rectangle(tc[0] - tail.x_pos, tc[1] - tail.y_pos,
                                                                           tc[2] - tail.x_pos, tc[3] - tail.y_pos,
                                                                           outline='#006400',
                                                                           fill='#32CD32',
                                                                           tags=('ss' + str(len(self.snake) + 1)))
                    np.id = 'S' + str(len(self.snake) + 1)
                    np.x_pos = tail.x_pos
                    np.y_pos = tail.y_pos
                    np.moves = []
                    for m in tail.moves:
                        np.moves.append(m)
                    self.snake.append(np)
                    self.score += self.prize.value
                    self.score_label_text.set('SCORE: ' + str(self.score))
                    self.snake_length.set('SNAKE LENGTH: ' + str(len(self.snake)))
                    self.prize.remove()
                    self.prize = None
                    self.prize = Prize(self.game_board_canvas, self.snake, self.traps)

            if len(self.move_positions) > 0:
                pos = self.move_positions[0]
                for sp in self.snake:
                    sp.add_move(pos)
                del self.move_positions[0]

            for snake_part in self.snake:
                c = self.game_board_canvas.coords(snake_part.body_part)
                if len(snake_part.moves) > 0:
                    m = snake_part.moves[0]
                    if c[0] == m[0] and c[1] == m[1] and c[2] == m[2] and c[3] == m[3]:
                        snake_part.x_pos = m[4]
                        snake_part.y_pos = m[5]
                        del snake_part.moves[0]
                self.game_board_canvas.move(snake_part.body_part, snake_part.x_pos, snake_part.y_pos)
                if c[2] >= 400 and snake_part.x_pos == 10:
                    self.game_board_canvas.coords(snake_part.body_part, [0, c[1], 10, c[3]])
                if c[0] <= 0 and snake_part.x_pos == -10:
                    self.game_board_canvas.coords(snake_part.body_part, [390, c[1], 400, c[3]])
                if c[3] >= 300 and snake_part.y_pos == 10:
                    self.game_board_canvas.coords(snake_part.body_part, [c[0], 0, c[2], 10])
                if c[1] <= 0 and snake_part.y_pos == -10:
                    self.game_board_canvas.coords(snake_part.body_part, [c[0], 290, c[2], 300])

            snake_body = copy.copy(self.snake)
            del snake_body[0]

            sh_cords = self.str_coords(self.game_board_canvas.coords(self.snake[0].body_part))
            for snake_body_part in snake_body:
                sbp_str_cords = self.str_coords(self.game_board_canvas.coords(snake_body_part.body_part))
                if sh_cords == sbp_str_cords:
                    self.game_over_text()
                    self.game = False
                    break

            if len(self.traps) > 0:
                head = self.snake[0]
                hc = self.game_board_canvas.coords(head.body_part)
                for trap in self.traps:
                    tc = self.game_board_canvas.coords(trap.get())
                    if tc[0] == hc[0] and tc[1] == hc[1] and tc[2] == hc[2] and tc[3] == hc[3]:
                        self.game_over_text()
                        self.game = False
                        break

            self.game_board.bind('<Key>', lambda event, current_snake=self.snake: self.move_snake(event, current_snake), add='')
            self.game_board_canvas.update()
        self.game_board.mainloop()

snake_game = SnakeGame()
snake_game.play()
