import requests
import json
import os
from bs4 import BeautifulSoup
from scraping import utils
from datetime import datetime

from scraping.utils import print_log


def atmospheric_resources_data_to_json(soup: BeautifulSoup):
    print("     ✅ Lancement du script principal process_atmospheric_resources.py")
    ENDPOINT_ATMOSPHERIC_RESOURCE = utils.get_env("ENDPOINT_ATMOSPHERIC_RESOURCE")
    print("ENDPOINT_ATMOSPHERIC_RESOURCE")
    print(ENDPOINT_ATMOSPHERIC_RESOURCE)
    
    atmospheric_resources_data = utils.get_between(soup, "#Ressources_atmosphériques", "#Ressources_Composées", "dd")
    atmospheric_resources = []
    for element in atmospheric_resources_data:
        icon_data = element.select_one("a:has(img)")
        img = icon_data.select_one("img")
        atmospheric_resource = {
            "text" : element.get_text(separator='', strip=True),
            "icon_data" : element.select_one("a:has(img)"),
            "title" : icon_data.get("title") if icon_data else None,
            "img_src": img.get("src") if img else None,
            "icon_data_src" : img.get("data-src") if img else None
        }   
        atmospheric_resources.append(atmospheric_resource)
        
    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    utils.create_json_file (dir_name=script_dir, dataset_name="atmospheric_resources", json_data=atmospheric_resources)   
    
    # On envoie le JSON au service REST
    headers = {"Content-Type": "application/json"}
    #response = requests.post(ENDPOINT_ATMOSPHERIC_RESOURCE, json=atmospheric_resources, headers=headers)

    # On checke la réponse
    #print("Status:", response.status_code)
    #print("Response:", response.text)
    
print("     ✅ Fin du script principal process_atmospheric_resources.py")
