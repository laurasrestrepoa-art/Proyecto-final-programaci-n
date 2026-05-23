# Ejemplos de ejecucion de StructuraLab

Este documento presenta ejemplos de entrada y salida para evidenciar el
funcionamiento del proyecto.

## Cómo ejecutar el programa

Después de descargar y descomprimir el proyecto, abre `cmd` dentro de la carpeta principal del proyecto.

Luego ejecuta:

```cmd
py main.py

Si es la primera vez en el computador:

```cmd
py -m pip install -r requirements.txt
py main.py
```

Y para las pruebas:

```md
## Cómo ejecutar las pruebas

Desde la carpeta principal del proyecto, ejecuta:

```cmd
py -B -m unittest discover tests

## Ejemplo 1: matriz estable 2x2

Entrada:

```text
[ 4  -2 ]
[ -2  4 ]
```

Resultados obtenidos:

```text
Determinante: 12.0000
Traza: 8.0000
Valores propios: 6.0000, 2.0000
Nivel de riesgo: Bajo
Estado: Estable y rigido
```

Interpretacion:

La matriz es simetrica, tiene valores propios positivos y presenta dominancia
diagonal. Por eso el sistema se clasifica como estable y rigido.

## Ejemplo 2: matriz estable 3x3

Entrada:

```text
[ 6  -2   1 ]
[ -2  5   0 ]
[ 1   0   3 ]
```

Resultados obtenidos:

```text
Determinante: 73.0000
Traza: 14.0000
Valores propios: 7.6964, 3.8218, 2.4818
Nivel de riesgo: Bajo
Estado: Estable y rigido
```

Interpretacion:

La matriz 3x3 tiene determinante diferente de cero y valores propios positivos.
En la pestana de vectores, el programa representa los modos propios en una
grafica 3D con componentes X, Y y Z.

## Ejemplo 3: matriz critica 2x2

Entrada:

```text
[ 2  4 ]
[ 1  2 ]
```

Resultados obtenidos:

```text
Determinante: 0.0000
Traza: 4.0000
Valores propios: 4.0000, 0.0000
Nivel de riesgo: Critico
Estado: Sistema singular o cercano a singular
```

Interpretacion:

El determinante es cero y uno de los valores propios tambien es cero. Esto
indica posible singularidad, perdida de rigidez o falta de restricciones dentro
del modelo simplificado.
