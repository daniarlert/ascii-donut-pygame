import os
from math import cos, sin
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

os.environ["SDL_VIDEO_CENTERED"] = "1"
RES = WIDTH, HEIGHT = 640, 1080
FPS = 30

pixel_width = 14
pixel_height = 14

x_pixel = 0
y_pixel = 0

screen_width = WIDTH // pixel_width
screen_height = HEIGHT // pixel_height
screen_size = screen_width * screen_height

A, B = 0, 0

theta_spacing = 10
phi_spacing = 3

chars = ".,-~:;=!*#$@"

R1 = 10
R2 = 20
K2 = 200
K1 = screen_height * K2 * 3 / (8 * (R1 + R2))

pygame.init()

pygame.display.set_caption("ASCII Donut")

screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Fira Code", 20, bold=True)

def print_char(char: str, x: int, y: int):
    text = font.render(char, True, WHITE)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


k = 0
i = 0
record = False
while True:
    clock.tick(FPS)
    screen.fill(BLACK)

    output: list[str] = [" "] * screen_size
    zbuffer: list[int | float] = [0] * screen_size

    for theta in range(0, 628, theta_spacing):
        for phi in range(0, 628, phi_spacing):
            cosA = cos(A)
            sinA = sin(A)
            cosB = cos(B)
            sinB = sin(B)

            costheta = cos(theta)
            sintheta = sin(theta)
            cosphi = cos(phi)
            sinphi = sin(phi)

            # 3D (x, y, z) coordinates before rotation
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # 3D (x, y, z) coordinates after rotation
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z  # one over z

            # x, y projection
            xp = int(screen_width / 2 + K1 * ooz * x)
            yp = int(screen_height / 2 - K1 * ooz * y)

            position = xp + screen_width * yp

            # luminance
            L = (
                cosphi * costheta * sinB
                - cosA * costheta * sinphi
                - sinA * sintheta
                + cosB * (cosA * sintheta - costheta * sinA * sinphi)
            )

            if ooz > zbuffer[position]:
                # we only draw if the pixel is closer to the viewer
                zbuffer[position] = ooz
                luminance_index = int(L * 8)
                output[position] = chars[luminance_index if luminance_index > 0 else 0]

    for i in range(screen_height):
        y_pixel += pixel_height

        for j in range(screen_width):
            x_pixel += pixel_width
            print_char(output[k], x_pixel, y_pixel)
            k += 1

        x_pixel = 0

    y_pixel = 0
    k = 0

    A += 0.15
    B += 0.035

    i += 1
    if record:
        pygame.image.save(screen, f"frames/frame_{i}.png")

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_q:
                pygame.quit()
                exit()
            elif event.key == pygame.K_r:
                record = not record
