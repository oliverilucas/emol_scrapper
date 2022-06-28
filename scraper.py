from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from multiprocessing.sharedctypes import Value
import os
import datetime
import requests
import lxml.html as html
import pathlib

#Declaro algunas constantes
#La web de noticias
HOME_URL = 'https://www.emol.com'
#Las rutas XPath:
XPATH_LINK_TO_ARTICLE = '//h3/a/@href'
XPATH_TITLE = '//div/h1/text()'
XPATH_SUMMARY = '//div/h2/text()'
XPATH_BODY = "/html/body[@class='cont_fs_gale_f']/div[@id='contentenedor']/div[@id='LadoA']/div[@id='cont_iz_creditos']/div[@id='cont_iz_cuerpo']/div[@id='texto_noticia']/div[@id='cuDetalle_cuTexto_textoNoticia']/div//text()"
link_to_notices = []


#Accedemos a las noticias
def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                #Elementos de la noticia
                #Obtiene el título. Si el título tiene comillas las elimina por precaución.
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                #Obtiene el resumen
                summary = parsed.xpath(XPATH_SUMMARY)[1]
                #Obtiene el cuerpo
                body = parsed.xpath(XPATH_BODY)
            except IndexError:
                #Si encuentra alguna noticia que no tiene Summary o Title (fuera del index), no guarda la noticia:
                return
            #Guardamos el archivo
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



#Función para extraer el link de las noticias
def parse_home():
    try:

        #Accede la página web. Devolverá 200 si se conecta correctamente.
        response = requests.get(HOME_URL)

        if response.status_code == 200:
            
            #Obtiene el código fuente de la página accedida.
            home = response.content.decode('utf-8')

            #Toma el contenido HTML y lo transforma en un documento especial donde puedo hacer XPath
            parsed = html.fromstring(home)

            #Obtengo una lista de todos las HTTP de las noticias
            link_to_notices_a = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #Hago una pequeña transformación, puesto que los links vienen sin el HOME.
            for link in link_to_notices_a:
                link_to_notices.append(HOME_URL + str(link))
            

            ######
            # Crea una carpeta del día
            today = datetime.date.today().strftime('%d-%m-%Y')
            
            #Pregunta: Existe una carpeta llamada con la fecha de hoy?
            if not os.path.isdir('news'):
                os.mkdir('news')
            path = os.path.dirname(os.path.abspath(__file__)) + "/news/" + today
            if not os.path.isdir(os.path.dirname(os.path.abspath(__file__)) + "/news/" + today):
                os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "/news/" + today)

            for link in link_to_notices:
                parse_notice(link, today)
            




        else:
            #Elevamos un error si la página no contesta
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)
    
def run():
    parse_home()


if __name__ == '__main__':
    run()