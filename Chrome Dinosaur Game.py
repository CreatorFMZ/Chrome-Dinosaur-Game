import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
GROUND_HEIGHT = 100
GRAVITY = 1
JUMP_STRENGTH = 18
GAME_SPEED = 8
OBSTACLE_FREQUENCY = 0.02

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (83, 83, 83)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrome Dinosaur Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 20)

class Dinosaur:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - 40
        self.width = 40
        self.height = 40
        self.vel_y = 0
        self.is_jumping = False
        self.is_ducking = False
        
    def jump(self):
        if not self.is_jumping:
            self.vel_y = -JUMP_STRENGTH
            self.is_jumping = True
    
    def duck(self, is_ducking):
        self.is_ducking = is_ducking
        if self.is_ducking:
            self.height = 20
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - 20
        else:
            self.height = 40
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - 40
    
    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        if self.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
            self.vel_y = 0
            self.is_jumping = False
    
    def draw(self):
        pygame.draw.rect(screen, GRAY, (self.x, self.y, self.width, self.height))
        
        eye_x = self.x + self.width - 10
        eye_y = self.y + 10
        pygame.draw.rect(screen, WHITE, (eye_x, eye_y, 5, 5))
        
        if not self.is_ducking:
            leg_y = self.y + self.height - 5
            pygame.draw.rect(screen, GRAY, (self.x + 5, leg_y, 8, 10))
            pygame.draw.rect(screen, GRAY, (self.x + self.width - 13, leg_y, 8, 10))

class Obstacle:
    def __init__(self, x, obstacle_type):
        self.x = x
        self.obstacle_type = obstacle_type  
        
        if obstacle_type == 0:
            self.width = 20
            self.height = 40
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        elif obstacle_type == 1:
            self.width = 30
            self.height = 50
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        else:  # 鸟
            self.width = 40
            self.height = 30
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - 60 - random.randint(0, 30)
    
    def update(self, speed):
        self.x -= speed
    
    def draw(self):
        if self.obstacle_type == 0 or self.obstacle_type == 1:
            pygame.draw.rect(screen, GRAY, (self.x, self.y, self.width, self.height))
            if self.obstacle_type == 0:
                pygame.draw.rect(screen, GRAY, (self.x - 5, self.y + 10, 5, 5))
                pygame.draw.rect(screen, GRAY, (self.x + self.width, self.y + 10, 5, 5))
            else:
                pygame.draw.rect(screen, GRAY, (self.x - 5, self.y + 15, 5, 8))
                pygame.draw.rect(screen, GRAY, (self.x + self.width, self.y + 15, 5, 8))
        else:
            pygame.draw.rect(screen, GRAY, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, GRAY, (self.x + 10, self.y - 5, 15, 5))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = random.randint(20, SCREEN_HEIGHT - GROUND_HEIGHT - 50)
        self.width = random.randint(40, 80)
        self.height = 20
        self.speed = random.uniform(0.5, 1.5)
    
    def update(self):
        self.x -= self.speed
    
    def draw(self):
        pygame.draw.rect(screen, GRAY, (self.x, self.y, self.width, self.height))

def check_collision(dino, obstacle):
    dino_rect = pygame.Rect(dino.x, dino.y, dino.width, dino.height)
    obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
    return dino_rect.colliderect(obstacle_rect)

def draw_ground():
    pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
    
    for i in range(0, SCREEN_WIDTH, 30):
        pygame.draw.rect(screen, WHITE, (i, SCREEN_HEIGHT - GROUND_HEIGHT, 15, 5))

def game_over_screen(score):
    screen.fill(WHITE)
    
    game_over_text = font.render("GAME OVER", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    restart_text = font.render("Press SPACE to restart", True, BLACK)
    
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    dino = Dinosaur()
    obstacles = []
    clouds = []
    score = 0
    game_speed = GAME_SPEED
    game_active = True
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if game_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        dino.jump()
                    if event.key == pygame.K_DOWN:
                        dino.duck(True)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        dino.duck(False)
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    dino = Dinosaur()
                    obstacles = []
                    clouds = []
                    score = 0
                    game_speed = GAME_SPEED
                    game_active = True
        
        if game_active:
            dino.update()
            
            if random.random() < OBSTACLE_FREQUENCY and (not obstacles or obstacles[-1].x < SCREEN_WIDTH - 300):
                obstacle_type = random.randint(0, 2)
                obstacles.append(Obstacle(SCREEN_WIDTH, obstacle_type))
            
            if random.random() < 0.01 and (not clouds or clouds[-1].x < SCREEN_WIDTH - 200):
                clouds.append(Cloud())
            
            for obstacle in obstacles[:]:
                obstacle.update(game_speed)
                if obstacle.x + obstacle.width < 0:
                    obstacles.remove(obstacle)
            
            for cloud in clouds[:]:
                cloud.update()
                if cloud.x + cloud.width < 0:
                    clouds.remove(cloud)
            
            for obstacle in obstacles:
                if check_collision(dino, obstacle):
                    game_active = False
                    game_over_screen(score)
                    break
            
            score += 1
            if score % 100 == 0:
                game_speed += 0.5
            
            screen.fill(WHITE)
            
            for cloud in clouds:
                cloud.draw()
            
            draw_ground()
            
            dino.draw()
            
            for obstacle in obstacles:
                obstacle.draw()
            
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (SCREEN_WIDTH - 150, 20))
            
            speed_text = font.render(f"Speed: {game_speed:.1f}", True, BLACK)
            screen.blit(speed_text, (SCREEN_WIDTH - 150, 50))
            
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    main()