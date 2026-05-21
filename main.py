import pygame

clock = pygame.time.Clock()
pygame.init()

screen = pygame.display.set_mode((1280, 748))
pygame.display.set_caption("The Ghost Hunter")

bg = pygame.image.load('images/bg.png').convert_alpha()

PLAYER_SIZE = (180, 180)
GHOST_SIZE = (170, 170)
BULLET_SIZE = (50, 50)

walk_left = [
    pygame.transform.scale(pygame.image.load('images/player_left/1.1.png').convert_alpha(), PLAYER_SIZE),
    pygame.transform.scale(pygame.image.load('images/player_left/1.2.png').convert_alpha(), PLAYER_SIZE),
    pygame.transform.scale(pygame.image.load('images/player_left/1.3.png').convert_alpha(), PLAYER_SIZE),
]

walk_right = [
    pygame.transform.scale(pygame.image.load('images/player_right/2.1.png').convert_alpha(), PLAYER_SIZE),
    pygame.transform.scale(pygame.image.load('images/player_right/2.2.png').convert_alpha(), PLAYER_SIZE),
    pygame.transform.scale(pygame.image.load('images/player_right/2.3.png').convert_alpha(), PLAYER_SIZE),
]

ghost = pygame.transform.scale(pygame.image.load('images/gohst.png').convert_alpha(), GHOST_SIZE)
ghost_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 13
player_x = 150
player_y = 450
is_jump = False
jump_count = 11

bg_music = pygame.mixer.Sound('music/song1.mp3')
bg_music.play()

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 5500)

label = pygame.font.Font('fonts/font1.ttf', 100)
lose_label = label.render('ВЫ ПРОИГРАЛИ!', False, (0, 0, 0))
restart_label = label.render('Играть заново', False, (128, 0, 0))
restart_label_rect = restart_label.get_rect(topleft=(640, 200))

bullets_left = 5
bullet = pygame.transform.scale(pygame.image.load('images/bullet.png').convert_alpha(), BULLET_SIZE)
bullets = []

gameplay = True
running = True

while running:
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1280, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i, el) in enumerate(ghost_list_in_game):
                screen.blit(ghost, el)
                el.x -= 10

                if el.x < -10:
                    ghost_list_in_game.pop(i)

                player_hitbox = player_rect.inflate(-60, -60)
                ghost_hitbox = el.inflate(-60, -60)

                if player_hitbox.colliderect(ghost_hitbox):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 600:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -11:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 11

        if player_anim_count == 2:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -1280:
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 15

                if el.x > 1280:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, ghost_el) in enumerate(ghost_list_in_game):
                        if el.colliderect(ghost_el):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()

        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(1290, 500)))

        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_a and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 150, player_y + 50)))
            bullets_left -= 1

    clock.tick(20)