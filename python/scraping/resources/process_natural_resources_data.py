import csv
from bs4 import BeautifulSoup
from scraping import utils

import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime


def natural_resources_data_to_json(soup: BeautifulSoup):
    print("     ✅ Lancement du script process_natural_resources_data.py")
    #natural_resources_data = soup.select_one(":nth-child(1)")
    natural_resources_data = utils.get_between(soup, "#Ressources_Naturelles", "table", "dd")
    
    natural_resources = []
    for element in natural_resources_data:
        #print (element)
        icon_data = element.select_one("a:has(img)")
        img = icon_data.select_one("img")
        natural_resource = {
            "text" : element.get_text(separator="", strip=True),
            "title" : icon_data.get("title") if icon_data else None,
            "img_src": img.get("src") if img else None,
            "icon_data_src" : img.get("data-src") if img else None
        }
        natural_resources.append(natural_resource)

    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    utils.create_json_file (dir_name=script_dir, dataset_name="natural_resources", json_data=natural_resources)
    # On envoie le JSON au service REST
    headers = {"Content-Type": "application/json"}
    #response = requests.post(ENDPOINT_NATURAL_RESOURCE, json=natural_resources, headers=headers)

    # On checke la réponse
    #print("Status:", response.status_code)
    #print("Response:", response.text)
    
print("     ✅ Script process_natural_resources_data.py terminé")
