import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urlunsplit
from pprint import pprint

REQUEST_TIMEOUT = 5
FOLDER_LOCATION = '/mnt/Portable/TV\ Series/Utopia'

def get_seasons(url):
    # Step 1: Get a webpage HTML and extract the body

    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    html = response.text

    # Step 2: Parse the HTML and extract <a> elements
    soup = BeautifulSoup(html, 'html.parser')
    a_elements = soup.find_all('a')

    # Step 3: Convert <a> elements to YAML
    yaml_data = []
    for a in a_elements:
        link_data = {
            'href': a.get('href'),
            'text': a.text.strip(),
        }
        yaml_data.append(link_data)

    return yaml_data

def get_episodes(url):
    response = requests.get(url[:-1], timeout=REQUEST_TIMEOUT)

    html = response.text

    # Step 2: Parse the HTML and extract <a> elements
    soup = BeautifulSoup(html, 'html.parser')
    a_elements = soup.find_all('a')

    # Step 3: Convert <a> elements to YAML
    yaml_data = []
    for a in a_elements:
        link_data = {
            'href': a.get('href'),
            'text': a.text.strip(),
        }
        yaml_data.append(link_data)

    return yaml_data


if __name__ == "__main__":
    return_data = {}

    url = "http://ftp.timepassbd.live/timepassbd-data/ftp3/TV_SERIES/ENGLISH_TV_SERIES/U/Utopia%20%282013-2014%29"  # Replace with the URL of the webpage you want to scrape
    split_url = urlsplit(url)

    scheme =  split_url.scheme  
    location = split_url.netloc  


    seasons = get_seasons(url)

    for dir in filter(lambda x: 'timepassbd-data' in x['href'], seasons):
        # Step 1: Get a webpage HTML and extract the body
        url = f'{scheme}://{location}/{dir["href"]}'
        episode = get_episodes(url)
        return_data[dir.get('text').strip()] = episode

    with open("script1.sh", "w+") as file:
        file.write(f"#!/bin/bash\n\n")
        file.write(f"mkdir -p {FOLDER_LOCATION}\n")
        file.write(f"cd {FOLDER_LOCATION}\n")

        for season in return_data.keys():
            file.write(f"mkdir -p '{season}'\n")
            file.write(f"cd '{season}'\n")

            for episode in filter(lambda x: 'timepassbd-data' in x['href'], return_data[season]):
                file.write(f"wget {scheme}://{location}/{episode['href']}\n")

            file.write(f"cd ..\n")






    


