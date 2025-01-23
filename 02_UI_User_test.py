"""
@author: Konat
Codigo principal MNIXEL 
"""
import numpy as np


# RGB Colores
Black = (0, 0, 0)
White =(255, 255, 255)
Green = (0, 255, 0)
Red = (255, 0, 0)
Blue = (0, 0, 255) 
Gray = (127, 127, 127)

# Tamaños
scale = 1 # para tener mas pixeles poner un numero mayor que 1
filas = int(28*scale)
columnas = int(28*scale)
border = 2

X_new = []
y_new = []

class Salida():
    def __init__(self) -> None:
        self.X = np.empty(())
        self.y = np.empty(())
        
salida = Salida()


board_size =(448,448) #tamaño de de la zona donde se dibujara
centerboard = (board_size[0]/2,board_size[1]/2)
pixel_size = (board_size[0]/columnas,board_size[1]/filas)
size = (1000, 700) # Tamaño de la ventana
centersize = (size[0]/2,size[1]/2)

# Pygame
import pygame, sys
from utils.slider import Slider
from utils.button import Button
from utils.blackboard import Blackboard
from utils.image_p import *
pygame.init()
screen = pygame.display.set_mode(size) #Crear ventana


clock = pygame.time.Clock()

class Text():
    def __init__(self, font_size, text, color, pos):
        self.font = pygame.font.Font(None, font_size)
        self.text = text
        self.color = color
        self.pos = pos

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.color)
        surface.blit(text_surface, self.pos)







class Pixel():
    def __init__(self, loc) -> None:

        self.left = loc[0]
        self.top = loc[1]
        self.width = pixel_size[0]
        self.height = pixel_size[1]
        self.color = 'black'
        
        self.insiderect = pygame.Rect(self.left , self.top , self.width, self.height)
        #self.rect = pygame.Rect(self.left , self.top , self.width, self.height)
        #self.insiderect = pygame.Rect(loc[0]+border/2, loc[1]+border/2, pixel_size[0]-border, pixel_size[1]-border)

    def draw(self,surface, colorborder):
        
        #pygame.draw.rect(surface, colorborder, self.rect)
        pygame.draw.rect(surface, self.color, self.insiderect)

    def paint(self, element):
        """
        Esta funcion se encarga de colorear
        """ 
        color = int (element)
        self.color = (color,color,color) # nivel de gris

class Grid():
    def __init__(self,size,offset) -> None:
        self.offset = offset
        self.surfaceOne = pygame.Surface(size)
        self.array = [[Pixel((j*pixel_size[0],i*pixel_size[1])) for i in range(columnas)] for j in range(filas)]
        self.margin = 10 # pixeles que se consideran cerca 
        self.ishow = False
        self.matriz = np.zeros((int(size[0]),int(size[1])), dtype=np.uint8)
    
    def draw(self):
        for i,raw in enumerate(self.array):
            for j,pixel in enumerate(raw):
                pixel.draw(self.surfaceOne, Gray)
                if clic_izquierdo:
                    pixel.paint(self.matriz[i,j])
        screen.blit(self.surfaceOne, self.offset)
    def set_margin(self,slider):
        self.margin = slider.get_value()*20 # Va de 0 a 20 pixeles
    
    def update(self, slider):
        self.draw()
        self.set_margin(slider)
    def set_show(self):
        self.ishow = not self.ishow
    




def preview_function(board, matriz):
    
    board.matriz = greduce(matriz,4)
    board.set_show()



from tensorflow.keras.models import load_model
loaded_model = load_model("model/modelo.h5")

def predict_function(matriz,Text_message):
    matriz = greduce(matriz,4) # reducir tamaño
    matriz = np.transpose(matriz,(1,0)) # invertir dimensiones
    matriz = shift_to_center(matriz)
    matriz = np.array(matriz)  # Asegúrate de que sea un array de NumPy
    matriz = np.expand_dims(matriz, axis=-1)  # Agrega una dimensión en el eje de canales (final)
    matriz = np.expand_dims(matriz, axis=0)  # Agrega una dimensión en el eje de lote (primero)
    Y = loaded_model.predict(matriz)[0]
    print("predicción:",Y)    
    Y = np.argmax(Y)
    Text_message.text = f"El numero es: {Y}"



def events():
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        slider.handle_event(event)
        previewButton.handle_event(event,board_preview,myboard.matriz)
        limpiarButton.handle_event(event)
        myboard.handle_event(event)
        if event.type == pygame.MOUSEBUTTONUP:
            board_preview.matriz = greduce(myboard.matriz,4)
            board_preview.draw()
        predictButton.handle_event(event,myboard.matriz,text_adivinado)

offset_surface = [10, centersize[1]-centerboard[1]]


myboard = Blackboard(board_size,offset_surface)
board_preview = Grid([board_size[0],board_size[1]],[size[0] - board_size[0], centersize[1]-centerboard[1]])

# Crear botones y slider
slider = Slider(10, 10, 600, 20)
previewButton = Button(size[0]-200-10, size[1]-40, 100, 40, "Preview", preview_function)
limpiarButton = Button(0,size[1]-40,100,40,"Limpiar",myboard.clear)
predictButton = Button(100+10,size[1]-40, 100, 40, "Predict", predict_function)

# Crear texto
text = Text(30, f"Dibuja cualquier numero", White, (10, 100))
text_adivinado = Text(30, f"El numero es", White, (10, 600))

M_test = np.random.randint(0, 256, board_size, dtype=np.uint8)
while True:
    events()
    screen.fill('gray15') #color de fondo y limpia pantalla
        
    #------------ ZONA DE DIBUJO -----------------#
    
    
    mouse = pygame.mouse

    # Verifica si el botón izquierdo del mouse está presionado (clic)
    clic_izquierdo, _, _ = mouse.get_pressed()
    mouse_pos = mouse.get_pos()
    
    

    slider.update(screen)
    previewButton.draw(screen)
    limpiarButton.draw(screen)
    predictButton.draw(screen)

    # Texto
    
    text.draw(screen)
    text_adivinado.draw(screen)
    

    if board_preview.ishow:
        board_preview.update(slider)
    
    myboard.update(screen,slider)
    
    #-----------FIN ZONA DE DIBUJO ---------------#
    #Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)