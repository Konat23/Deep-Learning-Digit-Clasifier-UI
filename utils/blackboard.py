import pygame
import numpy as np

class Blackboard:
    def __init__(self,size,pos):
        self.matriz = np.zeros(size, dtype=np.uint8)
        self.gray_image = pygame.surfarray.make_surface(np.stack((self.matriz,) * 3, axis=-1))
        self.pos = pos
        self.dragging = False
        self.r = 5 # Radio del punter

    def get(self, key):
        return self.matriz

    def set(self, M):
        self.matriz = M

    def update_surface(self):
        pygame.surfarray.blit_array(self.gray_image, np.stack((self.matriz,) * 3, axis=-1))

    def draw(self, screen):
        screen.blit(self.gray_image, self.pos)

    def update(self,screen, slider):
        self.r = int(slider.get_value()*20+5)
        self.paint()
        self.update_surface()
        self.draw(screen)
    
    def paint(self):
        if self.dragging:
            pos = pygame.mouse.get_pos()
            # Restamos la posicion del tablero para que quede en el origen
            x = int(pos[0]-self.pos[0])
            y = int(pos[1]-self.pos[1])

            for i in range(x-self.r, x+self.r):
                for j in range(y-self.r, y+self.r):
                    if i >= 0 and i < self.matriz.shape[0] and j >= 0 and j < self.matriz.shape[1]:
                        if np.sqrt((x-i)**2+(y-j)**2)<self.r:
                            self.matriz[i][j] = 255
            self.update_surface()
    def clear(self):
        self.matriz = np.zeros(self.matriz.shape, dtype=np.uint8)
        self.update_surface()
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (self.gray_image.get_rect().collidepoint(mouse_x-self.pos[0], mouse_y-self.pos[1])):
                self.dragging = True
            
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
    