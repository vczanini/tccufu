import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Clickable Circles")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
LIGHTBLUE = (173, 216, 230)

# Function to draw a circle
def draw_circle(surface, color, center, radius):
    pygame.draw.circle(surface, color, center, radius)

# Function to check if a point is inside a circle
def point_inside_circle(point, center, radius):
    return math.sqrt((point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2) <= radius

# Function to change color of circle and background when clicking
def change_color(pos):
    global current_circle

    # Check if click is on the blue circle
    if point_inside_circle(pos, (central_x, central_y), central_radius):
        # Turn all surrounding circles red
        for _, circle in circles.items():
            circle["color"] = RED
        # Change the background color to lightblue
        screen.fill(LIGHTBLUE)
        # Set the current circle to None
        current_circle = None
        return

    # Check if click is on any of the surrounding circles
    for key, circle in circles.items():
        if point_inside_circle(pos, circle["center"], circle_radius):
            # If a circle is already selected, change it back to red
            if current_circle is not None:
                circles[current_circle]["color"] = RED
            # Change the clicked circle to purple
            circle["color"] = PURPLE
            # Update the current_circle variable
            current_circle = key
            return

# Draw the central circle and surrounding circles
central_x, central_y = screen_width // 2, screen_height // 2
central_radius = 50
circle_radius = 20
circles = {}
angle_increment = 360 / 10  # Split the circle into 10 equal parts
for i in range(10):
    angle = math.radians(i * angle_increment)
    x = central_x + 400 * math.cos(angle)
    y = central_y + 400 * math.sin(angle)
    circles[i] = {"center": (int(x), int(y)), "color": RED}

# Main loop
running = True
current_circle = None
while running:
    screen.fill(WHITE)
    # Draw the central circle
    draw_circle(screen, BLUE, (central_x, central_y), central_radius)
    # Draw surrounding circles
    for key, circle in circles.items():
        draw_circle(screen, circle["color"], circle["center"], circle_radius)

    # Event handling
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
       elif event.type == pygame.MOUSEBUTTONDOWN:
           if event.button == 1:  # Left mouse button
               pos = pygame.mouse.get_pos()
               change_color(pos)
       elif event.type == pygame.KEYDOWN:
           if event.key == pygame.K_c:
               pygame.quit()
               sys.exit()

    pygame.display.flip()
    clock.tick(60)

# Quit Pygame 
pygame.quit()
