import numpy as np
import scipy.signal as ssig

def greduce(g0,n):
    # %Reduce color image
    # %Sintax:
    # %	g1 = greduce(g0, a)
    # % g0 -> H * W * 3
    # % n -> numero de veces a divir en 2
    # %Edit here %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Flitro gaussiano
    a = 0.4
    k = np.array([[0.25 - 0.5*a],
                   [0.25],
                   [a],
                   [0.25],
                   [0.25 - 0.5*a]])
    H = np.matmul(k,np.transpose(k))
    B = np.zeros_like(g0)
    B = ssig.convolve2d(g0,H,'same')

    
    # Reduccion
    H, W = g0.shape
    if H%2 == 0: # si es par
        M = int(H/2)
    else:
        M = int((H+1)/2)
    if W%2 == 0: # si es par
        N = int(W/2)
    else:
        N = int((W+1)/2)
    g1 = np.zeros((M,N))
    
    for j in range(M): # M filas N columnas
        for i in range(N): # fila j columna i 
            g1[j,i]=B[2*j, 2*i]
    n = n-1
    # repetimos la operacion si hace falta
    #print(n)
    if n>0:
        g1 = greduce(g1,n)

    return g1

def shift_to_center(image):
    x_l = image.shape[1]
    y_l = image.shape[0]


    # Centro de la imagen
    x_centro = np.floor(x_l/2)
    y_centro = np.floor(y_l/2)

    # Centro de mas del numero
    xi,yi = mass_center(image)

    dx = int(x_centro - xi)
    dy = int(y_centro - yi)

    shift_image = np.zeros_like(image)
    print(f"centro de masa: {xi},{yi}")
    print(f"centro de imagen: {x_centro},{y_centro}")
    print(f"dx: {dx}")
    print(f"dy: {dy}")
    # Desplazamos la imagen
    if (dy>=0) and (dx>=0):
        dx = abs(dx)
        dy = abs(dy)
        shift_image[dy:,dx:] = image[0:y_l-dy,0:x_l-dx]
    if (dy>=0) and (dx<0):
        dx = abs(dx)
        dy = abs(dy)
        shift_image[dy:,0:x_l-dx] = image[0:y_l-dy,dx:]
    if (dy<0) and (dx>=0):
        dx = abs(dx)
        dy = abs(dy)
        shift_image[0:y_l-dy,dx:] = image[dy:,0:x_l-dx]
    if (dy<0) and (dx<0):
        dx = abs(dx)
        dy = abs(dy)
        shift_image[0:y_l-dy,0:x_l-dx] = image[dy:,dx:]




    return shift_image

def mass_center(image):
    """
    Esta funcion calcula el centro de masa de un arreglo bidimensional de numpy
    INPUT:
    image: array [i,j].

    OUTPUT:
    (x,y) . Pixel donde esta el centro de masa
    """
    x = np.arange(0, image.shape[1], 1)
    y = np.arange(0, image.shape[0], 1)
    xv, yv = np.meshgrid(x, y)

    xc = np.sum(image*xv)/np.sum(image)
    yc = np.sum(image*yv)/np.sum(image)

    return (np.around(xc),np.around(yc))
if __name__ == '__main__':
    matriz = np.random.rand(8,8)
    print(greduce(matriz,2))