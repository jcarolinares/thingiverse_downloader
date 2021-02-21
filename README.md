# Thingiverse downloader

A program that massive downloads objects from Thingiverse.com

**Remember to put you thingiverse API TOKEN** inside the file **api_credentials.ini**

## Use

Type in your terminal to know all the options:

```bash
python thingiverse_downloader.py --help
```

For example, if you want to search objects by keywords:

```bash
python thingiverse_downloader.py --search "star wars" --pages 3
```

The optional argument pages set the number of objects to download. In this case, 12 objects per page.

You can also use other arguments like **--user** or **--newest** to download objects.

## Where are the objects

All the stls of the objects are downloaded at the folder **stls**. In case you use the option **--zip**, you will find the zip files inside the folder **zip_files** 

Enjoy!

***

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Licencia Creative Commons" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Thingiverse downloader</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Julián Caro Linares</span> licensed by <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.<br /><br />
