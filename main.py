import pygame
import json
from player import Player, TILE_SIZE
from map import Map 
from npc import load_npcs
from ui import UI

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():


    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # 플레이어 데이터 로드 (player.json)
    player = Player.load("data/player.json")
    print(f"Loaded player: {player.x}, {player.y}")

    # 맵 데이터 로드 (map.json)
    current_map = Map.load("data/map.json")

    # NPC 데이터 로드 (npc.json)
    npcs = load_npcs("data/npc.json")

    # UI 초기화 (플레이어 정보 표시 등)
    ui = UI(player)

    game_time = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    # 'E' 키를 눌러 상호작용
                    pass

        dt = clock.tick(60)  # 프레임별 경과 시간 (밀리초)
        game_time += dt     # 게임 전체의 누적 시간을 업데이트

        # 간단한 키 입력에 따른 플레이어 이동 (격자 단위 이동)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(0, -1, current_map, npcs)
        elif keys[pygame.K_s]:
            player.move(0, 1, current_map, npcs)
        elif keys[pygame.K_a]:
            player.move(-1, 0, current_map, npcs)
        elif keys[pygame.K_d]:
            player.move(1, 0, current_map, npcs)

        # 화면 그리기
        screen.fill((0, 0, 0))
        current_map.draw(screen)
        for npc in npcs:
            npc.draw(screen)
        player.draw(screen)
        ui.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    # 게임 종료 전에 플레이어 데이터를 저장할 수도 있음
    player.save("player.json")
    pygame.quit()

if __name__ == "__main__":
    print("1")
    main()
