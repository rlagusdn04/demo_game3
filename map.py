import json
import pygame

TILE_SIZE = 32

def get_tile_image(tile_id):
    """
    타일 ID에 따라 간단한 Surface를 생성.
    실제 프로젝트에서는 타일셋 이미지를 사용하는 것이 좋음.
    """
    surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
    if tile_id == 0:
        surface.fill((100, 100, 100))  # 바닥 타일
    elif tile_id == 1:
        surface.fill((0, 0, 0))        # 벽 (충돌 타일)
    else:
        surface.fill((150, 150, 150))
    return surface

class Map:
    def __init__(self, name, map_type, width, height, tiles, objects, triggers, properties):
        self.name = name
        self.map_type = map_type
        self.width = width
        self.height = height
        self.tiles = tiles
        self.objects = objects
        self.triggers = triggers
        self.properties = properties
        # 기본적으로 벽(타일 ID 1)을 충돌 타일로 사용.
        self.collision_tiles = [1]

    def draw(self, screen):
        # 타일 그리기
        for y, row in enumerate(self.tiles):
            for x, tile_id in enumerate(row):
                tile_image = get_tile_image(tile_id)
                screen.blit(tile_image, (x * TILE_SIZE, y * TILE_SIZE))
        
        # 객체(아이템, NPC 등) 렌더링: 실제 객체 처리는 해당 모듈에서 할 수 있으므로, 여기서는 간단한 색상 표시 예시
        for obj in self.objects:
            obj_type = obj.get("type")
            obj_x = obj.get("x")
            obj_y = obj.get("y")
            if obj_type == "item":
                color = (0, 0, 255)
            elif obj_type == "npc":
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)
            rect = pygame.Rect(obj_x * TILE_SIZE, obj_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
        
        # 트리거 렌더링 (예시: 녹색 테두리)
        for trigger in self.triggers:
            trigger_x = trigger.get("x")
            trigger_y = trigger.get("y")
            rect = pygame.Rect(trigger_x * TILE_SIZE, trigger_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)

    def is_colliding(self, x, y):
        # 맵 경계 체크
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        # 지정된 타일이 충돌 타일인지 확인
        return self.tiles[y][x] in self.collision_tiles

def load_maps(filename):
    """
    주어진 JSON 파일에서 모든 맵 데이터를 로드하여, 
    맵 이름을 키로 갖는 딕셔너리 형태로 반환함.
    """
    with open(filename, "r") as f:
        data = json.load(f)
    
    maps = {}
    for map_data in data.get("maps", []):
        name = map_data.get("name")
        map_obj = Map(
            name = name,
            map_type = map_data.get("type"),
            width = map_data.get("width"),
            height = map_data.get("height"),
            tiles = map_data.get("tiles"),
            objects = map_data.get("objects", []),
            triggers = map_data.get("triggers", []),
            properties = map_data.get("properties", {})
        )
        maps[name] = map_obj
    return maps

# 예시: 단일 맵만 로드해서 사용하고 싶을 때
def load_map(filename, map_name):
    maps = load_maps(filename)
    return maps.get(map_name)
