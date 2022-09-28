# This file will get the images from teh website IGCD

from bs4 import BeautifulSoup
from requests import get as rget
from time import sleep
from tqdm import tqdm
import json
import urllib.parse
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth()
drive = GoogleDrive(gauth)


def get_price():
    url = 'https://andelenergi.dk/kundeservice/aftaler-og-priser/timepris/'
    response = rget(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # get the data used to create the chart
    data = json.loads(soup.select('#chart-component')[0].get("data-chart"))
    # grab west data
    data['west']
    # append data to existing database
    # upload to drive
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(
        '1cIMiqUDUNldxO6Nl-KVuS9SV-cWi9WLi')}).GetList()

    print(file_list)

    # list_of_URLs = []
    # for link in soup.find_all('#chart-current-price'):
    #     link = link.get('href')
    #     if ('S0' in link):
    #         # Add encoded URL to the list
    #         list_of_URLs.append(link.replace(' ', '%20'))

    # return list_of_URLs


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


get_price()
# final_list = []
# for season in tqdm(seasons):
#     sleep(1)
#     final_list.append(get_all_video_links(season))

# jsonString = json.dumps(final_list)
# jsonFile = open("data.json", "w")
# jsonFile.write(jsonString)
# jsonFile.close()
