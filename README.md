# StructuraLab

StructuraLab es una aplicacion de escritorio para analisis estructural matricial
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

La interfaz puede programarse desde Visual Studio Code, pero si deseas editar la
ventana de forma visual puedes usar Qt Designer. Este proyecto ya incluye la GUI
hecha en codigo PyQt6, lista para ejecutar y modificar.

## Pruebas

```bash
python -m unittest discover tests
```


## Notas importantes

Este proyecto es academico. La interpretacion estructural es una aproximacion
educativa basada en propiedades matriciales, no reemplaza un calculo profesional
de ingenieria civil.
