# StructureLab

StructureLab es una aplicacion de escritorio para analisis estructural matricial
en ingenieria civil. Permite analizar matrices 2x2 y 3x3, calcular propiedades
matematicas y mostrar una interpretación física con gráficas que permitan entender de un mejor forma el analisis.

## Funcionalidades

- Ingreso de matrices 2x2 o 3x3.
- Calculo de determinante, traza, inversa, transpuesta, valores propios y
  vectores propios.
- Clasificacion de estabilidad, rigidez y condicion numerica.
- Interpretacion estructural automatica en lenguaje de ingenieria.
- Visualizacion de estructura, mapa de calor y modos vectoriales.
- Exportacion de reportes PDF con resultados y graficas.
- Historial local de analisis en `outputs/matrices/history.json`.
- Pruebas automaticas para validar los modulos matematicos.

## Estructura

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

## Instalacion

Se recomienda crear un entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecucion

```bash
python main.py
```

El proyecto cuenta con una interfaz grafica desarrollada en PyQt6, organizada de forma modular para 
separar la entrada de datos, el procesamiento matematico, la visualizacion y la exportacion de resultados.

## Pruebas

```bash
python -m unittest discover tests
```


## Nota importante

Este proyecto es academico. La interpretacion estructural es una aproximacion
educativa basada en propiedades matriciales, no reemplaza un calculo profesional
de ingenieria civil.
