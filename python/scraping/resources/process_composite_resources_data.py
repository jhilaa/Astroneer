import requests
import json
import os
from bs4 import BeautifulSoup
from scraping import utils
from datetime import datetime


def composite_resources_data_to_json(soup: BeautifulSoup):
    print("     ✅ Lancement du script process_composite_resources_data.py")
    
    composite_resources = []
    start = soup.select_one("#Ressources_Composées")
    if start:
        table = start.find_next("table")
        if table:
            rows = table.find_all("tr")
            for row in rows[1:]:
                cells = row.find_all("td")
                icon = cells[0].find("img")               
                resource_name = cells[0].get_text(strip=True)
                icon_data_src = icon.get("data-src") if icon else None
                resource_1_name = cells[1].get_text(strip=True)
                resource_2_name = cells[2].get_text(strip=True)  
                gaz_name = cells[3].get_text(strip=True)  

                composite_resources.append ({
                    "name" : resource_name,
                    "icon_data_src" : icon_data_src,
                    "resource_1_name" : resource_1_name,
                    "resource_2_name" : resource_2_name,
                    "gaz_name" : gaz_name
                })
                
            script_dir = os.path.dirname(os.path.abspath(__file__)) 
            utils.create_json_file (dir_name=script_dir, dataset_name="composite_resources", json_data=composite_resources)   
            
            # On envoie le JSON au service REST
            headers = {"Content-Type": "application/json"}
            #response = requests.post(ENDPOINT_composite_RESOURCE, json=composite_resources, headers=headers)

            # On checke la réponse
            #print("Status:", response.status_code)
            #print("Response:", response.text)
    
