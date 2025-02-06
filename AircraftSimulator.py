import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (135, 206, 250)
PLANE_COLOR = (255, 255, 255)
CARRIER_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)

# Physics
GRAVITY = 0.05
THRUST = 0.2
DRAG = 0.01
LANDING_SPEED = 1.5

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aircraft Carrier Landing Game")
font = pygame.font.Font(None, 36)

# Load Plane Image (Optional)
plane_surface = pygame.Surface((40, 20), pygame.SRCALPHA)
pygame.draw.polygon(
    plane_surface, PLANE_COLOR, [(0, 10), (30, 0), (40, 10), (30, 20), (0, 10)]
)

# Load Sound Effects
# landing_sound = pygame.mixer.Sound("landing.wav")
# crash_sound = pygame.mixer.Sound("crash.wav")


# Plane Class
class Plane:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 2
        self.vy = 0

    def update(self, keys):
        if keys[pygame.K_UP]:  # Thrust
            self.vy -= THRUST
        if keys[pygame.K_DOWN]:  # Reduce speed
            self.vy += THRUST / 2
        if keys[pygame.K_LEFT]:
            self.angle += 2
        if keys[pygame.K_RIGHT]:
            self.angle -= 2

        # Apply gravity and drag
        self.vy += GRAVITY
        self.vy -= self.vy * DRAG

        # Update position
        self.y += self.vy
        self.x += math.cos(math.radians(self.angle)) * self.speed

    def draw(self):
        rotated_plane = pygame.transform.rotate(plane_surface, self.angle)
        rect = rotated_plane.get_rect(center=(self.x, self.y))
        screen.blit(rotated_plane, rect.topleft)


# Carrier Class
class Carrier:
    def __init__(self):
        self.x = WIDTH // 2 - 100
        self.y = HEIGHT - 50
        self.width = 200
        self.height = 20

    def draw(self):
        pygame.draw.rect(
            screen, CARRIER_COLOR, (self.x, self.y, self.width, self.height)
        )


# Initialize Objects
plane = Plane(WIDTH // 4, HEIGHT // 3)
carrier = Carrier()
landing_message = ""

# Game Loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BG_COLOR)

    keys = pygame.key.get_pressed()
    plane.update(keys)

    # Check for landing
    if (
        carrier.x < plane.x < carrier.x + carrier.width
        and carrier.y - 5 < plane.y < carrier.y + 5
    ):
        if abs(plane.vy) <= LANDING_SPEED:
            landing_message = "Successful Landing!"
            landing_sound.play()
        else:
            landing_message = "Crash Landing!"
            crash_sound.play()
        running = False

    # Draw Objects
    carrier.draw()
    plane.draw()

    if landing_message:
        text_surface = font.render(landing_message, True, TEXT_COLOR)
        screen.blit(
            text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2)
        )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
