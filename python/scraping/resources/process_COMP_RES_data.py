import requests
import json
import os
from bs4 import BeautifulSoup
from scraping import utils
from datetime import datetime


def COMP_RES_data_to_json(soup: BeautifulSoup):
    print("     ✅ Lancement du script process_COMP_RES_data.py")
    
    COMP_RES = []
    start = soup.select_one("#Ressources_Composées")
    if start:
        table = start.find_next("table")
        if table:
            rows = table.find_all("tr")
            for row in rows[1:]:
                cells = row.find_all("td")
                icon = cells[0].find("img")               
                resource_name = cells[0].get_text(strip=True)
                icon_url = icon.get("data-src") if icon else None
                resource_1_name = cells[1].get_text(strip=True)
                resource_2_name = cells[2].get_text(strip=True)  
                gaz_name = cells[3].get_text(strip=True)  

                COMP_RES.append ({
                    "name" : resource_name,
                    "icon_url" : icon_url,
                    "resource_1_name" : resource_1_name,
                    "resource_2_name" : resource_2_name,
                    "gaz_name" : gaz_name
                })
                
            script_dir = os.path.dirname(os.path.abspath(__file__)) 
            utils.create_json_file (dir_name=script_dir, dataset_name="COMP_RES", json_data=COMP_RES)   
            
            # On envoie le JSON au service REST
            headers = {"Content-Type": "application/json"}
            #response = requests.post(ENDPOINT_COMP_RES, json=COMP_RES, headers=headers)

            # On checke la réponse
            #print("Status:", response.status_code)
            #print("Response:", response.text)
    
