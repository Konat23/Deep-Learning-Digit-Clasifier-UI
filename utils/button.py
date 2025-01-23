import pygame
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class Button:
    def __init__(self, x, y, width, height, text, action=None, action_args=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.hovered = False
        self.text = text
        self.action = action
        self.action_args = action_args

    def draw(self, screen):
        # Cambia el color del botón si el mouse está sobre él
        if self.hovered:
            self.color = WHITE
        else:
            self.color = GRAY

        # Dibuja el botón
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Dibuja el texto en el centro del botón
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event, *action_args):
        if event.type == pygame.MOUSEMOTION:
            # Comprueba si el mouse está sobre el botón
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            # Llama a la función del botón si se hace clic en él
            self.action_args = action_args
            if self.action:
                    if self.action_args:
                        self.action(*self.action_args)
                    else:
                        self.action()