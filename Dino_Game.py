import pygame
import random

# 초기화
pygame.init()

# 화면 크기
WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("공룡 게임")

# 색상
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 공룡 클래스
class Dinosaur:
    def __init__(self):
        self.rect = pygame.Rect(50, HEIGHT - 60, 40, 40)
        self.jump = False
        self.jump_count = 10

    def draw(self):
        pygame.draw.circle(screen, GREEN, (self.rect.x + 20, self.rect.y + 20), 20)

    def update(self):
        if self.jump:
            if self.jump_count >= -10:
                neg = 1 if self.jump_count >= 0 else -1
                self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.jump = False
                self.jump_count = 10
        else:
            if self.rect.y < HEIGHT - 60:
                self.rect.y += 5
            else:
                self.rect.y = HEIGHT - 60

# 장애물 클래스
class Obstacle:
    def __init__(self):
        self.width = 20
        self.height = random.randint(40, 100)
        self.rect = pygame.Rect(WIDTH, HEIGHT -self.height, self.width, self.height)

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

    def update(self, speed):
        self.rect.x -= speed

# 게임 루프
def main():
    clock = pygame.time.Clock()
    dinosaur = Dinosaur()
    obstacles = []
    score = 0
    spawn_timer = 0
    spawn_interval = random.randint(20, 60)  # 랜덤한 생성 간격
    speed = 10

    # 기본 폰트 로드
    font = pygame.font.SysFont("Arial", 36)

    running = True
    while running:
        clock.tick(30)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dinosaur.jump:
                    dinosaur.jump = True

        # 장애물 생성
        spawn_timer += 1
        if spawn_timer > spawn_interval:
            obstacles.append(Obstacle())
            spawn_timer = 0
            spawn_interval = random.randint(20, 100)  # 다음 장애물의 랜덤한 생성 간격

        # 장애물 업데이트 및 그리기
        for obstacle in obstacles[:]:
            obstacle.update(speed)
            obstacle.draw()
            if obstacle.rect.x < 0:
                obstacles.remove(obstacle)
            if dinosaur.rect.colliderect(obstacle.rect):
                print("게임 오버! 점수:", score)
                running = False

        # 이동 거리 비례 점수 증가
        score += 1

        # 점수판 그리기
        score_text = font.render(f"SCORE: {score}", True, BLUE)
        screen.blit(score_text, (10, 10))

        # 속도 증가 로직
        if score % 100 == 0 and score > 0:
            speed += 1

        dinosaur.update()
        dinosaur.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
