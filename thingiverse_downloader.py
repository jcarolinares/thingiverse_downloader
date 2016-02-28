from pyquery import PyQuery as pq #actualmente solo consigo que funcione en python 2 sin embargo deberia poder ser compatible con python3
from lxml import etree
import os
import urllib
import urllib2
import time
import subprocess
import re



user=""
user_statics={"followers":0,"following":0,"designs":0,"collections":0,"makes":0,"likes":0}


print("THINGIVERSE DOWNLOADER\n")
user=raw_input("ENTER A THINGIVERSE USERNAME\n")

#Acceso al html
#d = pq("<html></html>")
#d = pq(etree.fromstring("<html></html>"))
#d = pq(url='https://es.wikipedia.org/wiki/Legan%C3%A9s')
d = pq(url='http://www.thingiverse.com/jcarolinares/likes/page:1')
#d = pq(url='http://www.thingiverse.com/will_CORP/likes/page:1')
#d = pq(url='http://google.com/', opener=lambda url, **kw: urllib.urlopen(url).read())
#d = pq(filename='table.html')

#Number of likes
data_user_statics=d('span[class="box-count"]')
data_user_statics=data_user_statics.append(" **")
data_user_statics=data_user_statics.text()
data_user_statics=data_user_statics.split("**")


#Picking data_user_statics
if data_user_statics[0]=="1K":
	user_statics["followers"]=1000
	print("WARNING: TOO MANY FOLLOWERS, TAKING ONLY THE LAST 1000")
else:
	user_statics["followers"]=int(data_user_statics[0])

print data_user_statics[1]

#ERROR-IT DOESN T TAKE THE IF==1K problems with whitespaces?
if data_user_statics[1]=="1K":
	user_statics["following"]=1000
	print("WARNING: TOO MANY USERS FOLLOWING, TAKING ONLY THE LAST 1000")
else:
	user_statics["following"]=int(data_user_statics[1])

if data_user_statics[2]=="1K":
	user_statics["designs"]=1000
	print("WARNING: TOO MANY DESIGNS, TAKING ONLY THE LAST 1000")
else:
	user_statics["designs"]=int(data_user_statics[2])

if data_user_statics[3]=="1K":
	user_statics["collections"]=1000
	print("WARNING: TOO MANY COLLECTIONS, TAKING ONLY THE LAST 1000")
else:
	user_statics["collections"]=int(data_user_statics[3])

if data_user_statics[4]=="1K":
	user_statics["makes"]=1000
	print("WARNING: TOO MANY MAKES, TAKING ONLY THE LAST 1000")
else:
	user_statics["makes"]=int(data_user_statics[4])

if data_user_statics[5]=="1K":
	user_statics["likes"]=1000
	print("WARNING: TOO MANY LIKES, TAKING ONLY THE LAST 1000")
else:
	user_statics["likes"]=int(data_user_statics[5])

#print user_statics

#Calculates the numbers of likes pages
if user_statics["likes"]%12 ==0:
	n_likes_pages=user_statics["likes"]/12
else:
	n_likes_pages=(user_statics["likes"]/12)+1
print n_likes_pages

objects_list=[]


for page in range(n_likes_pages):

	url_name="http://www.thingiverse.com/"+user+"/likes/page:"+str(page+1)
	print url_name
	d=pq(url=url_name)
	#d = pq(url='http://www.thingiverse.com/jcarolinares/likes/page:1')
	#d = pq(url='http://www.thingiverse.com/will_CORP/likes/page:1')
	#http://www.thingiverse.com/will_CORP/likes

	#Selection of object info
	date_data=d('div[data-type="Thing"]')
	date_data=date_data.append(" **")
	event_link=date_data #We use event_link to take the object html links
	date_data=date_data.text()
	date_data=date_data.split("**")

	event_link=str(event_link)
	event_link=event_link.split("**")

	#Taking the Objects ID and rebuilding the URL
	for x in range(len(event_link)):

		relative_link=re.search('href="(.+?)\"',event_link[x])

		if relative_link:
			event_link[x]= relative_link.group(1)
			#event_link[x]="http://www.thingiverse.com"+str(event_link[x])
			objects_list.append("http://www.thingiverse.com"+str(event_link[x]))
			#print event_link[x]


downloads_links=[]
for x in objects_list:
	print x
	downloads_links.append(x+"/zip")



#Now we have all the objects links, it s time to download the objects
#pd=pq(url=objects_list[0])


#downloads_links=downloads_links.append(" **")
#downloads_links=downloads_links.text()
#downloads_links=downloads_links.split("**")

print("DOWNLOADING FILES")
subprocess.call('mkdir '+user,shell=True)
#print and download downloads_links
i=0
for x in downloads_links:
	print(x)
	subprocess.call('wget -O '+'./'+user+'/file'+str(i)+'.zip ' +'"'+x+'"' ,shell=True)
	i=i+1

#subprocess.call('wget -O '+'./jcarolinares/prueba_wget.zip ' +'"http://www.thingiverse.com/thing:15276/zip"' ,shell=True)
#subprocess.call('echo pru.txt',shell=True)
'''
#Puede que se encuentre con archivos no descargables que den error, usar excepciones para continnuar el for
archivoDescargar = "http://www.thingiverse.com/thing:15276/zip"
archivoGuardar = "descarga.zip"

now = time.time()

descarga = urllib2.urlopen(archivoDescargar)

ficheroGuardar=file(archivoGuardar,"w")
ficheroGuardar.write(descarga.read())
ficheroGuardar.close()

elapsed = time.time() - now

print "Descargado el archivo: %s en %0.3fs" % (archivoDescargar,elapsed)

'''

'''
<a href="/thing:1375883/zip" class="thing-download-btn thing-option-btn track" data-track-category="[&quot;thing&quot;, &quot;thing&quot;]" data-track-action="[&quot;download&quot;, &quot;download_logged_in&quot;]" data-track-label="[&quot;zip&quot;, &quot;zip&quot;]">Download This Thing!</a>

'''

'''
import urllib2
import time

archivoDescargar = "http://www.lawebdelprogramador.com/logolwp100x25.jpg"
archivoGuardar = "logoLWP.jpg"

now = time.time()

descarga = urllib2.urlopen(archivoDescargar)

ficheroGuardar=file(archivoGuardar,"w")
ficheroGuardar.write(descarga.read())
ficheroGuardar.close()

elapsed = time.time() - now

print "Descargado el archivo: %s en %0.3fs" % (archivoDescargar,elapsed)
'''
