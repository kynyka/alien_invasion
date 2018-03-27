# -*- coding:utf-8 -*-
import pygame


class Ship():
    def __init__(self, ai_settings, screen):
        '''初始化飞船并设置其初始位置'''
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.png')  # 返回表示飞船的surface并存于变量
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx  # 左上角(0, 0)
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''根据移动标志调整飞船的位置'''
        # 以飞船的center值作为替代进行更新, 而不是rect
        if self.moving_right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left:
            self.center -= self.ai_settings.ship_speed_factor  # elif则右向键居优先地位

        # 根据self.center更新rect对象
        self.rect.centerx = self.center  # rect的centerx等属性只能存储整数值

    def blitme(self):
        '''在指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect)
