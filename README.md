# Proyecto final: StructureLab

Este proyecto fue realizado con el fin de aplicar conceptos de álgebra lineal y programación
en Python al análisis estructural mediante matrices. Este programa permite ingresar matrices 
2x2 y 3x3 para realizar diferentes operaciones matemáticas y visualizar los resultados 
mediante gráficas, además de mostrar una interpretación de los resultados obtenidos.


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

Primero, se deberá ingresar a la terminar y poner lo siguiente:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```



### Nota:

Este proyecto fue creado con fines académicos, por tal razón la interpretación estructural es 
una aproximación basada en propiedades matriciales y demás temas vistos en el àlgebra lineal.
