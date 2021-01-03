# -*- coding: utf-8 -*-

# A Python 3 program

'''
Created by Julian Caro Linares

jcarolinares@gmail.com
@jcarolinares

'''

import requests
import json
import sys
import argparse
import os.path
from collections import OrderedDict

stl_path = "./stls"

thingiverse_api_base = "https://api.thingiverse.com/"
access_keyword = "?access_token="
# Go to https://www.thingiverse.com/apps/create and create your own Desktop app
api_token = "<API TOKEN>"

rest_keywords = {"newest": "newest", "users": "users/", "likes": "likes/",
                 "things": "things/", "files": "/files", "search": "search/",
                 "zip": "/package-url", "pages": "&page=",
                 "collections": "collections/"}

hall_of_fame = []
all_files_flag = False
zip_files_flag = False

if not os.path.exists("./zip_files"):
    os.makedirs("./zip_files/")
    print("zip_files folder created")
if not os.path.exists(stl_path):
    os.makedirs(stl_path)
    print("stls folder created")

def traffic_lights(n_pages=1):
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url = thingiverse_api_base + \
            rest_keywords["search"]+"traffic light"+access_keyword + \
            api_token+rest_keywords["pages"]+str(index+1)
        print(rest_url)
        parser_info(rest_url, "traffic_lights.json")

        save_data()


def load_data():
    # Load the data from the file to a list
    if os.path.isfile("hall_of_fame.list"):
        file = open("hall_of_fame.list", "r")
        hall_of_fame = file.readlines()
        file.close()
        # Removing \n
        hall_of_fame = [x.strip() for x in hall_of_fame]

    # for n in hall_of_fame:
    #     print(n)
    # else:
    #     print("Hall of fame file not found")


def save_data():
    # Save the data
    ordered_halloffame = list(OrderedDict.fromkeys(hall_of_fame))
    ordered_halloffame.sort()
    file = open("hall_of_fame.list", "w")
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
        rest_url = thingiverse_api_base + \
            rest_keywords["newest"]+access_keyword+api_token+rest_keywords["pages"]+str(n_pages)
        print(rest_url)
        download_objects(rest_url, "newest.json")


def user(username, n_pages=1):
    # /users/{$username}/things
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url = thingiverse_api_base + \
            rest_keywords["users"]+username+"/"+rest_keywords["things"] + \
            access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        print(rest_url)
        download_objects(rest_url, str(username+".json"))

def collection(id, n_pages=1):
    # /collections/{$id}/things
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url = thingiverse_api_base + \
            rest_keywords["collections"]+id+"/"+rest_keywords["things"] + \
            access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        print(rest_url)
        download_objects(rest_url, str(id+".json"))


def likes(username, n_pages=1):
    # /users/{$username}/things
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url = thingiverse_api_base + \
            rest_keywords["users"]+username+"/"+rest_keywords["likes"] + \
            access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        # print(rest_url)
        download_objects(rest_url, str(username+"_likes.json"))


def search(keywords, n_pages=1):
    # GET /search/{$term}/
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url = thingiverse_api_base + \
            rest_keywords["search"]+keywords+access_keyword + \
            api_token+rest_keywords["pages"]+str(index+1)
        print(rest_url)
        download_objects(rest_url, str(keywords+".json"), "search")


def parser_info(rest_url, file_name):
    s = requests.Session()  # It creates a session to speed up the downloads
    r = s.get(rest_url)
    data = r.json()

    # Save the data
    file = open(file_name, "w")
    file.write(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))
    file.close()

    # Reading the json file
    file = open(file_name, "r")
    data_pd = json.loads(file.read())

    # The page has objects?
    if (len(data_pd) == 0):
        print("\n\nNo more pages- Finishing the program")
        save_data()
        sys.exit()

    # Is it an error page?
    for n in data_pd:
        if (n == "error"):
            print("\n\nNo more pages- Finishing the program")
            save_data()
            sys.exit()

    print("Parsing data from {} objects from thingiverse".format(len(data_pd)))

    for object in range(len(data_pd)):

        object_id = str(data_pd[object]["id"])
        print("\n{} -> {}".format(data_pd[object]["name"], data_pd[object]["public_url"]))

        # Name and last name
        print("Name: {} {}".format(data_pd[object]["creator"]
                                   ["first_name"], data_pd[object]["creator"]["last_name"]))

        # If the name and last name are empty, we use the username
        # TODO check if the name is already on the list or is new->call the twitter api
        # 3 in [1, 2, 3] # => True
        if (data_pd[object]["creator"]["first_name"] == "" and data_pd[object]["creator"]["last_name"] == ""):
            hall_of_fame.append(data_pd[object]["creator"]["name"]+"\n")
        else:
            hall_of_fame.append(data_pd[object]["creator"]["first_name"] +
                                " "+data_pd[object]["creator"]["last_name"]+"\n")


