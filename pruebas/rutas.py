"""Las dos rutas de las pruebas: RAIZ, el repo (la carpeta de arriba), y PRUEBAS, esta carpeta. Lo que escriben las
pruebas (capturas de pantalla, mediciones) va en SALIDA, que git no sigue."""
import os
PRUEBAS = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(PRUEBAS)
SALIDA = os.path.join(PRUEBAS, 'salida')
os.makedirs(SALIDA, exist_ok=True)
