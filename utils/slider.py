import pygame
import sys

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Slider:
    def __init__(self, x, y, width, height):
        self.value = 0.5
        self.rect = pygame.Rect(x, y, width, height)

        # Iniciar x segun value
        initial_x = self.value*(self.rect.width - 20)+self.rect.left
        self.handle = pygame.Rect(initial_x, y, 20, height)
        self.dragging = False
        
        

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, RED, self.handle)

    def update(self,screen):
        if self.dragging:
            mouse_x, _ = pygame.mouse.get_pos()
            self.handle.x = max(self.rect.left, min(self.rect.right - self.handle.width, mouse_x))
            self.value = (self.handle.x - self.rect.left) / (self.rect.width - self.handle.width)
        self.draw(screen)
    def get_value(self):
        return self.value
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
                if self.handle.collidepoint(event.pos):
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

def main():
    pygame.init()

    # Configuración de pantalla
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Barra Deslizable')

    slider = Slider(100, 300, 600, 20)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider.handle.collidepoint(event.pos):
                    slider.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                slider.dragging = False

        slider.update()

        # Dibuja todo
        screen.fill(WHITE)
        slider.draw(screen)
        pygame.display.flip()

        clock.tick(60)

if __name__ == '__main__':
    main()
