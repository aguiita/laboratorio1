
from skimage import io
#para leer imagenes

import numpy as np
#para trabajar con arreglos y matrices

import glob
import os
#para buscar archivos en carpetas
import plotly.express as px 
# Para gráficos
import matplotlib.pyplot as plt  
from mpl_toolkits.mplot3d import Axes3D  # para gráficos 3D
import plotly.graph_objects as go

# carpeta donde estan las fots

ruta_imagenes = "/Users/agmendez/Downloads/fotosmoneda/"
#print(os.listdir(ruta_imagenes))

#busco todos los png en la carpta y los ordeno
#igual ya son todos png
archivos = [os.path.join(ruta_imagenes, f)  #me construye la ruta de las img, me las pega con ruta imganes a la ruta de la fot
            for f in os.listdir(ruta_imagenes) #lista de los elementos de la carpeta
            if f.lower().endswith((".tif", ".png", ".jpg"))] #filtra solo png tif y jpg
#mi lista archivos tiene las rutas completas de las imagenes


#%%
#printeo la cantidad y el primero para probar
#print("Cantidad de imágenes encontradas:", len(archivos))
#print("Primer archivo:", archivos[0] if archivos else "Ninguno")

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
    #print(f"Imagen {archivo} leída con forma {img.shape} y tipo {img.dtype}")
   # print (imagenes)
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
 # para cada uno de estos arrays, hago un flatten para ""aplastarlo"
#y paso de tener los indices de mi array,a tener un vector lineal ordenado,
#esscomo que lo baja a una dimension, un vector, una lista
# ssi tengo ([[123],[456]]), lo convierte en [123456]

Z, Y, X = np.indices(volumen.shape)
factor = 30  # plo puedo cambiar
x = X.flatten()[::factor]
y = Y.flatten()[::factor]
z = Z.flatten()[::factor]
c = volumen.flatten()[::factor]
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


# puedo usar un ax.scatter(x.flatten(), y.flatten(), z.flatten())
# donde cada (x[i], y[i], z[i]) es un voxel en el espacio.
# scatter es para graficar puntos
# uso un factor para usar solo algunos voxeles y no todos para q no se cuelgue



# me quedaria : [0,1,2,3,4,5,6,7,8,9][::3] → [0,3,6,9]
#esto lo saco cuando use muchas imagenes 

# ahora con mi array 3d, hago mi figura 3d
#con pltfigure creo mi ""hoja""
#el subplot es como mi cuadro de dibujo
 

c = np.asarray(c, dtype=float)
cmin, cmax = c.min(), c.max()
c = np.zeros_like(c) if cmax == cmin else (c - cmin) / (cmax - cmin)

# Reconstrucción 3D interactiva con Plotly
fig3d = go.Figure(data=[
    go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=2,
            color=c,
            colorscale='gray',
            opacity=0.1,
            colorbar=dict(title='Intensidad')
        )
    )
])

fig3d.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
        aspectmode="cube"
    ),
    title="Reconstrucción 3D interactiva"
)

fig3d.show()

# Mostrar un slice 2D como referencia
fig2d = px.imshow(volumen[0, :, :], color_continuous_scale="gray")
fig2d.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
fig2d.show()
