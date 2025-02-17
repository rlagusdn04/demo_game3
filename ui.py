import pygame

class UI:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont("Arial", 20)

    def draw_ui(self, screen):
        #상태창 ui 
        display_text = f"Player: {self.player.name} HP: {self.player.hp}"
        screen.blit(self.font.render(display_text, True, (255, 255, 255)), (10, 10))

    def camera(self, screen):
        # 플레이어를 비추는 카메라
        pass

    def inventory(self, screen):
        # 인벤토리 UI 
        pass

    def hand_ui(self, screen):
        # 손에 든 아이템 UI 
        pass

    def dioalogue(self, screen):
        # 대화 UI 
        pass