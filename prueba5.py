
from skimage import io
#para leer imagenes

import numpy as np
#para trabajar con arreglos y matrices

import glob
import os
#para buscar archivos en carpetas

# Para gráficos
import matplotlib.pyplot as plt  
from mpl_toolkits.mplot3d import Axes3D  # para gráficos 3D

# carpeta donde estan las fots

ruta_imagenes="C:/Users/agmendez/prueba2/moneda3d"
print(os.listdir(ruta_imagenes))

#busco todos los png en la carpta y los ordeno
#igual ya son todos png
archivos = [os.path.join(ruta_imagenes, f) 
            for f in os.listdir(ruta_imagenes) 
            if f.lower().endswith((".tif", ".png", ".jpg"))]
# os.path.join("mondea3d/", "*.png") en esa carpeta busca todo lo que termine en .png
#el glob me busca archivos q coincidan con el patron q le dpoy y el ospathjoin me construye rutas de una carpeta
# lo podria sacar tmb, pero es como q me evita problemas con ios y windows

#%%
#printeo la cantidad y el primero para probar
print("Cantidad de imágenes encontradas:", len(archivos))
print("Primer archivo:", archivos[0] if archivos else "Ninguno")

# ahora que encontre las imagenes, las voy a leer y guardar en una lista
imagenes=[]
for archivo in archivos:
    try:
        img = io.imread(archivo, as_gray=True)
        imagenes.append(img)
        print(f"Leída correctamente: {archivo}")
    except Exception as e:
        print(f"No se pudo leer {archivo}: {e}")
#printeo para ver que onda
#eso lo puedo sacar despues
    print(f"Imagen {archivo} leída con forma {img.shape} y tipo {img.dtype}")
    print (imagenes)
  #imagenes es una lista de matrices 
  #Cada matriz es una “rebanada” del volumen.
#%%

#ahora la lista de matrices la hago 3d
#porque quiero tener un array 3d, una pila de mis matrices
#Eje Z, es el 0 = número de imágenes
#Eje Y , es el 1 = altura de la imagen
#Eje X , es el 2 = ancho de la imagen
volumen = np.stack(imagenes, axis=0)
#axis 0 porque quiero apilar a lo largo del primer eje (el z)
# lo convierto en un bloque continuo de datos en memoria
#el npstack lo que hace es tomar cada matriz de la lista y las apila en un nuevo eje
#osea si tengo 100 imagenes de 200x200, me queda un array de 100x200x200
print("Dimensiones del volumen:", volumen.shape)
#el volumen.shape me da las dimensiones del array, osea me da la cantidad de elementos.


#creo como una grilla de coordenadas de los puntos en 3d
#me genera los indices de mi array, osea yo tengo mi array y con esto nombro mis voxeles con indices. 
#me devuelve las coordenadas de cada posicion del array
Z,Y,X= np.indices(volumen.shape) #me devuelve 3 arraays
x=X.flatten() # para cada uno de estos arrays, hago un flatten para ""aplastarlo"
#y paso de tener los indices de mi array,a tener un vector lineal ordenado,
#esscomo que lo baja a una dimension, un vector, una lista
# ssi tengo ([[123],[456]]), lo convierte en [123456]
y=Y.flatten()
z=Z.flatten()
#flatten lo que hace es convertir la matriz en un vector,lo aplasta
#osea si tengo una matriz de 200x200, me queda un vector de 40000
#osea todas las coordenadas de los puntos en 3d
#ahora tengo 3 vectores, uno para cada coordenada
#cada vector tiene la misma cantidad de elementos
#osea si tengo 100 imagenes de 200x200, me queda un vector de 4000000
#osea todas las coordenadas de los puntos en 3d (100*200*200) 
                  
#coords[0].shape   # (2, 3, 4)
#coords[0].flatten().shape  # (24,), te da una lista con valores, lista lineal.

# scaterr necesita listas 1d de coordenadas para graficar

#puedo graficar con 
#ax.scatter(x.flatten(), y.flatten(), z.flatten())
#donde cada (x[i], y[i], z[i]) es un voxel en el espacio.


C = volumen.flatten() #me aplasta el valor del volumen

# puedo usar un ax.scatter(x.flatten(), y.flatten(), z.flatten())
# donde cada (x[i], y[i], z[i]) es un voxel en el espacio.
# scatter es para graficar puntos
# uso un factor para usar solo algunos voxeles y no todos para q no se cuelgue

factor=32
x=x[::factor ]
y=y[::factor ]
z=z[::factor ]
C=C[::factor ]  
# me quedaria : [0,1,2,3,4,5,6,7,8,9][::3] → [0,3,6,9]
#esto lo saco cuando use muchas imagenes 

# ahora con mi array 3d, hago mi figura 3d
#con pltfigure creo mi ""hoja""
#el subplot es como mi cuadro de dibujo
fig = plt.figure(figsize=(10, 8)) # 10 x 8 pulgadas 
ax=fig.add_subplot(111, projection='3d')
# 111 significa 1 fila, 1 columna, 1er subplot
# projection='3d' es para que sea 3d      
# el scatter me dibuja losp puntos, pone puntos en las coordenada que les digo, como q me içubica losp untos
ax.scatter(X, Y, Z)          # dibuja los puntos
ax.set_xlabel("Eje X")       # etiqueta del eje X
ax.set_ylabel("Eje Y")       # etiqueta del eje Y
ax.set_zlabel("Eje Z")       # etiqueta del eje Z
ax.set_title("Reconstrucción 3D")  # título del gráfico

plt.show
