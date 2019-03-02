import json
import requests
import sys
from datetime import datetime
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from skimage import io
import webcolors


def find_RGB(imageUrl):
	img = io.imread(imageUrl)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
	clt = KMeans(n_clusters=3) #cluster number
	clt.fit(img)
	rgb = clt.cluster_centers_
	rgbLst = []
	for item in rgb:
		rgbLst.append(list(item))
	return rgbLst



def closest_colour(requested_colour):
    min_colours = {}
    count = 0
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = key
    return min_colours[min(min_colours.keys())]





whole_dict ={}

with open('sampleResult2.json', 'w') as f:
	for i in range(100):
		url = 'https://www.behance.net/v2/projects?field=illustration&api_key=bWcjs1ixeYPvzVoK0bgAMgNzL21ZtOWI&page=%{}'.format(i)

		resp = requests.get(url)
		data = json.loads(resp.text)


		init = data['projects']

		for project in init:

			whole_dict[project['id']] = []
			whole_dict[project['id']].append({'name' : project['name']})
			whole_dict[project['id']].append({'fields': project['fields']})
			# whole_dict[project['id']].append({'owners': project['owners']})
			# whole_dict[project['id']].append({'stats': project['stats']})

			timedict = {}
			timeCreated = datetime.fromtimestamp(project['created_on'])	
			timestr = timeCreated.__str__()
			timelst = timestr.split(' ')[0].split('-')
			timedict['year'] = timelst[0]
			timedict['month'] = timelst[1]
			timedict['date'] = timelst[2]


			whole_dict[project['id']].append({'timeCreated': timedict})


			imageUrl = project['covers']['115']
			rgbLst = []
			rgbLst.append(closest_colour(find_RGB(imageUrl)[0]))
			rgbLst.append(closest_colour(find_RGB(imageUrl)[1]))
			rgbLst.append(closest_colour(find_RGB(imageUrl)[2]))



			whole_dict[project['id']].append({'color': rgbLst})


			project_owner = project['owners'][0]
			owners = {}
			owners['first_name'] = project_owner['first_name']
			owners['last_name'] = project_owner['last_name']
			owners['location'] = [project_owner['city']]
			owners['location'].append(project_owner['state'])
			owners['location'].append(project_owner['country'])
			whole_dict[project['id']].append({'owners': owners})


			project_stats = project['stats']
			stats = {}
			stats['views'] = project_stats['views']
			stats['appreciations'] = project_stats['appreciations']
			whole_dict[project['id']].append({'stats': stats})
			







	dumped = json.dumps(whole_dict)
	f.write(dumped)








