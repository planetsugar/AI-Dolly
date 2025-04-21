import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
DOLLY_SPEED = 5
DANCE_TIME = 30  # seconds

# Colors
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dolly Dance')

# Load Dolly sprite
# Assuming you have a dolly.png image in the same directory
# dolly_image = pygame.image.load('dolly.png')
# For now, we'll use a simple rectangle to represent Dolly
DOLLY_WIDTH, DOLLY_HEIGHT = 50, 50

# Increase size by 30%
DOLLY_WIDTH = int(DOLLY_WIDTH * 1.3)
DOLLY_HEIGHT = int(DOLLY_HEIGHT * 1.3)

# Update dolly_rect to reflect new size
# Recalculate the position to keep Dolly centered vertically
# dolly_rect = pygame.Rect(0, SCREEN_HEIGHT // 2 - DOLLY_HEIGHT // 2, DOLLY_WIDTH, DOLLY_HEIGHT)
dolly_rect = pygame.Rect(0, SCREEN_HEIGHT // 2 - DOLLY_HEIGHT // 2, DOLLY_WIDTH, DOLLY_HEIGHT)

# Adjust head and body positions
head_radius = 15 * 1.3
body_width = 30 * 1.3
body_height = 40 * 1.3
arm_length = 30 * 1.3  # Extend arm length more
leg_length = 20 * 1.3  # Extend leg length more

# Clock to control the frame rate
clock = pygame.time.Clock()

# Variable to track split time
did_splits = False
split_start_time = None

# Set up font
font = pygame.font.SysFont(None, 36)

# Main loop
running = True
start_dance_time = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Start Dolly's movement and hide the message
                if start_dance_time is None:
                    start_dance_time = time.time()
                else:
                    # Fireworks effect
                    for _ in range(50):
                        x = random.randint(dolly_rect.x, dolly_rect.x + DOLLY_WIDTH)
                        y = random.randint(dolly_rect.y, dolly_rect.y + DOLLY_HEIGHT)
                        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        pygame.draw.circle(screen, color, (x, y), random.randint(2, 5))
                    pygame.display.flip()
                    pygame.time.delay(1000)  # Delay to show fireworks
                    running = False
            elif event.key == pygame.K_LEFT:
                dolly_rect.x -= DOLLY_SPEED
            elif event.key == pygame.K_RIGHT:
                dolly_rect.x += DOLLY_SPEED
            elif event.key == pygame.K_UP:
                dolly_rect.y -= DOLLY_SPEED
            elif event.key == pygame.K_DOWN:
                dolly_rect.y += DOLLY_SPEED

    # Fill the background
    screen.fill(WHITE)

    # Render text only if the dance hasn't started
    if start_dance_time is None:
        text = font.render('Press space to make the dolly dance', True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 10))

    # Move Dolly to the center only after space is pressed
    if start_dance_time is not None:
        if dolly_rect.x < SCREEN_WIDTH // 2 - DOLLY_WIDTH // 2:
            dolly_rect.x += DOLLY_SPEED
        else:
            # Start dancing
            if time.time() - start_dance_time < DANCE_TIME:
                # Dolly is dancing, continue moving arms and legs
                floss_phase = (time.time() * 5) % 4
                if floss_phase < 2:
                    # Arms move in opposite directions
                    left_arm_offset = arm_length
                    right_arm_offset = -arm_length
                else:
                    left_arm_offset = -arm_length
                    right_arm_offset = arm_length
            else:
                # Dolly walks off to the right
                dolly_rect.x += DOLLY_SPEED

    # Initialize arm offsets
    left_arm_offset = 0
    right_arm_offset = 0

    # Initialize leg offsets
    left_leg_offset = 0
    right_leg_offset = 0

    # Calculate arm and leg positions for animation
    arm_offset = 5 * (1 if (dolly_rect.x // 10) % 2 == 0 else -1)  # Simple back and forth
    leg_offset = 5 * (1 if (dolly_rect.x // 10) % 2 == 0 else -1)

    # Adjust arm positions for floss dance
    if start_dance_time is not None and time.time() - start_dance_time < DANCE_TIME:
        floss_phase = (time.time() * 5) % 4
        if floss_phase < 2:
            left_arm_offset = arm_length
            right_arm_offset = -arm_length
        else:
            left_arm_offset = -arm_length
            right_arm_offset = arm_length

        # Randomly do the splits
        if random.random() < 0.05 and not did_splits:  # 5% chance each frame
            left_leg_offset = -30  # Move left leg outward
            right_leg_offset = 30  # Move right leg outward
            dolly_rect.y = SCREEN_HEIGHT // 2 - DOLLY_HEIGHT // 2 + 20  # Lower body to touch the ground
            did_splits = True
            split_start_time = time.time()
        elif did_splits:
            if time.time() - split_start_time >= 4:  # 4 second delay
                did_splits = False
            left_leg_offset = -30  # Keep legs in split position
            right_leg_offset = 30
        else:
            left_leg_offset = 5 * (1 if (dolly_rect.x // 10) % 2 == 0 else -1)
            right_leg_offset = -left_leg_offset
            dolly_rect.y = SCREEN_HEIGHT // 2 - DOLLY_HEIGHT // 2  # Reset body position

    # Draw Dolly's long brown hair
    pygame.draw.rect(screen, (139, 69, 19), (dolly_rect.x + int(5 * 1.3), dolly_rect.y - int(10 * 1.3), int(40 * 1.3), int(50 * 1.3)))  # Brown hair

    # Draw Dolly's round face
    pygame.draw.circle(screen, (255, 224, 189), (dolly_rect.x + DOLLY_WIDTH // 2, dolly_rect.y + int(10 * 1.3)), int(head_radius))  # Skin color

    # Draw Dolly's facial features
    # Eyes
    pygame.draw.circle(screen, (0, 0, 0), (dolly_rect.x + DOLLY_WIDTH // 2 - 10, dolly_rect.y + int(10 * 1.3) - 5), 3)  # Left eye
    pygame.draw.circle(screen, (0, 0, 0), (dolly_rect.x + DOLLY_WIDTH // 2 + 10, dolly_rect.y + int(10 * 1.3) - 5), 3)  # Right eye
    # Nose
    pygame.draw.line(screen, (0, 0, 0), (dolly_rect.x + DOLLY_WIDTH // 2, dolly_rect.y + int(10 * 1.3)), (dolly_rect.x + DOLLY_WIDTH // 2, dolly_rect.y + int(10 * 1.3) + 5), 1)
    # Mouth
    pygame.draw.arc(screen, (0, 0, 0), (dolly_rect.x + DOLLY_WIDTH // 2 - 10, dolly_rect.y + int(10 * 1.3) + 5, 20, 10), 3.14, 0, 1)

    # Draw Dolly's body and limbs
    # Body (Pink tank top)
    pygame.draw.rect(screen, (255, 192, 203), (dolly_rect.x + int(10 * 1.3), dolly_rect.y + int(25 * 1.3), int(body_width), int(body_height)))  # Pink color
    # Left arm
    pygame.draw.line(screen, (0, 0, 0), (dolly_rect.x + int(10 * 1.3), dolly_rect.y + int(35 * 1.3)), (dolly_rect.x + int(10 * 1.3) + int(left_arm_offset), dolly_rect.y + int(35 * 1.3) + int(arm_offset)), 7)
    # Right arm
    pygame.draw.line(screen, (0, 0, 0), (dolly_rect.x + int(40 * 1.3), dolly_rect.y + int(35 * 1.3)), (dolly_rect.x + int(40 * 1.3) + int(right_arm_offset), dolly_rect.y + int(35 * 1.3) - int(arm_offset)), 7)
    # Left leg
    pygame.draw.line(screen, (0, 0, 0), (dolly_rect.x + int(20 * 1.3), dolly_rect.y + int(65 * 1.3)), (dolly_rect.x + int(20 * 1.3) + int(left_leg_offset), dolly_rect.y + int(65 * 1.3) + int(leg_length)), 7)
    # Right leg
    pygame.draw.line(screen, (0, 0, 0), (dolly_rect.x + int(30 * 1.3), dolly_rect.y + int(65 * 1.3)), (dolly_rect.x + int(30 * 1.3) + int(right_leg_offset), dolly_rect.y + int(65 * 1.3) + int(leg_length)), 7)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

    # Check if Dolly has walked off the screen
    if dolly_rect.x > SCREEN_WIDTH:
        running = False

# Quit Pygame
pygame.quit()
sys.exit() 