# This file will get the images from teh website IGCD

from bs4 import BeautifulSoup
from requests import get as rget
from time import sleep
from tqdm import tqdm
import json
import urllib.parse


def get_all_links(season_number):
    """
    Returns:
        list: the list of full urls
    """
    url = 'http://realitypoint.com/Data/The%20Big%20Bang%20Theory%20Season%20' + \
        season_number+'.html'
    response = rget(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    list_of_URLs = []
    for link in soup.find_all('a'):
        link = link.get('href')
        if ('S0' in link):
            # Add encoded URL to the list
            list_of_URLs.append(link.replace(' ', '%20'))

    return list_of_URLs


def get_image_from_url_and_save(url):
    response = rget(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_link = 'https://www.igcd.net/' + \
        soup.findAll(attrs={'class': 'VehiclePicture'})[0].get('src')
    img_data = rget(image_link).content
    with open('images/'+image_link.split('/')[-1], 'wb') as handler:
        handler.write(img_data)


def get_all_video_links(season_number):

    def get_video_link(link):
        return 'http://realitypoint.com:88/media/TV%20Shows/TV%20Comedy/The%20Big%20Bang%20Theory/Season%20'+season_number+'/' \
            + link.split('http://realitypoint.com/HTML/')[1].replace('.html', '.mp4')

    urls = get_all_links(season_number)

    video_links = []

    for link in tqdm(urls):
        # sleep(1)
        video_links.append(get_video_link(link))

    return {
        'season': 'S'+season_number,
        'links': video_links
    }


seasons = ['3', '4', '5', '6', '7', '8', '9']
final_list = []
for season in tqdm(seasons):
    sleep(1)
    final_list.append(get_all_video_links(season))

jsonString = json.dumps(final_list)
jsonFile = open("data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
