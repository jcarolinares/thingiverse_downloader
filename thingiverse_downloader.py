import requests
import json
import sys
import argparse

thingiverse_api_base="https://api.thingiverse.com/"
access_keyword="?access_token="
api_token="bc56e9669fca74e63a9de72061b929ca"# This must be inside another file SEE zowi to more info

rest_keywords={"newest":"/newest","users":"/users/","things":"/things/","files":"/files","search":"/search/","pages":"&page="}

# username=rest_keywords["users"]+"jcarolinares"
#newest things
newest="/newest" #https://api.thingiverse.com/newest?access_token=bc56e9669fca74e63a9de72061b929ca
#things
things="/things/" #GET /things/{$id}/files/{$file_id}
#https://api.thingiverse.com/things/2976276?access_token=bc56e9669fca74e63a9de72061b929ca
#files
files="/files"

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
        print("\n{} -> {}".format(data_pd[object]["name"],data_pd[object]["public_url"]))
        # print("Object id: {}".format(object_id))

        #Get file from a things
        # GET /things/{$id}/files/{$file_id}
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


if __name__ == "__main__": #TODO use another library to simplify the arguments system

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

    # parser.set_defaults(func=newest(1)) #If we don't have an argument. It calls the newest option with only 1 page

    args = parser.parse_args()
    # args.func(args)  # call the default function


    if args.newest_true:
        newest(args.newest_true)
    elif args.username:
        user(args.username,args.pages)
    elif args.keywords:
        search(args.keywords,args.pages)
