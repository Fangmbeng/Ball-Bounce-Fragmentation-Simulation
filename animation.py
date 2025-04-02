import pygame
import random
import math

# Window size
WIDTH, HEIGHT = 500, 500

# Ball properties
RADIUS = 20
DAUGHTER_RADIUS = 15
GRAVITY = 0.2
REBOUND_FACTOR = 0.9
INITIAL_VY = 5  # Increased for a more dynamic fall

class Ball:
    def __init__(self, x, y, vx, vy, radius, color, is_daughter=False):
        """
        Initialize a ball object.
        :param x: Initial x-coordinate
        :param y: Initial y-coordinate
        :param vx: Initial horizontal velocity
        :param vy: Initial vertical velocity
        :param radius: Radius of the ball
        :param color: Color of the ball
        :param is_daughter: Boolean indicating if the ball is a daughter ball
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.is_daughter = is_daughter
        self.created_daughter = False  # Only parent balls can create daughter balls

    def update(self):
        """
        Update ball position based on velocity and gravity.
        """
        self.x += self.vx
        self.y += self.vy
        self.vy += GRAVITY  # Apply gravity

        # Bounce off the ground
        if self.y + self.radius > HEIGHT:
            self.vy = -self.vy * REBOUND_FACTOR  # Reduce velocity after bounce
            self.y = HEIGHT - self.radius  # Keep ball above ground
            self.created_daughter = False  # Reset only for the parent ball

        # Bounce off walls (left and right)
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx = -self.vx

    def draw(self, screen):
        """
        Draw the ball on the screen.
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def get_random_color():
    """
    Generate a bright, visually distinct random color.
    """
    return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Start the main ball at y=400 with a realistic initial downward velocity
    balls = [Ball(250, 400, 0, INITIAL_VY, RADIUS, (255, 0, 0))]

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Clear the screen

        for ball in balls:
            ball.update()
            ball.draw(screen)

            # Only the main ball (not daughter balls) can generate new balls
            if (
                ball.vy < 0  # Ball is moving upward
                and ball.y + ball.radius > HEIGHT - 10  # Near ground
                and ball.radius == RADIUS  # Only the main ball
                and not ball.created_daughter  # Only create once per bounce
            ):
                # Generate random angle for daughter ball movement
                angle = random.uniform(0, 2 * math.pi)
                vx = math.cos(angle) * 5
                vy = -abs(math.sin(angle) * 5)  # Ensure it's moving upward

                # Create a daughter ball with a new color
                balls.append(Ball(ball.x, ball.y, vx, vy, DAUGHTER_RADIUS, get_random_color(), is_daughter=True))
                ball.created_daughter = True  # Mark that daughter has been created

        # Update color of daughter balls when they bounce
        for ball in balls:
            if ball.is_daughter and ball.vy < 0 and ball.y + ball.radius > HEIGHT - 10:
                ball.color = get_random_color()  # Assign a highly distinct color

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Limit FPS

    pygame.quit()

if __name__ == "__main__":
    main()
