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
    
    atmospheric_resources = []
    start = soup.select_one("#Ressources_atmosphériques")
    if start:
        table = start.find_next("table")
        if table:
            rows = table.find_all("tr")  
            # On extrait les noms de planètes depuis l'entête
            planet_names = [th.get_text(strip=True) for th in rows[0].find_all("th")[1:]]
            for row in rows[1:]:
                cells = row.find_all("td")
                resource_name = cells[0].get_text(strip=True)
                icon = cells[0].find("img")
                icon_data_src = icon.get("data-src") if icon else None

                planet_concentration_data = []
                for i, cell in enumerate(cells[1:]):
                    concentration = cell.get_text(strip=True)
                    planet_concentration_data.append({"planete": planet_names[i], "taux": concentration})

                atmospheric_resources.append({
                    "name": resource_name,
                    "icon_data_src": icon_data_src,
                    "concentration": planet_concentration_data})
                
            script_dir = os.path.dirname(os.path.abspath(__file__)) 
            utils.create_json_file (dir_name=script_dir, dataset_name="atmospheric_resources", json_data=atmospheric_resources)   
            
            # On envoie le JSON au service REST
            headers = {"Content-Type": "application/json"}
            #response = requests.post(ENDPOINT_ATMOSPHERIC_RESOURCE, json=atmospheric_resources, headers=headers)

            # On checke la réponse
            #print("Status:", response.status_code)
            #print("Response:", response.text)
    
