# encoding:utf-8
import pygame
from pygame.locals import *
import sys
import time
#���ʒ萔
SCREEN_SIZE = (640, 480)
SCR_WIDTH = 640
SCR_HEIGHT = 480
SCR_RECT = Rect(0, 0, 640 / 4, 480)#main_char�ړ������͈�

class Zyoheki(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # ���S���W��pos��
        self.life = 2

    def update(self):
        if self.life <= 0:
            self.kill()

    def damage(self):
        self.rect.move_ip(-15,0)
class Shot(pygame.sprite.Sprite):
    """�v���C���[�����˂���e�e"""
    speed = 5  # �ړ����x
    def __init__(self, pos):
        # image��containers��main()�ŃZ�b�g
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # ���S���W��pos��
        self.max_length = SCR_WIDTH/2
    def update(self):
        self.rect.move_ip(self.speed,0 )  # �E�ֈړ�
        if self.rect.left > self.max_length:  # ���E�ɒB�����珜��
            self.kill()

class Shot2(pygame.sprite.Sprite):
    """�v���C���[�����˂��郍�P�b�g"""
    speed = 10  # �ړ����x
    def __init__(self, pos, which):
        # image��containers��main()�ŃZ�b�g
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # ���S���W��pos��
        self.life = 2
        self.max_length = SCR_WIDTH
        if which == 'left':
            self.rect.move_ip(0,self.speed*8)  # �E�ֈړ�
        else:
            self.rect.move_ip(0, -self.speed*8)
    def update(self):
        self.rect.move_ip(self.speed,0)
        if self.rect.left > self.max_length or self.life <= 0: # ���E�ɒB�����珜��
            self.kill()

class Shield(pygame.sprite.Sprite):
    """�v���C���[�̔�������"""
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.life = 3
        self.time = 800

    def update(self):
        self.time -= 1
        if self.life <= 0 or self.time <= 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    """���@"""
    def __init__(self, score_board):
        # image��containers��main()�ŃZ�b�g
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.score_board = score_board
        self.rect = self.image.get_rect()
        self.rect.top = SCR_HEIGHT/2
        self.reload_timer = 0
        self.reload_timer_rocket = 0
        self.life = 5
        self.level = 1
        self.exp = 0
        self.next_exp = 8
        self.speed = 2  # �ړ����x
        self.reload_time = 30  # �����[�h����
        self.reload_rocket = 350 #�@���P�b�g�����[�h
        self.range_interval = 500
    def update(self):
        # ������Ă���L�[���`�F�b�N
        if self.life <= 0:
            self.kill()
            time.sleep(2)
            sys.exet()
        pressed_keys = pygame.key.get_pressed()
        # ������Ă���L�[�ɉ����ăv���C���[���ړ�
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        elif pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        elif pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)

        self.rect.clamp_ip(SCR_RECT)
        # �e�ۂ̔���
        if pressed_keys[K_SPACE]:
            # �����[�h���Ԃ�0�ɂȂ�܂ōĔ��˂ł��Ȃ�
            if self.reload_timer <= 0:
                # ���ˁI�I�I
                #Player.shot_sound.play()
                Shot(self.rect.center)  # �쐬����Ɠ�����all�ɒǉ������
                self.reload_timer = self.reload_time
        elif pressed_keys[K_RETURN]:
            # �����[�h���Ԃ�0�ɂȂ�܂ōĔ��˂ł��Ȃ�
            if self.reload_timer_rocket <= 0 and self.level >= 3 and self.score_board.score >= 50:
                # ���ˁI�I�I
                #Player.shot_sound.play()
                Shot2(self.rect.center,'left')  # �쐬����Ɠ�����all�ɒǉ������
                Shot2(self.rect.center,'right')  # �쐬����Ɠ�����all�ɒǉ������
                self.reload_timer_rocket = self.reload_rocket
                self.score_board.score -= 50

        if pressed_keys[K_s]:
            if self.level >= 5 and self.score_board.score >= 200:
                self.score_board.score -= 200
                Shield(self.rect.move(20,0).center)

    def reload_method(self):
        if self.reload_timer > 0:
            self.reload_timer -= 1
        if self.reload_timer_rocket > 0:
            self.reload_timer_rocket -= 1

    def gain_exp(self, x):
        self.exp += x

    def level_up(self, score_board):
        if self.exp >= self.next_exp:
            flag = False
            if self.level % 5 == 0 and score_board.m_boss_flag == False:
                flag = True
            self.level += 1
            if flag == True:
                score_board.m_boss_flag = True
                self.range_interval -= 20
            score_board.level += 1
            self.next_exp *= 1.3
