import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (50, 50, 50)
CAR_COLOR = (200, 0, 0)

# Car properties
MAX_SPEED = 5
ACCELERATION = 0.1
FRICTION = 0.05
TURN_SPEED = 3

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Car Simulator")

# Load Car Image (optional)
car_surface = pygame.Surface((50, 30), pygame.SRCALPHA)
pygame.draw.polygon(
    car_surface, CAR_COLOR, [(0, 10), (40, 0), (50, 15), (40, 30), (0, 20)]
)


class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0

    def update(self, keys):
        if keys[pygame.K_UP]:  # Accelerate
            self.speed += ACCELERATION
        elif keys[pygame.K_DOWN]:  # Brake/Reverse
            self.speed -= ACCELERATION

        # Apply friction
        if self.speed > 0:
            self.speed -= FRICTION
        elif self.speed < 0:
            self.speed += FRICTION

        # Limit speed
        self.speed = max(-MAX_SPEED, min(self.speed, MAX_SPEED))

        # Turn left/right
        if keys[pygame.K_LEFT]:
            self.angle += TURN_SPEED * (-1 if self.speed < 0 else 1)
        if keys[pygame.K_RIGHT]:
            self.angle -= TURN_SPEED * (-1 if self.speed < 0 else 1)

        # Update position
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed

    def draw(self):
        rotated_car = pygame.transform.rotate(car_surface, self.angle)
        rect = rotated_car.get_rect(center=(self.x, self.y))
        screen.blit(rotated_car, rect.topleft)


# Initialize car
car = Car(WIDTH // 2, HEIGHT // 2)

# Game Loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BG_COLOR)

    keys = pygame.key.get_pressed()
    car.update(keys)
    car.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
