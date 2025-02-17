import pygame
import json
from player import TILE_SIZE  # TILE_SIZE가 player.py에서 정의되어 있다고 가정

class NPC:
    def __init__(self, x, y, sprite_path, name, dialogue=None):
        self.x = x
        self.y = y
        self.sprite_path = sprite_path
        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.name = name
        # 대화 데이터는 리스트 형태로 저장됨
        self.dialogue = dialogue if dialogue is not None else []

    def draw(self, screen):
        # NPC 스프라이트를 타일 크기 단위 위치에 그림
        screen.blit(self.sprite, (self.x * TILE_SIZE, self.y * TILE_SIZE))

    def get_dialogue(self, index=0):
        """
        현재 대화 노드를 반환.
        index 값에 따라 다음 대화 노드를 선택할 수 있음.
        예) index=0: 현재 대화, index=1: 다음 대화
        """
        if self.dialogue and 0 <= index < len(self.dialogue):
            return self.dialogue[index]
        return None

def load_npcs(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    
    npcs = []
    for npc_data in data.get("npcs", []):
        npc = NPC(
            x=npc_data["x"],
            y=npc_data["y"],
            sprite_path=npc_data["sprite"],
            name=npc_data["name"],
            dialogue=npc_data.get("dialogue")
        )
        npcs.append(npc)
    return npcs
