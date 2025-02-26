import json
import pygame

TILE_SIZE = 32  

class Map:
    current_map = None  # 현재 활성화된 맵

    def __init__(self, name=None, map_type=None, width=0, height=0,
                 tiles=None, objects=None, triggers=None, properties=None):
        if name is None:
            self.maps = {}  # 매니저 역할일 경우 전체 맵 데이터 관리
        else:
            self.name = name
            self.map_type = map_type
            self.width = width
            self.height = height
            self.tiles = tiles or []
            self.objects = objects or []
            self.triggers = triggers or []
            self.properties = properties or {}
            self.collision_tiles = [1]  # 충돌 타일 ID 예시

    def load(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)

        self.maps = {}
        for map_data in data.get("maps", []):
            name = map_data.get("name")
            self.maps[name] = Map(
                name=name,
                map_type=map_data.get("type"),
                width=map_data.get("width"),
                height=map_data.get("height"),
                tiles=map_data.get("tiles"),
                objects=map_data.get("objects", []),
                triggers=map_data.get("triggers", []),
                properties=map_data.get("properties", {})
            )

        current_map_name = data.get("current_map")
        if current_map_name in self.maps:
            Map.set_current_map(self.maps[current_map_name])
        elif self.maps:
            Map.set_current_map(list(self.maps.values())[0])

    @classmethod
    def set_current_map(cls, map_obj):
        cls.current_map = map_obj

    @classmethod
    def get_current_map(cls):
        return cls.current_map

    @classmethod
    def get_current_map_name(cls):
        if cls.current_map:
            return cls.current_map.name
        return None

    @classmethod
    def draw_current_map(cls, screen, ui):
        if cls.current_map:
            cls.current_map.draw(screen, ui)

    def draw(self, screen, ui):
        camera_x, camera_y = ui.camera_x, ui.camera_y
        
        # 타일 그리기
        for y, row in enumerate(self.tiles):
            for x, tile_id in enumerate(row):
                tile_image = self.get_tile_image(tile_id)
                screen.blit(tile_image, ((x - camera_x) * TILE_SIZE, (y - camera_y) * TILE_SIZE))
        
        # 객체 그리기 (예: 아이템, NPC 등)
        for obj in self.objects:
            obj_type = obj.get("type")
            obj_x = obj.get("x")
            obj_y = obj.get("y")
            color = (0, 0, 255) if obj_type == "item" else (255, 0, 0)
            # 카메라 오프셋 적용
            rect = pygame.Rect((obj_x - camera_x) * TILE_SIZE, (obj_y - camera_y) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
        
        # 트리거 영역 그리기 (녹색 테두리)
        for trigger in self.triggers:
            trigger_x = trigger.get("x")
            trigger_y = trigger.get("y")
            # 카메라 오프셋 적용
            rect = pygame.Rect((trigger_x - camera_x) * TILE_SIZE, (trigger_y - camera_y) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)

    def is_colliding(self, x, y):
        if self.current_map:
            tile_id = self.current_map.get_tile_id(x, y)
            return tile_id in self.current_map.collision_tiles
        return False

    def get_tile_id(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    @staticmethod
    def get_tile_image(tile_id):
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        if tile_id == 0:
            surface.fill((100, 100, 100))  # 바닥 타일
        elif tile_id == 1:
            surface.fill((0, 0, 0))        # 충돌 타일(벽)
        else:
            surface.fill((150, 150, 150))
        return surface

    def check_collision_rect(self, rect):
        """
        주어진 rect(픽셀 단위)가 충돌 타일과 겹치는지 검사합니다.
        """
        left_tile = rect.left // TILE_SIZE
        right_tile = (rect.right - 1) // TILE_SIZE
        top_tile = rect.top // TILE_SIZE
        bottom_tile = (rect.bottom - 1) // TILE_SIZE
        for y in range(top_tile, bottom_tile + 1):
            for x in range(left_tile, right_tile + 1):
                tile_id = self.get_tile_id(x, y)
                if tile_id in self.collision_tiles:
                    return True
        return False
