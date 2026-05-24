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
|   |-- config/
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

Después de descargar y descomprimir el proyecto, abra `cmd` en la carpeta principal del proyecto, es decir, en la carpeta donde se encuentra el archivo `main.py`.

```cmd
py -m pip install -r requirements.txt
```

## Ejecución

```cmd
py main.py
```

Si el comando `py ` no funciona, puede intentar con:
```cmd
python main.py
```



### Notas Importantes:
Este proyecto fue creado con fines académicos, por tal razón la interpretación 
estructural es una aproximación basada en propiedades matriciales y demás temas
vistos en el álgebra lineal.

Importante: cuando descargues desde GitHub, debes entrar a la carpeta descomprimida que contiene directamente:

```text
main.py
requirements.txt
src
data
docs
```
Si se encuentra en una carpeta anterior a esa, los comandos no funcionarán correctamente.

Para entrar desde `cmd`, use el comando `cd /d` seguido de la ruta de la carpeta. Por ejemplo:

```cmd
cd /d "C:\Users\LAURA\Desktop\Proyecto-final-programaci-n-main"
```
También puede hacerlo de una forma más sencilla: abra la carpeta correcta en el Explorador de archivos, haga clic en la barra de dirección, escriba `cmd` y presione Enter. Esto abrirá la terminal directamente en esa ubicación.
