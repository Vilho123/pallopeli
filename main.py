import pygame

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

# pygame setup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.y -= 10

    def draw(self, surface):
        pygame.draw.circle(surface, "black", (self.x, self.y), bullet_size)

class NPC:
    def __init__(self):
        #self.rect = pygame.Vector2(random.randint(0, SCREEN_WIDTH), 20)
        self.rect = pygame.Rect(20, 20, 40, 40)
        self.x = self.rect.x
        self.y = self.rect.y
    
    def bullet_collision(self, x, y):
        bullet_collide = self.rect.collidepoint(x, y)
        return bullet_collide

    def player_collision(self, x, y):
        player_collide = self.rect.collidepoint(x, y)
        return player_collide
    
    def right(self):
        self.rect.x += speed
        self.x += speed

    def left(self):
        self.rect.x -= speed
        self.x -= speed
    
    def down(self):
        self.rect.y += 50
        self.y += 50

    def draw(self, surface):
        pygame.draw.rect(surface, "red", self.rect, npc_size)

npc_size = 20
bullet_size = 5

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 25)
npc_pos = pygame.Vector2(screen.get_width() / 2, 20)

shooting = False
bullet = None

npc = False
max_npcs = 3

moving_right = True
moving_left = False

score = 0
final_score = 0

font = pygame.font.SysFont(None, 24)

npcs = []

speed = 3

game_state = "start_menu"

def draw_start_menu():
    font_game_title = pygame.font.SysFont(None, 40)
    font_game_screen = pygame.font.SysFont(None, 32)
    screen.fill("gray")
    title = font_game_title.render("Game", True, "blue")
    start_game = font_game_screen.render("Start", True, "red")
    quit_game = font_game_screen.render("Quit", True, "red")
    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 40))
    screen.blit(start_game, (SCREEN_WIDTH / 2 - start_game.get_width() / 2, 125))
    screen.blit(quit_game, (SCREEN_WIDTH / 2 - quit_game.get_width() / 2, 250))
    pygame.display.update()

def draw_game_over_screen(p):
    font_game_over_title = pygame.font.SysFont(None, 40)
    font_game_over = pygame.font.SysFont(None, 32)
    screen.fill("gray")
    title = font_game_over_title.render("Game Over", True, "yellow")
    restart_button = font_game_over.render('Restart', True, (255, 255, 255))
    quit_button = font_game_over.render('Quit', True, (255, 255, 255))
    final_score = font_game_over_title.render('Final Score {}'.format(p), True, "blue")
    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 40))
    screen.blit(restart_button, (SCREEN_WIDTH / 2 - restart_button.get_width() / 2, 120))
    screen.blit(quit_button, (SCREEN_WIDTH / 2 - quit_button.get_width() / 2, 180))
    screen.blit(final_score, (SCREEN_WIDTH / 2 - final_score.get_width() / 2, 280))
    pygame.display.update()

sprites = []
start_button_rect = pygame.Rect(SCREEN_WIDTH / 2 - 50, 100, 100, 50)
quit_button_rect = pygame.Rect(SCREEN_WIDTH / 2 - 50, 220, 100, 50)
restart_button_rect = start_button_rect
game_over_quit_button = pygame.Rect(SCREEN_WIDTH / 2 - 50, 175, 100, 50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the mouse click is within the start button area
            if game_state == "start_menu" and start_button_rect.collidepoint(event.pos):
                game_state = "game"  # Transition to the game state
            elif game_state == "start_menu" and quit_button_rect.collidepoint(event.pos):
                quit()
            if game_state == "game_over" and restart_button_rect.collidepoint(event.pos):
                game_state = "game"
            elif game_state == "game_over" and game_over_quit_button.collidepoint(event.pos):
                quit()
            
    pos = pygame.mouse.get_pos()

    if game_state == "start_menu":
        draw_start_menu()
        keys = pygame.key.get_pressed()
    
    if game_state == "game_over":
        final_score += score  # Accumulate the score into final_score
        draw_game_over_screen(final_score)
        score = 0  # Reset the score to 0 for the next game
        speed = 3
        keys = pygame.key.get_pressed()
        
    
    if game_state == "game":
        final_score = 0
        screen.fill("gray")
        font_display = font.render('Score: {}'.format(score), True, "blue")
        screen.blit(font_display, (10, 10))

        # Player
        player = pygame.draw.circle(screen, "darkgreen", player_pos, 20)

        if len(npcs) < 1:
            npc = NPC()
            npcs.append(npc)
            speed += 2

        for npc in npcs:
            npc.draw(screen)

            if moving_right is True:
                npc.right()
            
            if moving_left is True:
                npc.left()

            if npc.x > screen.get_width():
                moving_right = False
                npc.down()
                moving_left = True

            if npc.x < 0:
                moving_right = True
                npc.down()
                moving_left = False
            
            if npc.player_collision(player_pos.x, player_pos.y):
                npcs.remove(npc)
                game_state = "game_over"
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_RIGHT]:
            player_pos.x += 300 * dt
        if keys[pygame.K_SPACE] and not shooting:
            bullet = Bullet(player_pos.x, player_pos.y)
            shooting = True

        if shooting:
            bullet.update()
            bullet.draw(screen)
            if bullet.y < 0:
                shooting = False

            for npc in npcs:
                if npc.bullet_collision(bullet.x, bullet.y):
                    print("hit")
                    score += 1
                    npcs.remove(npc)
                    break

        pygame.display.flip()
        dt = clock.tick(60) / 1000
