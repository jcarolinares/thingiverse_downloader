from pyquery import PyQuery as pq #actualmente solo consigo que funcione en python 2 sin embargo deberia poder ser compatible con python3
from lxml import etree
import urllib
import re

user=""
user_statics={"followers":0,"following":0,"designs":0,"collections":0,"makes":0,"likes":0}


print("Bienvenido\n")

#Acceso al html
#d = pq("<html></html>")
#d = pq(etree.fromstring("<html></html>"))
#d = pq(url='https://es.wikipedia.org/wiki/Legan%C3%A9s')
d = pq(url='http://www.thingiverse.com/jcarolinares/likes/page:1')
#d = pq(url='http://google.com/', opener=lambda url, **kw: urllib.urlopen(url).read())
#d = pq(filename='table.html')


#Number of likes
data_user_statics=d('span[class="box-count"]')
data_user_statics=data_user_statics.append(" **")
data_user_statics=data_user_statics.text()
data_user_statics=data_user_statics.split("**")

user_statics["followers"]=int(data_user_statics[0])
user_statics["following"]=int(data_user_statics[1])
user_statics["designs"]=int(data_user_statics[2])
user_statics["collections"]=int(data_user_statics[3])
user_statics["makes"]=int(data_user_statics[4])
user_statics["likes"]=int(data_user_statics[5])

print user_statics
#user_statics={"followers":0,"following":0,"designs":0,"collections":0,"makes":0,"likes":0}


#user_likes=int(likes.text())
#print n_likes

#<span class="box-count">777</span>


#Selection of data date
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
		event_link[x]="http://www.thingiverse.com"+str(event_link[x])
		print event_link[x]




#<a href="/thing:1183298" class="thing-img-wrapper">
#print raw_data


#raw_data=date_data.html()#solo coge el primer objeto...



'''
<div class="thing thing-interaction-parent" data-type="Thing" data-id="1374672" data-thing-id="1374672" title="A Box for Carcassonne's river extension">

	<div class="row-fluid">
				<a href="/thing:1374672" class="thing-img-wrapper">
                        <img class="thing-img" src="https://thingiverse-production-new.s3.amazonaws.com/renders/0c/10/64/1b/66/aee366d3cbf50f1d4a86fcba992b5743_preview_card.JPG">
            		</a>

		<div class="thing-about">
			<div class="profile-pic">
				<div class="profile-img-wrapper">
					<a href="/laurent_despeyroux"><img src="https://thingiverse-production-new.s3.amazonaws.com/renders/20/99/c9/dc/20/moi-bicolor_thumb_tiny.jpg" alt="" class="render"></a>				</div>
							</div>

			<span class="thing-who-what">
				<span class="thing-made">
					<span class="thing-name">A Box for Carcassonne's river extension</span>
											<span class="creator-name">by <a href="/laurent_despeyroux">laurent_despeyroux</a></span>
									</span>
			</span>
			<span class="thing-pub-time">
									23 mins ago							</span>
		</div>

		<div class="thing-interact">
												<span class="thing-like active" title="Unlike this Thing">
						<span class="interaction-count">1</span>
					</span>

                                                <span class="thing-collect" title="Collect this Thing">
                        <span class="interaction-count collection-count">0</span>
                    </span>

			<a href="/thing:1374672/#comments" class="thing-comment" title="View Comments">
				<span class="interaction-count comment-count">0</span>
			</a>
		</div>


					<form class="collect-form">
		<h2>Select a collection</h2>
		<h3>or create a new one below:</h3>

		<select name="collection">
												<option value="4947705" selected="selected">
						gopro					</option>
									<option value="4713370">
						pololu motors					</option>
									<option value="4861997">
						Screws					</option>
									<option value="5210">
						Things to Make					</option>
										<option value="-1" class="create-new-collection">- Create a new collection -</option>
		</select>

		<div class="new-collection-name">
			<input type="text" name="new-collection-name" placeholder="Enter new collection name">
		</div>

		<input type="hidden" name="thing_id" value="1374672">

		<button class="collection-save">Save</button>
		<button class="collection-cancel">Cancel</button>
	</form>



			</div>

</div>

'''

#no2data = map(int, no2data) #int conversion
#for data in date_data:
#    print (data)

#print(raw_data)
