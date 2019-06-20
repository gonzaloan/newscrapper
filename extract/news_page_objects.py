# Clase para obtener los objetos de las páginas a scrappear
from common import config
import requests
import bs4
import gzip

#Refactorizamos para que newsPage sea la clase padre y la homepage hijo
class NewsPage:
    def __init__(self, news_site_uid, url):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self._visit(url)
    
     #Obtiene informacion del documento que se acaba de parsear
    def _select(self, query_str):
        return self._html.select(query_str)

    # Método hará una llamada a una página web
    def _visit(self, url):
        response = requests.get(url, headers={"Accept-Encoding": "gzip"})
        #Método tirará error si hubo un error ne la petición
        response.raise_for_status()
        print(response)
        #response = gzip.decompress(response)
        #self._html = bs4.BeautifulSoup(response.text, 'html.parser')
        self._html = bs4.BeautifulSoup(response.text.encode("utf-8"), 'html.parser')
        #if response['Content-Encoding'] == 'gzip':
         
            #Método tirará error si hubo un error ne la petición
            #self._html = bs4.BeautifulSoup(response, 'html.parser')
        #else:
            #Método tirará error si hubo un error ne la petición
            


#Extiende
class HomePage(NewsPage):
    def __init__(self, news_site_uid, url):
        self._url = url
        super().__init__(news_site_uid,url)

    @property
    def article_links(self):
        link_list = []        
        for link in self._select(self._queries['homepage_article_links']):
            #Si el link es válido y tiene atributo href
            if link and link.has_attr('href'):
                link_list.append(link)
        #eliminamos si hay algun elemento repetido
        return set(link['href'] for link in link_list)

class ArticlePage(NewsPage):
    def __init__(self, news_site_uid, url):
        self._url = url
        super().__init__(news_site_uid,url)

    @property
    def body(self):
        result = self._select(self._queries['article_body'])
        if result != None:
            return result[0].text if len(result) else ''
        else:
            return ''
    @property
    def title(self):
        result = self._select(self._queries['article_title'])
        return result[0].text if len(result) else ''
    @property
    def url(self):
        return self._url
