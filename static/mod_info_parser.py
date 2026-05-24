from bs4 import BeautifulSoup
import requests
import re

def parse_by_link(link = None):
    
    if link == None: return False
    
    try: page = requests.get(link).text
    except: return False
    soup = BeautifulSoup(page,'html.parser')

    description_div = soup.find('div', class_='workshopItemDescription')
    div_text = description_div.get_text()

    split_div = div_text[div_text.find("Mod ID:"):].split()
    id_index = split_div.index("ID:")+1
    
    
    return split_div[id_index]

parse_by_link("https://steamcommunity.com/sharedfiles/filedetails/?id=2762018937")


