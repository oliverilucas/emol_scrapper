from urllib.parse import urlparse
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
csv = "news/emol_news.csv"

def main():
    logger.info('Empezando el proceso de limpiado de datos.')
    logger.info('Leyendo archivo {}'.format(csv))
    df = pd.read_csv(csv)
    logger.info('Extayendo el host de las URL')
    df['host'] = df['link'].apply(lambda url: urlparse(url).netloc)
    return df

if __name__ == '__main__':
    df = main()
    print(df)