## Newscrapper

Proyecto en Python que hace Scrapping a varios sitios web de noticias. 

Trabaja haciendo ETL(Extract, Translate, Load), y está separado en carpetas que cumplen dichas funcionalidades, que pueden ser ejecutadas una a una y también posee un pipeline que ejecuta todas las tareas una tras otra.

### Extracción

La extracción de datos puede ejecutarse desde la carpeta /extract/ con:
```python
python main.py {nombre_newspaper}
```
Esto generara un archivo CSV con el nombre del newspaper y los datos sucios.

Luego de los datos sucios, debe ser limpiado, para lo cual se debe iniciar el proceso de *Transform*

### Transformación

Para esto se debe entrar en la carpeta /transform y ejecutar:

```python
python scrapper_newspaper_receipe.py {fuente_de_datos.csv}
```
Entregando como parámetro el archivo CSV que se quiera limpiar.

Finalmente, se carga en una base de datos haciendo la parte de **Load**

### Carga

Este script sólo toma estos datos y los inserta en una base de datos. Este script, crea un archivo db de tipo Sqlite

```python
python main.py {fuente_de_datos_limpia.csv}
```
### Pipeline
El pipeline ejecuta todas las tareas automatizadas. Para ejecutar el pipeline se debe usar el Script **pipeline.py**:
```python
python pipeline.py
```
Se puede editar y agregar nuevos data sources modificando la siguiente línea:
```python
news_sites_uids = ['eluniversal', 'elpais']
```
Agregando el source que se requiera, que debe existir en el archivo config.yaml de extract/config.yaml



