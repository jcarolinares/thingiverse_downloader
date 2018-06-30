# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import os
import subprocess
import requests


user=""
user_statics={"followers":0,"following":0,"designs":0,"collections":0,"makes":0,"likes":0}

print("THINGIVERSE DOWNLOADER\n")
user=raw_input("ENTER A THINGIVERSE USERNAME\n")

#Downloading the page
r  = requests.get('http://www.thingiverse.com/'+user+'/likes/page:1')
data = r.text
soup = BeautifulSoup(data,"lxml")

#Number of likes
data_user_statics=[]
for link in soup.find_all('span',class_="box-count"):
	data_user_statics.append(link.get_text())
	#print(link.get_text())

#print data_user_statics

#Picking data_user_statics
if data_user_statics[0]=="1K":
	user_statics["followers"]=1000
	print("WARNING: TOO MANY FOLLOWERS, TAKING ONLY THE LAST 1000")
else:
	user_statics["followers"]=int(data_user_statics[0])

#print data_user_statics[1]

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

print user_statics


#Calculates the numbers of likes pages
if user_statics["likes"]%12 ==0:
	n_likes_pages=user_statics["likes"]/12
else:
	n_likes_pages=0
	#print (n_likes_pages)
	n_likes_pages=(user_statics["likes"]/12)+1

#print n_likes_pages

objects_names=[]
objects_list=[]
downloads_links=[]

for page in range(n_likes_pages):

	#Downloading the page
	url_name="http://www.thingiverse.com/"+user+"/likes/page:"+str(page+1)
	print url_name
	r  = requests.get(url_name)
	data = r.text
	soup = BeautifulSoup(data,"lxml")

	#Selection of object info
	date_data=[]
	for link in soup.find_all('div',class_="thing thing-interaction-parent"):
		date_data.append(link.get("data-thing-id"))
		#print(link.get("data-thing-id"))

	event_link=date_data #We use event_link to take the object html links
	title_object=[]#Auxiliar title list

	#Taking the Objects titles
	for link in soup.find_all('div',class_="thing thing-interaction-parent"):
		title_object.append(link.get("title"))

	for link in title_object:

		link=link.replace(" ","_") #Putting away namespaces
		link=link.replace("/","_") #Putting away /
		link=link.replace(";","") #Putting away ;
		link=link.replace(".","-") #Putting away not extensions points
		link=link.replace("!","-") #Putting away ! points
		link=link.replace("(","_") #Putting away ( The use of () in files names could be a problem
		link=link.replace(")","_") #Putting away ) The use of () in files names could be a problem
		link=link.replace(u"\u2122", '') #Putting away trademark symbol
		link=link.replace(",","") #Puttin away ,
		link=link.replace("&","") #Puttin away &
		link=link.replace("#","") #Puttin away #
		link=link.replace("?","") #Puttin away ?
		link=link.replace("\'","") #Puttin away single quotes
		link=link.replace("\"","") #Puttin away double quotes

		objects_names.append(link)

	#Taking the Objects ID and rebuilding the URL
	for x in range(len(event_link)):
		objects_list.append("http://www.thingiverse.com/thing:"+str(event_link[x]))

#Creating the downloading links
for x in objects_list:
	print x
	downloads_links.append(x+"/zip")

#Downloading the files
print("\n----DOWNLOADING FILES----\n")
subprocess.call('mkdir '+user,shell=True)
#likes_user_file=open('./'+user+'/'+user+'-log.txt','a')#We open or create a file with all the download links or the user-Format-title-downloaded url-state /*Donwloaded-Failed*/

#print and download downloads_links
for x in range(len(downloads_links)):
	print(downloads_links[x])
#	subprocess.call('wget -O '+'./'+user+'/file'+str(i)+'.zip ' +'"'+x+'"' ,shell=True)
	subprocess.call('wget --retry-connrefused -O '+'./'+user+'/'+objects_names[x]+'.zip ' +'"'+downloads_links[x]+'"' ,shell=True)

'''
	if os.path.exists('./'+user+'/'+objects_names[x]+'.zip'):
		likes_user_file.write(str(objects_names[x])+'-'+str(downloads_links[x])+'-downloaded\n')
	else:
		likes_user_file.write(str(objects_names[x])+'-'+str(downloads_links[x])+'-failed\n')
'''


print("Files download completed")
subprocess.call('notify-send -t 4500 "thingiverse-downloader: Files download completed"' ,shell=True)
