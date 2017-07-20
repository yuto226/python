# encoding:utf-8
import pygame
from Items import *
import random
import sys

SCREEN_SIZE = (640, 480)
SCR_WIDTH = 640
SCR_HEIGHT = 480

class Enemy(pygame.sprite.Sprite):
    """敵の雛形"""
    def __init__(self, pos, my_player):
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 中心座標をposに
        self.my_player = my_player
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.life <= 0:
            seed = random.randint(1,5)
            if seed == 1:
                Sushi1(self.rect.center)
            elif seed == 2:
                Sushi2(self.rect.center)
            self.kill()
            self.my_player.gain_exp(self.exp)
        if self.rect.left <= 0:
            sys.exit()

class Enemy1(Enemy):
    speed = 3
    life = 1
    exp = 1
    def __init__(self, pos, my_player):
        super(Enemy1,self).__init__(pos, my_player)

class Enemy2(Enemy):
    speed = 1
    life = 15
    exp = 10
    def __init__(self, pos, my_player):
        super(Enemy2,self).__init__(pos, my_player)
        self.timer = 100
    def update(self):
        if self.rect.left >= SCR_WIDTH/2:
            self.rect.move_ip(-self.speed,0)
        else:
            if self.timer == 0:
                self.timer = 1500
                for m in range(3):
                    Fireball(self.rect.move(-5,m*5).center,m)
            else:
                self.timer -= 1
        if self.life <= 0:
            seed = random.randint(1,5)
            if seed == 1:
                Sushi1(self.rect.center)
            elif seed == 2:
                Sushi2(self.rect.center)
            self.kill()

class Enemy3(Enemy):
    speed = 5
    life = 1
    exp = 3
    def __init__(self, pos, my_player):
        super(Enemy3,self).__init__(pos, my_player)

class Fireball(Enemy):
    def __init__(self, pos, num):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 中心座標をposに
        self.num = num
        self.speed = 2
        self.life = 1
    def update(self):
        if self.num == 0:
            self.rect.move_ip(-self.speed,-1)
        elif self.num == 1:
            self.rect.move_ip(-self.speed,0)
        elif self.num == 2:
            self.rect.move_ip(-self.speed,1)
        if self.life <= 0:
            self.kill()