def download_objects(rest_url, file_name, mode = "none"):

    # r = requests.get(rest_url)
    s = requests.Session()  # It creates a session to speed up the downloads
    r = s.get(rest_url)
    data = r.json()

    # Save the data
    file = open(file_name, "w")

    # print(json.dumps(data, indent=4, sort_keys=True,ensure_ascii=False)) # debug print
    file.write(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))
    file.close()

    # Reading the json file
    file = open(file_name, "r")
    data_pd = json.loads(file.read())

    if mode == "search":
        data_pd = data["hits"]

        # The page has objects?
        if (data_pd is None):
            print("\n\nNo more pages- Finishing the program")
            save_data()
            sys.exit()

        # Is it an error page?
        for n in data_pd:
            if (n == "error"):
                print("\n\nNo more pages- Finishing the program")
                save_data()
                sys.exit()
    else:
        data_pd = data

        # The page has objects?
        if (len(data_pd) == 0):
            print("\n\nNo more pages- Finishing the program")
            save_data()
            sys.exit()

        # Is it an error page?
        for n in data_pd:
            if (n == "error"):
                print("\n\nNo more pages- Finishing the program")
                save_data()
                sys.exit()



    print("Downloading {} objects from thingiverse".format(len(data_pd)))
    # print(data_pd)

    for object in range(len(data_pd)):
        # print(object)
        # print(data_pd[object])
        object_id = str(data_pd[object]["id"])
        print("\n{} -> {}".format(data_pd[object]["name"], data_pd[object]["public_url"]))
        print("Object id: {}".format(object_id))

        file_path = "./stls/"+data_pd[object]["name"].replace(" ", "_").replace("/", "-")
        file_path_zip = "./zip_files/"+data_pd[object]["name"].replace(" ", "_").replace("/", "-")+".zip"
 
        if zip_files_flag:
            print("\nZIP file request")
        elif not os.path.exists(file_path):
            os.makedirs(file_path)
        else:
            print("\nSkipping already downloaded object")
            continue

        # User name
        print("{} {}".format(data_pd[object]["creator"]["first_name"],
                             data_pd[object]["creator"]["last_name"]))

        # If the name and last name are empty, we use the username
        if (data_pd[object]["creator"]["first_name"] == "" and data_pd[object]["creator"]["last_name"] == ""):
            hall_of_fame.append(data_pd[object]["creator"]["name"]+"\n")
        else:
            hall_of_fame.append(data_pd[object]["creator"]["first_name"] +
                                " "+data_pd[object]["creator"]["last_name"]+"\n")
            # GET /things/{$id}/files/{$file_id}

        # Get file from a things
        r = s.get(thingiverse_api_base+rest_keywords["things"] +
                  object_id+rest_keywords["files"]+access_keyword+api_token)
        s_things = s.get(thingiverse_api_base+rest_keywords["things"] +
                  object_id+rest_keywords["zip"]+access_keyword+api_token)
        
        url_things = s_things.json()
        
        # print(url_things)
        # print(r)
        # print(thingiverse_api_base+rest_keywords["things"]+object_id+rest_keywords["files"]+access_keyword+api_token)
        files_info = r.json()

        if (zip_files_flag): # Download Thingiverse ZIP files
            print("    "+data_pd[object]["name"])
            print("Downloading ZIP file")
            # Download the file
            download_link = url_things["public_url"]
            # print(download_link)
            r = s.get(download_link)
            with open(file_path_zip, "wb") as code:
                code.write(r.content)
        else:
            for file in range(len(files_info)):

                if (all_files_flag):  # Download all the files
                    print("    "+files_info[file]["name"])
                    # Download the file
                    download_link = files_info[file]["download_url"]+access_keyword+api_token
                    r = s.get(download_link)
                    with open(file_path+"/"+files_info[file]["name"], "wb") as code:
                        code.write(r.content)
                else:  # Download only the .stls
                    if(files_info[file]["name"].find(".stl")) != -1:
                        print("    "+files_info[file]["name"])
                        # Download the file
                        download_link = files_info[file]["download_url"]+access_keyword+api_token
                        r = s.get(download_link)
                        with open(file_path+"/"+files_info[file]["name"], "wb") as code:
                            code.write(r.content)


if __name__ == "__main__":

    print("\nTHINGIVERSE DOWNLOADER")

    parser = argparse.ArgumentParser()

    parser.add_argument("--newest", type=bool, dest="newest_true",
                        help="It takes the newest objects uploaded")

    parser.add_argument("--user", type=str, dest="username",
                        help="Downloads the object of a specified user")

    parser.add_argument("--collection", type=str, dest="collection",
                        help="Downloads the collection with the specified id")

    parser.add_argument("--pages", type=int, default=1,
                        help="Defines the number of pages to be downloaded.")

    parser.add_argument("--all", type=bool, default=False,
                        help="Download all the pages available (MAX 1000).")

    parser.add_argument("--likes", type=str, dest="likes",
                        help="Downloads the likes of a specified user")

    parser.add_argument("--search", type=str, dest="keywords",
                        help="Downloads the objects that match the keywords. 12 objects per page\n Example: --search 'star wars'")
    parser.add_argument("--all-files", type=bool, dest="all_files",
                        help="Download all the files, images, stls and others\n Example: --all-files True")

    parser.add_argument("--traffic_light", type=int, dest="traffic",
                        help="Check new users that have done a traffic light, adding them to a black list")

    parser.add_argument("--zip", type=bool, default=False,
                        help="Download the complete ZIP file version-Including Thingiverse licenses")

    args = parser.parse_args()

    load_data()

    if args.all:
        args.pages = 1000
    if args.all_files:
        all_files_flag = True
    elif args.zip:
        zip_files_flag = True

    if args.newest_true:
        newest(args.newest_true)
    elif args.username:
        user(args.username, args.pages)
    elif args.likes:
        likes(args.likes, args.pages)
    elif args.keywords:
        search(args.keywords, args.pages)
    elif args.traffic:
        traffic_lights(args.traffic)
    elif args.collection:
        collection(args.collection, args.pages)
    else:
        newest(1)
