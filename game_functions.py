# -*- coding:utf-8 -*-
import sys
import pygame

def check_events(ship):
    '''相应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                # 向右移动飞船
                ship.rect.centertx += 1  # 同时给函数增加必要的形参

def update_screen(ai_settings, screen, ship):
        '''更新屏幕上的图像, 并切换到新屏幕'''
        screen.fill(ai_settings.bg_color)
        ship.blitme()

        # 让最近绘制的屏幕可见
        pygame.display.flip()