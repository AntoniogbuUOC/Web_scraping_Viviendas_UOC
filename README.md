# Web Scraping Viviendas UOC
_Este repositorio ha sido creado para realizar un estudio del mercado de las viviendas en la zona de Madrid Oeste, mediante el uso de técnicas de Web Scraping.
URL del sitio elegido: https://www.fotocasa.es/es/ _

## Integrantes del grupo ✒️
* **Mario García Puebla** - mariogar@uoc.edu
* **Antonio García-Bustamante Usano** - agarcia-bustamante@uoc.edu

## Archivos 📋
_La distribución de archivos es la siguiente._
* **Memoria.pdf**: Contiene la respuesta a las preguntas planteadas
* **dataset**: Contiene el dataset final obtenido tras la ejecución del programa
* **source**: 
    * **cfg**: incluye un archivo para poder autenticarse en la página web y un archivo con las localidades a buscar.
    * **data**: carpeta en donde se almacenan los datos de cada localidad durante el proceso.
    * **drivers**: carpeta que contiene el chromedriver para poder ejecutar el programa.
    * **scrappingFunctions.py**: archivo que contiene las funciones utilizadas para realizar la extracción de información.
    * **main.py**: archivo que ejecuta el programa entero.
    * **join.py**: archivo que unifica todos los dataset obtenidos por localidades y los junta en uno solo

## Ejecución ⚙️

_Para ejecutar el programa, en primer lugar hay que ejecutar el archivo main.py para obtener el dataset por cada localidad._

```
python main.py
```

_Una vez obtenidos los dataset por localidad, se juntan todos los datos en el dataset final con el archivo join.py._

```
python join.py
```
## Enlace del DOI  📄

[DOI Dataset_Viviendas_Madrid_Oeste](https://doi.org/10.5281/zenodo.7315303)

## Enlace al vídeo de presentación 📹

Enlace al vídeo de presentación: https://drive.google.com/file/d/1hQLvSxBPqZvxMdPnpa3_oVg2tgb7oC3Q/view?usp=share_link 

