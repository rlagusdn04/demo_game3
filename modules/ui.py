import pygame
import os

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

    def show_dialogue(self, dialogue):
        print(dialogue)
        pass
        
    def inventory(self, screen):
        pass

    def hand_ui(self, screen):
        pass

    def dialogue(self, screen):
        pass

    def name_input(self, screen):
        input_active = True
        input_text = ""
        clock = pygame.time.Clock()
        
        # 입력창 색상 설정 (투명도를 주기 위해 알파 채널 사용)
        box_color = (50, 50, 50, 180)      # 입력창 배경 (투명도 180)
        border_color = (200, 200, 200)      # 테두리 색상
        text_color = (255, 255, 255)        # 텍스트 색상
        
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.player.name = input_text.strip() if input_text.strip() != "" else "Player"
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

            # 기존 배경 유지: 화면 전체를 지우지 않고 현재 화면 위에 입력창 UI만 오버레이함
            # screen.fill(bg_color) 호출 제거
            
            # 입력창 위치와 크기 (화면 중앙)
            box_width, box_height = 400, 50
            box_x = (self.width - box_width) // 2
            box_y = (self.height - box_height) // 2
            
            # 투명 배경을 가진 입력창 surface 생성
            input_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            input_surface.fill(box_color)
            
            # 입력창 surface를 화면에 블릿
            screen.blit(input_surface, (box_x, box_y))
            pygame.draw.rect(screen, border_color, (box_x, box_y, box_width, box_height), 2)
            
            # 입력된 텍스트 그리기
            text_surface = self.font.render(input_text, True, text_color)
            screen.blit(text_surface, (box_x + 10, box_y + 10))
            
            # 안내 문구 표시
            prompt = "Enter your name:"
            prompt_surface = self.font.render(prompt, True, text_color)
            prompt_rect = prompt_surface.get_rect(center=(self.width / 2, box_y - 20))
            screen.blit(prompt_surface, prompt_rect)
            
            pygame.display.flip()
            clock.tick(30)
