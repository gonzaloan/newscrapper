import argparse
from common import config
import logging
import news_page_objects as news
import re
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError
import datetime
import csv

logging.basicConfig(level=logging.INFO)
is_well_formed_link = re.compile(r'^https?://.+/.+$') #r es string raw
# esto indica que debe empezar con http con s opcional (http o https), después seguido por dos slash
# que tenga al menos una o más letras (.+), otro slash y una o más letras (.+), y $ termina.
is_root_path = re.compile(r'^/.+$')
#empieza con un guión, despues tiene una o más letras y termina. Ejemplo /some-text

logger = logging.getLogger(__name__)

def _news_scrapper(news_site_uid):
    #url
    host = config()['news_sites'][news_site_uid]['url']
    logging.info('Iniciando scrapper para {}'.format(host))

    homepage = news.HomePage(news_site_uid, host)
    articles = []
    print("homepage {}".format(homepage.article_links))
    
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)

        if article:
            logger.info('Article fetched')
            articles.append(article)
            print(article.title)
        print(len(articles))
   
    _save_articles(news_site_uid, articles)

def _save_articles(news_site_uid, articles):
    now = datetime.datetime.now().strftime('%Y_%m_&d')
    out_file_name = '{news_site_uid}_{datetime}_articles.csv'.format(news_site_uid= news_site_uid, datetime=now)

    print('\n\n\n ', articles)
    if articles:
        csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))
        with open(out_file_name, mode = 'w+', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_headers)

            for article in articles:
                row = [str(getattr(article,prop)) for prop in csv_headers]
                writer.writerow(row)

def _fetch_article(news_site_uid, host, link):
    logger.info('Start Fetching artitle at {}'.format(link))
    article = None
    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning('Error while fetching article', exc_info=False) #No mostramos log para no ensuciar consola

    
    print("\n\n\n\n Article, ", article)

    if article and not article.body:
        logger.warning('Invalid article. There is no body')
        return None

    return article

def _build_link(host, link):
    #agregamos regex para verificar que sean válidos
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return '{}{}'.format(host,link)
    else:
        return '{host}/{uri}'.format(host=host, uri=link)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    news_site_choices = list(config()['news_sites'].keys())
    parser.add_argument('news_site', help= 'El sitio de noticias que se quiere hacer scrape',
                        type=str,
                        choices = news_site_choices)
    args = parser.parse_args()
    _news_scrapper(args.news_site)



    