import json
import pygame

TILE_SIZE = 32  

class SpriteSheet:
    def __init__(self, file_path, scale_factor=2):
        self.sheet = pygame.image.load(file_path)
        self.scale_factor = scale_factor

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        if self.scale_factor != 1:
            new_width = int(width * self.scale_factor)
            new_height = int(height * self.scale_factor)
            image = pygame.transform.scale(image, (new_width, new_height))
        return image

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
            self.sprite_sheet = SpriteSheet("assets/tiles.png")

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
                # 스프라이트 시트에서 불러온 이미지 크기와 화면 타일 크기가 다를 경우 위치 조정 필요
                screen.blit(tile_image , ((x - camera_x) * TILE_SIZE, (y - camera_y) * TILE_SIZE))
        
        # 객체 그리기 (예: 아이템, NPC 등)
        for obj in self.objects:
            obj_type = obj.get("type")
            obj_x = obj.get("x")
            obj_y = obj.get("y")
            color = (0, 0, 255) if obj_type == "item" else (255, 0, 0)
            rect = pygame.Rect((obj_x - camera_x) * TILE_SIZE, (obj_y - camera_y) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
        
        # 트리거 영역 그리기 (녹색 테두리)
        for trigger in self.triggers:
            trigger_x = trigger.get("x")
            trigger_y = trigger.get("y")
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

    def get_tile_image(self, tile_id):
        """
        tile_id 에 따라 스프라이트 시트에서 해당 타일 이미지를 추출합니다.
        여기서는 예시로 tile_id 0은 (0, 0), 1은 (TILE_SIZE, 0)에서 타일을 가져옵니다.
        """
        tile_mapping = {
            0: (0, 0, TILE_SIZE, TILE_SIZE),                   # 풀 타일
            1: (TILE_SIZE, TILE_SIZE, TILE_SIZE/2, TILE_SIZE/2),            # 물 타일
            2: (TILE_SIZE, 0, TILE_SIZE/2, TILE_SIZE/2)
            # 추가 타일 ID와 좌표를 매핑할 수 있습니다.
        }
        if tile_id in tile_mapping:
            x, y, width, height = tile_mapping[tile_id]
            return self.sprite_sheet.get_image(x, y, width, height)
        else:
            # 정의되지 않은 타일 ID는 기본 Surface를 반환합니다.
            default_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            default_image.fill((150, 150, 150))
            return default_image

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
