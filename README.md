# Proyecto final: StructureLab

StructureLab es un proyecto académico desarrollado con el propósito de aplicar conceptos de álgebra lineal
y programación en Python al análisis estructural mediante matrices.

El programa permite ingresar matrices de tamaño 2x2 y 3x3, realizar operaciones matemáticas como determinante,
traza, inversa, transpuesta, valores propios y vectores propios, y visualizar los resultados mediante gráficas. 
Además, genera una interpretación estructural de los resultados obtenidos, relacionando el comportamiento matemático 
de la matriz con conceptos como estabilidad, rigidez, deformación y modos de respuesta.

## Funciones principales: 

- Ingreso de matrices 2x2 y 3x3.
- Cálculo de determinante.
- Obtención de la matriz inversa y transpuesta.
- Cálculo de valores y vectores propios.
- Visualización de gráficas y mapas de calor.
- Generación de reportes en PDF.
- Guardado básico del historial de análisis.

## Estructura del proyecto:

```text
StructuraLab/
|-- main.py
|-- src/
|   |-- analysis/
|   |-- gui/
|   |-- storage/
|   |-- utils/
|   `-- visualization/
|-- data/
|-- outputs/
|   |-- graphs/
|   |-- matrices/
|   `-- reports/
|-- tests/
|-- requirements.txt
`-- README.md
```

## Instalación:

Después de descargar y descomprimir el proyecto, abraa `cmd` dentro de la carpeta principal y ejecute:

```cmd
pip install -r requirements.txt
```

## Ejecución

```cmd
python main.py
```



### Nota Importante:
Este proyecto fue creado con fines académicos, por tal razón la interpretación 
estructural es una aproximación basada en propiedades matriciales y demás temas
vistos en el álgebra lineal.
