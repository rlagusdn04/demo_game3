import pygame
import json

TILE_SIZE = 32  # 타일 크기

class Player:
    def __init__(self, name, x, y, sprite_path, hp=100, level=1, exp=0, money=0, inventory=None):
        self.name = name
        self.x = x
        self.y = y
        self.sprite_path = sprite_path
        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.hp = hp
        self.level = level
        self.exp = exp
        self.money = money
        self.inventory = inventory if inventory is not None else []  # 인벤토리는 아이템 목록

    def draw(self, screen):
        screen.blit(self.sprite, (self.x * TILE_SIZE, self.y * TILE_SIZE))

    def move(self, dx, dy, current_map, npcs):
        new_x = self.x + dx
        new_y = self.y + dy

        # 맵 경계 및 타일 충돌 체크
        if current_map.is_colliding(new_x, new_y):
            return  # 이동 불가

        # NPC와의 충돌 체크
        for npc in npcs:
            if (npc.x, npc.y) == (new_x, new_y):
                # NPC와 상호작용 (대화 등 추후 UI에서 처리)
                print(f"상호작용: {npc.name}")
                return

        # 충돌이 없으면 이동
        self.x = new_x
        self.y = new_y

    @classmethod
    def load(cls, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        return cls(
            name=data.get("name", "Hero"),
            x=data["x"],
            y=data["y"],
            sprite_path=data["sprite"],
            hp=data.get("hp", 100),
            level=data.get("level", 1),
            exp=data.get("exp", 0),
            money=data.get("money", 0),
            inventory=data.get("inventory", [])
        )

    def save(self, filename):
        data = {
            "name": self.name,
            "sprite": self.sprite_path,
            "x": self.x,
            "y": self.y,
            "hp": self.hp,
            "level": self.level,
            "exp": self.exp,
            "money": self.money,
            "inventory": self.inventory
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
