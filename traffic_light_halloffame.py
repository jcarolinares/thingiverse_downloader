# -*- coding: utf-8 -*-

import requests
import json
import sys
import argparse
from collections import OrderedDict

thingiverse_api_base="https://api.thingiverse.com/"
access_keyword="?access_token="
api_token="put your api token here" #Go to https://www.thingiverse.com/apps/create and select Desktop app

rest_keywords={"newest":"/newest","users":"/users/","things":"/things/","files":"/files","search":"/search/","pages":"&page="}

hall_of_fame=[]

def traffic_lights(n_pages=1):
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["search"]+"traffic light"+access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        parser_info(rest_url,"traffic_lights.json");

    #Save the data
    ordered_halloffame=list(OrderedDict.fromkeys(hall_of_fame))
    ordered_halloffame.sort()
    file=open("hall_of_fame.list","w")
    for user in ordered_halloffame:
        try:
            file.write(user)
        except:
            print("Error in name: {}".format(user))
            file.write(user)
            continue
    file.close()

def newest(n_pages=1):
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["newest"]+access_keyword+api_token+rest_keywords["pages"]+str(n_pages)
        download_objects(rest_url,"newest.json");

def user(username,n_pages=1):
    #/users/{$username}/things
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["users"]+username+rest_keywords["things"]+access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        download_objects(rest_url,str(username+".json"));

def search(keywords,n_pages=1):
    #GET /search/{$term}/
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["search"]+keywords+access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        download_objects(rest_url,str(keywords+".json"));

def parser_info(rest_url, file_name):
    s = requests.Session() #It creates a session to speed up the downloads
    r=s.get(rest_url)
    data=r.json()

    #Save the data
    file=open(file_name,"w")
    file.write(json.dumps(data, indent=4, sort_keys=True,ensure_ascii=False).encode('utf8'))
    file.close()

    #Reading the json file
    file=open(file_name,"r")
    data_pd=json.loads(file.read())

    print("Parsing data from {} objects from thingiverse".format(len(data_pd)))

    for object in range(len(data_pd)):

        object_id=str(data_pd[object]["id"])
        print("\n{} -> {}".format(data_pd[object]["name"].encode('utf-8'),data_pd[object]["public_url"]))

        #Name and last name
        print("Name: {} {}".format(data_pd[object]["creator"]["first_name"].encode('utf-8'),data_pd[object]["creator"]["last_name"].encode('utf-8')))

        #If the name and last name are empty, we use the username
        if (data_pd[object]["creator"]["first_name"]=="" and data_pd[object]["creator"]["last_name"]==""):
            hall_of_fame.append(data_pd[object]["creator"]["name"].encode('utf-8')+"\n")
        else:
            hall_of_fame.append(data_pd[object]["creator"]["first_name"].encode('utf-8')+" "+data_pd[object]["creator"]["last_name"].encode('utf-8')+"\n")



def download_objects(rest_url, file_name):

    # r = requests.get(rest_url)
    s = requests.Session() #It creates a session to speed up the downloads
    r=s.get(rest_url)
    data=r.json()

    #Save the data
    file=open(file_name,"w")
    file.write(json.dumps(data, indent=4, sort_keys=True,ensure_ascii=False).encode('utf8'))
    file.close()

    #Reading the json file
    file=open(file_name,"r")
    data_pd=json.loads(file.read())

    print("Downloading {} objects from thingiverse".format(len(data_pd)))

    for object in range(len(data_pd)):

        object_id=str(data_pd[object]["id"])
        print("\n{} -> {}".format(data_pd[object]["name"].encode('utf-8'),data_pd[object]["public_url"]))
        # print("Object id: {}".format(object_id))

        #test
        print("{} {}".format(data_pd[object]["creator"]["first_name"].encode('utf-8'),data_pd[object]["creator"]["last_name"].encode('utf-8')))

        #If the name and last name are empty, we use the username
        if (data_pd[object]["creator"]["first_name"]=="" and data_pd[object]["creator"]["last_name"]==""):
            hall_of_fame.append(data_pd[object]["creator"]["name"].encode('utf-8')+"\n")
        else:
            hall_of_fame.append(data_pd[object]["creator"]["first_name"].encode('utf-8')+" "+data_pd[object]["creator"]["last_name"].encode('utf-8')+"\n")
            # GET /things/{$id}/files/{$file_id}
        #Get file from a things
        r=s.get(thingiverse_api_base+rest_keywords["things"]+object_id+rest_keywords["files"]+access_keyword+api_token)
        files_info=r.json()

        for file in range(len(files_info)):
            if(files_info[file]["name"].find(".stl"))!=-1:
                print(files_info[file]["name"])
                #Download the file
                download_link=files_info[file]["download_url"]+access_keyword+api_token
                r = s.get(download_link)
                with open("./stls/"+files_info[file]["name"], "wb") as code:
                    code.write(r.content)


if __name__ == "__main__":

    print("\nTHINGIVERSE DOWNLOADER")

    parser = argparse.ArgumentParser()

    parser.add_argument("--newest", type=bool, dest="newest_true",
                        help="It takes the newest objects uploaded")

    parser.add_argument("--user", type=str, dest="username",
                        help="Downloads the object of a specified user")

    parser.add_argument("--pages", type=int, default=1,
                        help="Defines the number of pages to be downloaded. 30 objects per page")

    parser.add_argument("--search", type=str, dest="keywords",
                        help="Downloads the objects that match the keywords. 12 objects per page\n Example: --search 'star wars'")

    parser.add_argument("--traffic_light", type=int, dest="traffic",
                        help="Check new users that have done a traffic light, adding them to a black list")

    args = parser.parse_args()

    if args.newest_true:
        newest(args.newest_true)
    elif args.username:
        user(args.username,args.pages)
    elif args.keywords:
        search(args.keywords,args.pages)
    elif args.traffic:
        traffic_lights(args.traffic)
