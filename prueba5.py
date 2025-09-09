from skimage import io
import numpy as np
import os
import plotly.graph_objects as go

# Carpeta donde están las imágenes
ruta_imagenes = "/Users/agmendez/Downloads/fotosmoneda"

# Buscar archivos de imagen
archivos = [os.path.join(ruta_imagenes, f) 
            for f in os.listdir(ruta_imagenes) 
            if f.lower().endswith((".tif", ".png", ".jpg"))]

# Leer imágenes en escala de grises
imagenes = []
for archivo in archivos:
    try:
        img = io.imread(archivo, as_gray=True)
        imagenes.append(img)
        print(f"Leída correctamente: {archivo}")
    except Exception as e:
        print(f"No se pudo leer {archivo}: {e}")

# Crear volumen 3D (Z, Y, X)
volumen = np.stack(imagenes, axis=0)
print("Dimensiones del volumen:", volumen.shape)

# Crear grilla de coordenadas
Z, Y, X = np.indices(volumen.shape)
x_all = X.flatten()
y_all = Y.flatten()
z_all = Z.flatten()
C_all = volumen.flatten()

# --- Función que filtra por percentil ---
def filtrar(percentil):
    umbral = np.percentile(volumen, percentil)
    mask = C_all > umbral
    return x_all[mask], y_all[mask], z_all[mask], C_all[mask]

# --- Crear figura inicial ---
percentil_inicial = 50
x, y, z, C = filtrar(percentil_inicial)

scatter = go.Scatter3d(
    x=x, y=y, z=z,
    mode="markers",
    marker=dict(size=1, color=C, colorscale="Gray", opacity=1)
)

fig = go.Figure(data=[scatter])

# --- Slider interactivo ---
steps = []
for p in range(1, 100):  # percentiles 10,20,...90
    x, y, z, C = filtrar(p)
    step = dict(
        method="update",
        args=[{"x": [x], "y": [y], "z": [z],
               "marker": [dict(size=1, color=C, colorscale="Gray", opacity=1)]}],
        label=f"{p}%"
    )
    steps.append(step)

sliders = [dict(
    active=percentil_inicial//10 - 1,
    currentvalue={"prefix": "Umbral (percentil): "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    scene=dict(
        xaxis_title="Eje X",
        yaxis_title="Eje Y",
        zaxis_title="Eje Z"
    ),
    title="Reconstrucción 3D interactiva con control de umbral",
    sliders=sliders
)

fig.show(renderer="browser")
