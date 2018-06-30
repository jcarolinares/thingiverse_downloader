import requests
import json
import sys
import wget

thingiverse_api_base="https://api.thingiverse.com/"
access_keyword="?access_token="
api_token="bc56e9669fca74e63a9de72061b929ca"# This must be inside another file SEE zowi to more info

rest_keywords={"newest":"/newest","users":"/users/","things":"/things/","files":"/files","pages":"&page="}

# username=rest_keywords["users"]+"jcarolinares"
#newest things
newest="/newest" #https://api.thingiverse.com/newest?access_token=bc56e9669fca74e63a9de72061b929ca
#things
things="/things/" #GET /things/{$id}/files/{$file_id}
#https://api.thingiverse.com/things/2976276?access_token=bc56e9669fca74e63a9de72061b929ca
#files
files="/files"

def main():
    #username
    print("algo")

    #User info
    # print(thingiverse_api_base+username+access_keyword+api_token)
    #
    # r = requests.get(thingiverse_api_base+username+access_keyword+api_token)
    # data=r.json()
    #
    # #Save the data
    # file=open("user.json","w")
    # file.write(json.dumps(data, indent=4, sort_keys=True,ensure_ascii=False).encode('utf8'))
    # file.close()
    #
    # #Reading the json
def newest(n_pages=1):
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["newest"]+access_keyword+api_token+rest_keywords["pages"]+str(n_pages)
        download_objects(rest_url,"newest.json",n_pages);

def user(username,n_pages=1):
    #/users/{$username}/things
    for index in range(n_pages):
        print("\n\nPage: {}".format(index+1))
        rest_url=thingiverse_api_base+rest_keywords["users"]+username+rest_keywords["things"]+access_keyword+api_token+rest_keywords["pages"]+str(index+1)
        download_objects(rest_url,str(username+".json"));

def download_objects(rest_url, file_name):

    r = requests.get(rest_url)
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
        print(object_id)


        #Get file from a things
        # GET /things/{$id}/files/{$file_id}

        r_thing=requests.get(thingiverse_api_base+rest_keywords["things"]+object_id+rest_keywords["files"]+access_keyword+api_token)
        files_info=r_thing.json()

        for file in range(len(files_info)):
            if(files_info[file]["name"].find(".stl"))!=-1:
                print("\n"+files_info[file]["name"])
                #Download the file
                download_link=files_info[file]["download_url"]+access_keyword+api_token
                #print(download_link)
                wget.download(download_link, "./stls/"+files_info[file]["name"])


    # #Save the data
    # file=open("thing.json","w")
    # file.write(json.dumps(files_info, indent=4, sort_keys=True,ensure_ascii=False).encode('utf8'))
    # file.close()


if __name__ == "__main__": #TODO use another library to simplify the arguments system

    print("THINGIVERSE DOWNLOADER\n\n")
    if sys.argv[1]=="--newest":
        newest()
    elif len(sys.argv)==3 and sys.argv[1]=="--newest":
        newest(n_pages=int(sys.argv[2]))
    elif len(sys.argv)==3 and sys.argv[1]=="--user":
        user(sys.argv[2])
    elif len(sys.argv)==4 and sys.argv[1]=="--user":
        user(sys.argv[2],int(sys.argv[3]))
