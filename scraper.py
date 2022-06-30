import os
import datetime
import requests
import bs4

HOME_URL = 'https://www.emol.com'
BS_LINKS_TO_ARTICLE = ["h1 a", "h3 a"]
BS_TITLE = 'div h1'
BS_SUMMARY = 'h2[id=cuDetalle_cuTitular_bajadaNoticia]'
BS_BODY = 'div div[id=cuDetalle_cuTexto_textoNoticia]'

def get_text(soup, object):
    for paragraph in soup.select(object):
        var = paragraph.get_text()
    return var

def file_name_cleaner(title):
    file_name = title.replace('\"', '-')
    file_name = title.replace(':', '-')
    file_name = title.replace('$', '-')
    file_name = title.replace('/', '-')
    return file_name

def write_file(today, title, summary, body, file_name):
    print("\n")
    with open(f'news/{today}/{file_name}.txt', 'w', encoding='utf-8') as f:
        f.write(title)
        f.write('\n\n')
        f.write(summary)
        f.write('\n\n')
        f.write(body)
        f.write('\n\n')

def scrapper(link, today, i, k):
    response = requests.get(link)
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        
        title = get_text(soup, BS_TITLE)
        summary = get_text(soup, BS_SUMMARY)
        body = get_text(soup, BS_BODY)
        file_name = file_name_cleaner(title)

        print(f"Descargando noticia {k+1} de {i-1} ({round((k+1)/(i-1)*100,1)}% completado): \n {title} \n ({link})")

        if os.path.isfile(os.path.dirname(os.path.abspath(__file__)) + "/news/" + today + "/" + title + ".txt"):
            print(f"(!) Esta noticia ya está guardada en el directorio.\n\n")
        else:
            write_file(today, title, summary, body, file_name)
    else:
        raise ValueError(f'Error: {response.status_code}')

def create_folders(today):
    if not os.path.isdir('news'):
        os.mkdir('news')
    if not os.path.isdir(os.path.dirname(os.path.abspath(__file__)) + "/news/" + today):
        os.mkdir(os.path.dirname(os.path.abspath(__file__)) + "/news/" + today)

def get_links():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            bs_link_to_notices = []
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            
            for i in range(0, len(BS_LINKS_TO_ARTICLE)):
                for link in soup.select(BS_LINKS_TO_ARTICLE[i]):
                    bs_link_to_notices.append(link.get('href'))
                    bs_link_to_notices = list(map(
                        lambda x: HOME_URL + x.replace(HOME_URL, ""), bs_link_to_notices))

            today = datetime.date.today().strftime('%d-%m-%Y')
            create_folders(today)

            for link in range(0, len(bs_link_to_notices)-1):
                scrapper(bs_link_to_notices[link], today, len(
                    bs_link_to_notices), link)

    except ValueError as ve:
        print(ve)

def run():
    get_links()

if __name__ == '__main__':
    run()
