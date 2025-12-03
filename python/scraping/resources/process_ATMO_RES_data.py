import requests
import json
import os
from bs4 import BeautifulSoup
from scraping import utils
from datetime import datetime
import logging
import httpx

from scraping.utils import print_log



def ATMO_RES_data_to_json(soup: BeautifulSoup):
    logging.basicConfig(level=logging.DEBUG)
    print("     ✅ Lancement du script principal process_ATMO_RES.py")
    ENDPOINT_ATMO_RES = utils.get_env("ENDPOINT_ATMO_RES")
    #ENDPOINT_ATMO_RES = utils.get_env("ENDPOINT_ATMO_RES_RATE")
    
    ATMO_RES = []
    ATMO_RES_RATE = []
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
                icon_url = icon.get("data-src") if icon else None
                
                # Données référentielles
                ATMO_RES.append({
                    "name": resource_name,
                    "icon_url": icon_url})
                # Données par planète
                for i, cell in enumerate(cells[1:]):
                    rate = cell.get_text(strip=True)
                    ATMO_RES_RATE.append ({
                        "resource_name" : resource_name,
                        "planete": planet_names[i],
                        "taux": rate})
 
            script_dir = os.path.dirname(os.path.abspath(__file__)) 
            # ========================
            # DONNÉES RÉFÉRENTIELLES 
            # ========================
            # Création du fichier json (pour avoir une trace)
            utils.create_json_file (dir_name=script_dir, dataset_name="ATMO_RES", json_data=ATMO_RES)  
            print("step 2")
            # On envoie le JSON au service REST
            try:
                url = "https://oracleapex.com/ords/astroneer_wksp/rest/atmo_res"

                payload = [
                  {
                    "name": "Hydrogène",
                    "icon_url": "https://s"
                  }
                ]

                headers = {
                  "Content-Type": "application/json",
                  "Accept": "application/json"
                }
                

                response = httpx.post(url, json=payload, headers=headers, timeout=10, verify=False)
                print("Status:", response.status_code)
                print("Response:", response.text)
                print("Chunk:", next(response.iter_bytes()))

            except Exception as e:
                print("Erreur simple test:", e)
            
            """
            try:
                response1 = requests.post(
                    ENDPOINT_ATMO_RES,
                    headers = {"Content-Type": "application/json"},
                    json = ATMO_RES,
                    timeout = 10
                )
                print("Status:", response1.status_code)
                print("Body:", response1.text)
            except Exception as e:
                print("Erreur simple test:", e)

            """
            
            """
            # ========================
            # DONNÉES PAR PLANÈTE 
            # ========================
            # Création du fichier json (pour avoir une trace)
            utils.create_json_file (dir_name=script_dir, dataset_name="ATMO_RES_RATE", json_data=ATMO_RES_RATE)   
            # On envoie le JSON au service REST
         
            headers = {"Content-Type": "application/json"}
            response2 = requests.post(ENDPOINT_ATMO_RES_RATE, json=ATMO_RES_RATE, headers=headers)
            #print("Status:", response2.status_code)
            #print("Response:", response2.text)
            """
            
            
           
            
            
    
