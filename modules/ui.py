import pygame

TILE_SIZE = 32

class UI:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont("Arial", 20)
        self.width = 800         # 화면 가로 크기 (픽셀)
        self.height = 600        # 화면 세로 크기 (픽셀)
        # camera_x, camera_y는 타일 단위 좌표로 사용
        self.camera_x = 0        
        self.camera_y = 0        

    def draw_ui(self, screen):
        # 상태창 UI: 플레이어 이름과 HP 표시
        display_text = f"Player: {self.player.name} HP: {self.player.hp}"
        screen.blit(self.font.render(display_text, True, (255, 255, 255)), (10, 10))
        
        # 상호작용 안내 UI: 'E'키 누르라는 메시지
        update_text = "Press 'E' to interact"
        screen.blit(self.font.render(update_text, True, (255, 255, 255)), (10, 40))

    def update(self, player):
        # 화면의 픽셀 단위를 타일 단위로 변환 (예: 800px -> 25타일, 600px -> 18.75타일)
        screen_tiles_x = self.width / TILE_SIZE
        screen_tiles_y = self.height / TILE_SIZE

        # 플레이어를 화면 중앙에 두기 위한 카메라 목표 좌표 계산 (타일 단위)
        target_x = player.x - screen_tiles_x / 2
        target_y = player.y - screen_tiles_y / 2

        # 즉시 목표 좌표로 이동 (부드러운 이동을 원하면 lerp_factor를 0과 1 사이로 조정)
        lerp_factor = 1  # 1이면 즉시 이동
        self.camera_x += (target_x - self.camera_x) * lerp_factor
        self.camera_y += (target_y - self.camera_y) * lerp_factor

        
    def inventory(self, screen):
        pass

    def hand_ui(self, screen):
        pass

    def dialogue(self, screen):
        pass

import os
import pygame

