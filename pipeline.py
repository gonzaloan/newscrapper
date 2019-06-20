import logging
logging.basicConfig(level=logging.INFO)
import subprocess #manipular archivos de terminal

logger = logging.getLogger(__name__)
news_sites_uids = ['eluniversal', 'elpais']

def _extract():
    logger.info('Starting Extract process')
    for news_sites_uid in news_sites_uids:
        #Ejecuta el script main de la carpeta extract
        #Esto generará un archivo del nombre del sitio más la fecha
        subprocess.run(['python', 'main.py', news_sites_uid], cwd='./extract')
        #Buscar todos los archivos que empiecen con le uid, y los moveremos a transform y cambiaremos el nombre.
        subprocess.run(['find', '.', '-name', '{}*'.format(news_sites_uid),
                        '-exec', 'mv', '{}', '../transform/{}_.csv'.format(news_sites_uid),
                        ';'], cwd='./extract')
def _transform():
    logger.info('Starting transform process')
    for news_sites_uid in news_sites_uids:
        #guardamos los nombews de los archivos a crear, un csv para los datos sucios y otro csv para los datos limpios
        dirty_data_filename = '{}_.csv'.format(news_sites_uid)
        clean_data_filename = 'clean_{}'.format(dirty_data_filename)
        #corremos el main.py de la carpeta transform con el csv sucio, y esto creará el nuevo csv limpio
        subprocess.run(['python', 'main.py', dirty_data_filename], cwd='./transform')
        #Eliminar archivo sucio
        subprocess.run(['rm', dirty_data_filename], cwd = './transform')
        #mover el archivo generado a la carpeta load
        subprocess.run(['mv', clean_data_filename, '../load/{}.csv'.format(news_sites_uid)], cwd='./transform')
    
def _load():
    logger.info('Starting load process')
    for news_sites_uid in news_sites_uids:
        #declaramos el nombre del archivo limpio
        clean_data_filename = '{}.csv'.format(news_sites_uid)
        #correr
        subprocess.run(['python', 'main.py', clean_data_filename], cwd='./load')
        #borramos archivo
        subprocess.run(['rm', clean_data_filename], cwd='./load')
def main():
    _extract()
    _transform()
    _load()

if __name__ == '__main__':
    main()

