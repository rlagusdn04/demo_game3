import pygame
from modules.map import Map
from modules.npc import NPCManager
from modules.player import Player, TILE_SIZE
from modules.ui import UI

screen_width = 800
screen_height = 600

def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("게임 타이틀")

    clock = pygame.time.Clock()

    # 맵, NPC, 플레이어, UI 초기화
    map_manager = Map()
    map_manager.load("data/map.json")
    current_map = Map.get_current_map()
    print("현재 맵:", Map.get_current_map_name())

    npc_manager = NPCManager()
    npc_manager.load("data/npc.json")

    player = Player()
    player.load("data/player.json")

    ui = UI(player)

    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    npcs_here = npc_manager.get_npcs(current_map)
                    if npcs_here:
                        dialogue = npcs_here[0].get_dialogue()
                        if dialogue:
                            print(f"{npcs_here[0].name} 대화: {dialogue}")

        # 키 입력에 따른 플레이어 이동 (WASD)
        keys = pygame.key.get_pressed()
        npcs_on_map = npc_manager.get_npcs(current_map)
        if keys[pygame.K_w]:
            player.move(0, -1, current_map, npcs_on_map)
        elif keys[pygame.K_s]:
            player.move(0, 1, current_map, npcs_on_map)
        elif keys[pygame.K_a]:
            player.move(-1, 0, current_map, npcs_on_map)
        elif keys[pygame.K_d]:
            player.move(1, 0, current_map, npcs_on_map)

        player.animator.update(dt)

        # 카메라 업데이트 (플레이어 중심으로)
        ui.update(player)

        # 화면 초기화
        screen.fill((0, 0, 0))

        # 카메라 오프셋을 이용해 월드를 그리기
        Map.draw_current_map(screen, ui)  
        for npc in npcs_on_map:
            npc.draw(screen, ui)         
        player.draw(screen, ui)             

        # UI는 월드 위에 고정된 좌표로 그리기 (카메라 오프셋 미적용)
        ui.draw_ui(screen)
        pygame.display.flip()

    player.save("data/player.json")
    pygame.quit()

if __name__ == "__main__":
    main()
