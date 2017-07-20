#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys
import os
import random
from Enemys import *
from Player import *
from Items import *

SCREEN_SIZE = (640, 480)
SCR_WIDTH = 640
SCR_HEIGHT = 480
SCR_RECT = Rect(0, 0, 640 / 4, 480)#main_char移動制限範囲

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Takuro Shooting　-Returns-")

    # フォントの作成
    sysfont = pygame.font.SysFont(None, 30)
    # テキストを描画したSurfaceを作成
    hello1 = sysfont.render("Life:", False, (0,0,255))
    hello2 = sysfont.render("Score:", True, (0,0,255))
    hello3 = sysfont.render("Level:", True, (0,0,255))

    # スプライトグループを作成して登録
    all = pygame.sprite.RenderUpdates()
    enemys = pygame.sprite.Group()  # エイリアングループ
    shots = pygame.sprite.Group()   # ミサイルグループ
    player = pygame.sprite.Group()  #プレイヤーグループ
    items = pygame.sprite.Group() #アイテムグループ
    sp_shots = pygame.sprite.Group() #sp_shotグループ
    shields = pygame.sprite.Group()
    zyoheki = pygame.sprite.Group()

    Player.containers = all, player
    Shot.containers = all, shots
    Shot2.containers = all,sp_shots
    Enemy.containers = all, enemys
    Sushi1.containers = all, items
    Sushi2.containers = all, items
    Shield.containers = all, shields
    Zyoheki.containers = all, zyoheki

    # スプライトの画像を登録
    Player.image = load_image("main_char.png")
    Shot.image = load_image("shot.png")
    Shot2.image = load_image("shot3.png")
    Enemy1.image = load_image("enemy1.png")
    Enemy2.image = load_image("enemy2.png")
    Enemy3.image = load_image("enemy3.png")
    Sushi1.image = load_image("sushi1.png")
    Sushi2.image = load_image("sushi2.png")
    Shield.image = load_image("shield.png")
    Zyoheki.image = load_image("zyoheki.png")
    Fireball.image = load_image("fireball.png")

    m_boss_flag = True
    for m in range(1,5):
        Zyoheki((-20,m*100))
    #スコアボード生成
    score_board = ScoreBoard()
    # 自機を作成
    my_player = Player(score_board)
    #初めの敵を生成
    Enemy1([SCR_WIDTH,200], my_player)
    enemy_interval = 100
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        enemy_interval -= 1
        # 衝突判定
        collision_detection_enemy(shots, enemys,score_board)
        collision_detection_self(player, enemys,score_board)
        collision_detection_item(player, items, my_player)
        collision_detection_spshot(sp_shots,enemys,score_board)
        collision_detection_shield(shields, enemys, score_board, my_player)
        collision_detection_zyoheki(zyoheki, enemys)
        screen.fill((0, 0, 0))
        # スコアボードを描画する。
        score_board.draw(screen)
        screen.blit(hello1, (250,20))
        screen.blit(hello2, (320,20))
        screen.blit(hello3, (430,20))
        my_player.reload_method()
        my_player.level_up(score_board)
        if my_player.reload_timer_rocket <= 0 and my_player.level >= 3 and score_board.score >= 50:
            screen.blit(load_image("shot3.gif"),(0,0))
        if my_player.level >= 5 and score_board.score >= 200:
            screen.blit(load_image("shield_tag.png"),(46,0))
        all.update()
        all.draw(screen)
        pygame.display.update()
        # 敵生成アルゴリズム
        seed = random.randint(1,my_player.range_interval)
        height = random.randint(50,400)
        if seed == 50 or seed == 51 or seed == 52:
            Enemy1([SCR_WIDTH,height], my_player)
            enemy_interval = 100
        if seed == 80 and my_player.level >= 6:
            Enemy3([SCR_WIDTH,height], my_player)
            enemy_interval = 100
        #敵が出な過ぎる時の処理
        if enemy_interval <= 0:
            Enemy1([SCR_WIDTH,height], my_player)
            enemy_interval = 100
        #中ボス
        if my_player.level % 5 == 0 and score_board.m_boss_flag == True:
            Enemy2([SCR_WIDTH,SCR_HEIGHT/2], my_player)
            score_board.m_boss_flag = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

def load_image(filename, colorkey=None):
    """画像をロードして画像と矩形を返す"""
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def collision_detection_enemy(shots, enemys, score_board):
    """敵ダメージ衝突判定"""
    enemy_collided = pygame.sprite.groupcollide(enemys, shots, False, True)
    for enemy in enemy_collided.keys():
        enemy.life -= 1
        score_board.add_score(1)

def collision_detection_spshot(sp_shots, enemys, score_board):
    """キラー衝突判定"""
    enemy_collided = pygame.sprite.groupcollide(enemys, sp_shots, False, False)
    sp_shots_collided = pygame.sprite.groupcollide(sp_shots, enemys, False, False)
    for enemy in enemy_collided.keys():
        enemy.life -= 1
        score_board.add_score(2)

    for sp_shot in sp_shots_collided.keys():
        sp_shot.life -= 1

def collision_detection_shield(shields, enemys, score_board, my_player):
    shield_collided = pygame.sprite.groupcollide(shields, enemys, False, True)
    for shield in shield_collided.keys():
        shield.life -= 1
        score_board.life += 1
        my_player.life += 1

def collision_detection_self(player, enemys, score_board):
    """自機ダメージ衝突判定"""
    # 敵と自機の衝突判定
    player_collided = pygame.sprite.groupcollide(player, enemys, False, True)
    for player in player_collided.keys():
        player.life -= 1
        score_board.reduce_life(1)
def collision_detection_zyoheki(zyoheki, enemys):
    zyoheki_collided = pygame.sprite.groupcollide(zyoheki, enemys, False, True)
    for zyoheki in zyoheki_collided.keys():
        zyoheki.life -= 1
        zyoheki.damage()

def collision_detection_item(player, items,my_player):
    """アイテム取得判定"""
    # 敵と自機の衝突判定
    item_collided = pygame.sprite.groupcollide(items, player, True, False)
    player_collided = pygame.sprite.groupcollide(player, items, False, True)
    # ↑には、第一引数のオブジェクト情報が格納されている。それと接触する全ての第二引数オブジェクトリスト
    for item in item_collided.keys():
        if item.item_type == 1:
            if my_player.speed < 15:
                my_player.speed += 0.5
        elif item.item_type == 2:
            if my_player.reload_time > 10:
                my_player.reload_time -= 0.5

class ScoreBoard():
    """スコアボード"""
    def __init__(self):
        self.sysfont = pygame.font.SysFont(None, 30)
        self.score = 0
        self.life = 5
        self.level = 1
        self.m_boss_flag = True
    def draw(self, screen):
        score_img = self.sysfont.render(str(self.score), True, (255,255,0))
        life_img = self.sysfont.render(str(self.life), True, (255,255,0))
        level_img = self.sysfont.render(str(self.level), True, (255,255,0))
        #x = (SCR_RECT.size[0] - score_img.get_width()) / 2
        #y = (SCR_RECT.size[1] - score_img.get_height()) / 2
        screen.blit(level_img,(490,20))
        screen.blit(score_img, (390, 20))
        screen.blit(life_img, (300, 20))
    def add_score(self, x):
        self.score += 10 * x

    def reduce_life(self, x):
        self.life -= 1 * x

if __name__ == "__main__":
    main()
