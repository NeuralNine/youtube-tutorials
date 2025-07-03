import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")
clock = pygame.time.Clock()

G = 6.67430e-11  # Gravitational constant
SCALE = 6e-11 
ZOOM_SCALE = 1e-9 
DT = 86400

zoomed = False


class Body:
    def __init__(self, x, y, vx, vy, mass, radius, color):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.mass = mass
        self.radius = radius
        self.color = color
        self.trail = []

    def update_position(self, bodies):
        fx = fy = 0
        for other in bodies:
            if other != self:
                dx = other.x - self.x
                dy = other.y - self.y
                r = math.sqrt(dx*dx + dy*dy)
                if r > 0:
                    # Formula: F = G * (m1 * m2) / r^2
                    f = G * self.mass * other.mass / (r*r)
                    fx += f * dx / r
                    fy += f * dy / r
        
        # Formula: a = F / m  (based on F = ma)
        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax * DT
        self.vy += ay * DT
        self.x += self.vx * DT
        self.y += self.vy * DT
        
        current_scale = ZOOM_SCALE if zoomed else SCALE

        self.trail.append((int(self.x * current_scale + WIDTH//2), int(self.y * current_scale + HEIGHT//2)))
        if len(self.trail) > 200:
            self.trail.pop(0)

    def draw(self, screen):
        if len(self.trail) > 1:
            pygame.draw.lines(screen, (50, 50, 50), False, self.trail, 1)
        
        current_scale = ZOOM_SCALE if zoomed else SCALE

        screen_x = int(self.x * current_scale + WIDTH // 2)
        screen_y = int(self.y * current_scale + HEIGHT // 2)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), self.radius)


bodies = [
    Body(0, 0, 0, 0, 1.989e30, 8, (255, 255, 0)),  # Sun  (1.989e30 kg, 8 pixel radius (not used in calculations, just visual))
    Body(5.79e10, 0, 0, 47360, 3.301e23, 2, (169, 169, 169)),  # Mercury
    Body(1.082e11, 0, 0, 35020, 4.867e24, 3, (255, 165, 0)),  # Venus
    Body(1.496e11, 0, 0, 29780, 5.972e24, 4, (0, 100, 255)),  # Earth
    Body(279e11, 0, 0, 24077, 6.39e23, 3, (255, 100, 0)),  # Mars
    Body(7.786e11, 0, 0, 13070, 1.898e27, 6, (200, 150, 100)),  # Jupiter
    Body(1.432e12, 0, 0, 9680, 5.683e26, 5, (250, 200, 100)),  # Saturn
    Body(2.867e12, 0, 0, 6810, 8.681e25, 4, (100, 200, 255)),  # Uranus
    Body(4.515e12, 0, 0, 5430, 1.024e26, 4, (0, 0, 255)),  # Neptune
    Body(5.906e12, 0, 0, 4670, 1.309e22, 2, (150, 100, 50)),  # Pluto
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                zoomed = not zoomed

            for body in bodies:
                body.trail = []
    
    screen.fill((0, 0, 0))
    
    for body in bodies:
        body.update_position(bodies)
        body.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit() 
