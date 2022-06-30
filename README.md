# Scrapping de emol.com
## Introducción
El script descarga todas las noticias que se encuentren en la portada del periódico [El Mercurio](https://www.emol.com/). Sin embargo, si se modifican las etiquetas HTML de las variables globales, el script está optimizado para hacer scrapping en cualquier portal de noticias.

## Variables

El script cuenta con 5 variables globales para su funcionamiento:

- ***HOME_URL*** - *Type: String*: Corresponde al link HTML del portal de noticias al que pretendemos hacer scrapping.

- ***BS_LINKS_TO_ARTICLE*** - *Type: List*:  Elemento que contiene el atributo *<href>* que contienen las direcciones HTTP de las noticias del portal.
- **BS_TITLE** - *Type: String*: Atributo que contienen los titulares de las noticias.
- **BS_SUMMARY** - *Type: String*: Atributo que contienen el resumen o bajada de las noticias.
- **BS_BODY** - *Type: String*: Atributo que contienen el cuerpo de las noticias.

## Requerimientos
### IDE:
  - Python 3 o superior.
  
### Librerías necesarias para scrapping:
  - **request**
  - **bs4**

### Otras librerías:
  - **datetime**
  - **os**

Si tienes problemas a la hora de leer código HTML, te recomiendo estas extensiones que facilitan la obtención de etiquetas, atributos y nodos:
- [XPath Helper](https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl): herramienta que nos entrega la ruta completa y el contenido de todos los elementos que seleccionemos.
- [SelectorGadget](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb/related?hl=es): esta herramienta nos entregará las etiquetas donde se encuentre algun determinado elemento que busquemos.

## Funciones principales

### **get_links()**
- Extrae los links de las noticias. 

- Crea una lista *bs_link_to_notices* la cual almacena todas las direcciones HTML dictadas según la variable global *BS_LINKS_TO_ARTICLE*.
- Cuenta con una función de orden superior que modifica ciertos HTML que vienen incompletos. Puede ocurrir que tus direcciones HTML vengan de la siguiente forma:
  ```HTML
  /noticias/nacional/fecha/link
  ```
  La función deja los HTML completos:
  ```HTML
  https://www.emol.com/noticias/nacional/fecha/link
  ```
- Llama a la función *create_folders* y *scrapper*.

### **scraper()**
- Para cada dirección HTML almacenada en la lista *bs_link_to_notices* extrae el título, resumen y cuerpo según lo declarado en las variables globales: *BS_TITLE*, *BS_SUMMARY* y *BS_BODY* a través de la función *get_text()*.
- Verifica que el nombre del archivo de texto a guardar en el directorio no tenga caracteres especiales a travésde la función *file_name_cleaner*. Por cierto, el archivo llevará como nombre el titular de la noticia.
- Finalmente, escribe el documento de texto a través de la función *write_file*.

## Créditos
* [Lucas Oliveri](https://www.linkedin.com/in/oliverilucas) - (oliverilucas@gmail.com)