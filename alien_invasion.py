# -*- coding:utf-8 -*-
import sys
import pygame


def run_game():
    pygame.init()  # 初始化游戏并创建一个屏幕对象
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption('Alien Invation')
    bg_color = (230, 230, 230) # 设置背景色, rgb; 浅灰色

    # 开始游戏主循环
    while 1:
        # 监视鼠标和事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # 每次循环是都重绘屏幕
        screen.fill(bg_color)

        # 让最近绘制的屏幕可见
        pygame.display.flip()


run_game()
