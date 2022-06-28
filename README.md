# Scrapping de noticias

## Librerías necesarias
Librerías necesarias para scrapping:
- **request**
- **lxml**
- **autopep8**

## Pasos para hacer scrapping

Usaremos como ejemplo el portal de noticias [El Mercurio](https://www.emol.com/) (emol).

### **Paso 1: Obtener las rutas de cada noticia**
El primer paso es conseguir las rutas o *path* de todos los enlaces HTML de las noticias de la página. Luego, habrá que obtener los *path* para el título, el resumen y el cuerpo de cada noticia. 

Para esto, recomiendo utilizar estas extensiones de Chrome que nos ayudarán mucho a la hora de obtener los distintos *path*:
- [XPath Helper](https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl): herramienta que nos entrega el *path* en XPath de todos los elementos por los cuales pasemos el mouse por encima.
- [SelectorGadget](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb/related?hl=es): esta herramienta nos entregará las etiquetas finales del *path* donde se encuentre algun determinado elemento que busquemos.

Con estas herramientas, procedemos a buscar cada uno de los *path* necesarios.

**Para obtener los enlaces HTML**, usamos SelectorGadget el cual nos indica que el HTML de los titulares se encuentra en (/h2/a). Para obtener los enlaces de todas las páginas agregamos *@href*, el cual nos entregará todas las HTML en esa determinada carpeta:
```java
$x('//h1/a/@href').map(x=>x.value)
$x('//h3/a/@href').map(x=>x.value)
```

**Para obtener una títulos**, hacemos exactamente lo mismo:
```java
$x('//div/h1/text()').map(x=>x.wholeText)
```

**Para obtener resumen**:
```java
$x('//div/h2/text()').map(x=>x.wholeText)
```

**Para obtener cuerpo de noticia**, utilizaremos la raíz que nos entrega XPath Helper, puesto que la cantidad de parrafos que componen el cuerpo de la noticia hacen más sencilla esta herramienta :
```java
$x("/html/body[@class='cont_fs_gale_f']/div[@id='contentenedor']/div[@id='LadoA']/div[@id='cont_iz_creditos']/div[@id='cont_iz_cuerpo']/div[@id='texto_noticia']/div[@id='cuDetalle_cuTexto_textoNoticia']/div//text()").map(x => x.wholeText)
```
Para confirmar que nuestros comandos están correctos, accedemos a la consola de nuestro navegador (puedes acceder a ella presionando *Ctrl+F12*) y vemos si cada uno de los *path* encontrados nos devuelve como output el scrapping que estamos buscando.