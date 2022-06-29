#Version 1.0
#Lucas Oliveri - oliverilucas@gmail.com
#Prueba de migración a Beautiful Soup

from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from multiprocessing.sharedctypes import Value
import os
import datetime
import requests
import lxml.html as html
import bs4

#Se declara la web de noticias
HOME_URL = 'https://www.emol.com'
#Se declaran las rutas XPath:
XPATH_LINK_TO_ARTICLE = '//h3/a/@href'
XPATH_TITLE = '//div/h1/text()'
XPATH_SUMMARY = '//div/h2/text()'
XPATH_BODY = "/html/body[@class='cont_fs_gale_f']/div[@id='contentenedor']/div[@id='LadoA']/div[@id='cont_iz_creditos']/div[@id='cont_iz_cuerpo']/div[@id='texto_noticia']/div[@id='cuDetalle_cuTexto_textoNoticia']/div//text()"
link_to_notices = []

#BS_COMMANDS
BS_LINKS_TO_ARTICLE = ["h1 a", "h3 a"]
bs_link_to_notices = []

#2
#Accedemos a las noticias
def scrapper(link, today, i, k):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                #Elementos de la noticia
                #Obtiene el título. Si el título tiene elementos especiales los elimina porque los archivos no pueden llevar carácteres especiales.
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','-')
                title = title.replace(':','-')
                title = title.replace('$','-')
                title = title.replace('/','-')
                #Obtiene el resumen
                summary = parsed.xpath(XPATH_SUMMARY)[1]
                #Obtiene el cuerpo
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                #Si encuentra alguna noticia que no tiene Summary o Title (fuera del index), no guarda la noticia:
                return
            #Panel de información
            print(f"Descargando noticia {k+1} de {i-1} ({round((k+1)/(i-1)*100,1)}% completado): \n {title} \n ({link})")
            #Verifica si la noticia ya fue descargada:
            if os.path.isfile(os.path.dirname(os.path.abspath(__file__)) + "/news/" + today + "/" + title + ".txt"):
                print(f"(!) Esta noticia ya está guardada en el directorio.\n\n")
            else:
                #Guarda el archivo
                print("\n")
                with open(f'news/{today}/{title}.txt', 'w', encoding='utf-8') as f:
                    f.write(title)
                    f.write('\n\n')
                    f.write(summary)
                    f.write('\n\n')
                    for p in body:
                        if p.find("RelacionadaDetalle") == 0:
                            continue
                        f.write(p)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        pass
    except ConnectionError as con:
        pass

#1
#Función para extraer el link de las noticias
def get_links():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            bs_link_to_notices = []
            response = requests.get(HOME_URL)
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            for i in range(0, len(BS_LINKS_TO_ARTICLE)):
                for link in soup.select(BS_LINKS_TO_ARTICLE[i]):
                    bs_link_to_notices.append(link.get('href'))
                    bs_link_to_notices = list(map(lambda x: HOME_URL + x.replace("https://www.emol.com", ""), bs_link_to_notices))
                
            for notice in bs_link_to_notices:
                print(notice)

            #Construye las carpetas
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir('news'):
                os.mkdir('news')
            if not os.path.isdir(os.path.dirname(os.path.abspath(__file__)) + "/news/" + today):
                os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "/news/" + today)
            
            for link in range(0, len(bs_link_to_notices)-1):
                scrapper(bs_link_to_notices[link], today, len(bs_link_to_notices), link)

    except ValueError as ve:
        print(ve)
    
def run():
    get_links()

if __name__ == '__main__':
    run()