# encoding:utf-8
import pygame
class Item(pygame.sprite.Sprite):
    """アイテムの基底クラス"""
    speed = 2
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 中心座標をposに
    def update(self):
        self.rect.move_ip(-self.speed,0)

class Sushi1(Item):
    def __init__(self,pos):
        self.item_type = 1 #speed up
        super(Sushi1,self).__init__(pos)

class Sushi2(Item):
    def __init__(self,pos):
        self.item_type = 2 #fast reload
        super(Sushi2,self).__init__(pos)
