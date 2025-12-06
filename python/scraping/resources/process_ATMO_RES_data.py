import requests
import json
import os
from bs4 import BeautifulSoup
from scraping import utils
from datetime import datetime

from scraping.utils import print_log



def ATMO_RES_data_to_json(soup: BeautifulSoup):
    print("     ✅ Lancement du script principal process_ATMO_RES.py")
    ENDPOINT_ATMO_RES = utils.get_env("ENDPOINT_ATMO_RES")
    ENDPOINT_ATMO_RES_RATE = utils.get_env("ENDPOINT_ATMO_RES_RATE")
    
    ATMO_RES_DATA = []
    ATMO_RES_RATE_DATA = []
    start = soup.select_one("#Atmospheric_Resources")
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
                icon_url = icon.get("data-src") if icon else None
                
                # Données référentielles
                ATMO_RES_DATA.append({
                    "name": resource_name,
                    "icon_url": icon_url})
                # Données par planète
                for i, cell in enumerate(cells[1:]):
                    rate = cell.get_text(strip=True)
                    ATMO_RES_RATE_DATA.append ({
                        "resource_name" : resource_name,
                        "planete": planet_names[i],
                        "taux": rate})
 
            script_dir = os.path.dirname(os.path.abspath(__file__)) 
            # ========================
            # DONNÉES RÉFÉRENTIELLES 
            # ========================
         
            # Création du fichier json (pour avoir une trace)
            utils.create_json_file (dir_name=script_dir, dataset_name="ATMO_RES", json_data=ATMO_RES_DATA)  
            # On envoie le JSON au service REST
            try:
                url = ENDPOINT_ATMO_RES
                headers = {
                  'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=json.dumps(ATMO_RES_DATA))

            except Exception as e:
                print("Erreur :", e)
            
            # ========================
            # DONNÉES PAR PLANÈTE 
            # ========================
            # Création du fichier json (pour avoir une trace)
            utils.create_json_file (dir_name=script_dir, dataset_name="ATMO_RES_RATE", json_data=ATMO_RES_RATE_DATA)  
            # On envoie le JSON au service REST
            try:
                url = ENDPOINT_ATMO_RES_RATE
                headers = {
                  'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=json.dumps(ATMO_RES_RATE_DATA))
            except Exception as e:
                print("Erreur :", e)

            
            
           
            
            
    
