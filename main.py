import pygame
import math
import sys

# Pygame initialize
pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cinematic Slow-Draw Blue Spirograph")
clock = pygame.time.Clock()

# Visualizer parameters
NUM_POINTS = 320
RADIUS = 300
MULTIPLIER = 4.0

# Interpolated Slow-Motion Line Drawing Settings
current_line_idx = 0       # Kaunsi line draw ho rahi hai
line_progress = 0.0        # 0.0 (start point) se 1.0 (target point) tak
LINE_GROWTH_SPEED = 0.04   # Line stretch hone ki speed (Slow motion control)
ROTATION_SPEED = 0.003

# Blue Palette
BG_COLOR = (3, 6, 16)
CYAN_BRIGHT = (0, 245, 255)
CYAN_MID = (0, 160, 240)
CYAN_GLOW = (0, 60, 120)
CYAN_CORE = (220, 255, 255)

completed_lines = []
rotation_angle = 0.0
paused = False
all_completed = False

def get_point(idx, total, radius, center, angle_offset=0.0):
    theta = (2 * math.pi / total) * idx + angle_offset
    return (center[0] + radius * math.cos(theta), center[1] + radius * math.sin(theta))

running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                # Reset
                current_line_idx = 0
                line_progress = 0.0
                completed_lines.clear()
                all_completed = False
                rotation_angle = 0.0
            elif event.key == pygame.K_UP:
                LINE_GROWTH_SPEED = min(0.2, LINE_GROWTH_SPEED + 0.01)
            elif event.key == pygame.K_DOWN:
                LINE_GROWTH_SPEED = max(0.005, LINE_GROWTH_SPEED - 0.005)

    center = (WIDTH // 2, HEIGHT // 2)

    # 2. Logic Update
    if not paused:
        if not all_completed:
            line_progress += LINE_GROWTH_SPEED
            if line_progress >= 1.0:
                # Current line complete hui
                p1_idx = current_line_idx
                p2_idx = int(p1_idx * MULTIPLIER) % NUM_POINTS
                completed_lines.append((p1_idx, p2_idx))

                current_line_idx += 1
                line_progress = 0.0

                if current_line_idx >= NUM_POINTS:
                    all_completed = True
        else:
            # Sab lines draw hone ke baad smooth gentle rotation
            rotation_angle += ROTATION_SPEED

    # 3. Screen Drawing
    screen.fill(BG_COLOR)

    # Draw all already-completed lines
    for p1_i, p2_i in completed_lines:
        pt1 = get_point(p1_i, NUM_POINTS, RADIUS, center, rotation_angle)
        pt2 = get_point(p2_i, NUM_POINTS, RADIUS, center, rotation_angle)

        # Multi-layer neon glow
        pygame.draw.line(screen, CYAN_GLOW, pt1, pt2, 3)
        pygame.draw.line(screen, CYAN_MID, pt1, pt2, 2)
        pygame.draw.line(screen, CYAN_BRIGHT, pt1, pt2, 1)

    # Draw CURRENT stretching line in slow motion
    if not all_completed and current_line_idx < NUM_POINTS:
        p1_idx = current_line_idx
        p2_idx = int(p1_idx * MULTIPLIER) % NUM_POINTS

        start_pt = get_point(p1_idx, NUM_POINTS, RADIUS, center, rotation_angle)
        target_pt = get_point(p2_idx, NUM_POINTS, RADIUS, center, rotation_angle)

        # Linear interpolation (LERP) for smooth stretching tip
        curr_x = start_pt[0] + (target_pt[0] - start_pt[0]) * line_progress
        curr_y = start_pt[1] + (target_pt[1] - start_pt[1]) * line_progress
        cur_tip = (curr_x, curr_y)

        # Active glowing line
        pygame.draw.line(screen, CYAN_GLOW, start_pt, cur_tip, 4)
        pygame.draw.line(screen, CYAN_BRIGHT, start_pt, cur_tip, 2)

        # Glowing pen tip particle
        pygame.draw.circle(screen, CYAN_BRIGHT, (int(curr_x), int(curr_y)), 7)
        pygame.draw.circle(screen, CYAN_CORE, (int(curr_x), int(curr_y)), 4)

    # Ambient glowing center core
    pulse = int(4 + 2 * math.sin(pygame.time.get_ticks() * 0.004))
    pygame.draw.circle(screen, CYAN_MID, center, pulse + 3, 1)
    pygame.draw.circle(screen, CYAN_CORE, center, 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
