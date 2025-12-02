import csv
from bs4 import BeautifulSoup
from scraping import utils

import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime


def NAT_RES_data_to_json(soup: BeautifulSoup):
    print("     ✅ Lancement du script process_NAT_RES_data.py")

    NAT_RES = []
    NAT_RES_concentration = []
    start = soup.select_one("#Ressources_Naturelles")
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
                NAT_RES.append({
                    "name": resource_name,
                    "icon_url": icon_url})
                # Données par planète
                for i, cell in enumerate(cells[1:]):
                    concentration = cell.get_text(strip=True)
                    NAT_RES_concentration.append ({
                        "resource_name" : resource_name,
                        "planete": planet_names[i],
                        "taux": concentration})
               

        script_dir = os.path.dirname(os.path.abspath(__file__)) 
        # Données référentielles
        utils.create_json_file (dir_name=script_dir, dataset_name="NAT_RES", json_data=NAT_RES)         
        # Données par planète
        utils.create_json_file (dir_name=script_dir, dataset_name="NAT_RES_RATE", json_data=NAT_RES_RATE)   
         # On envoie le JSON au service REST
        headers = {"Content-Type": "application/json"}
        #response = requests.post(ENDPOINT_NAT_RES, json=NAT_RES, headers=headers)

        # On checke la réponse
        #print("Status:", response.status_code)
        #print("Response:", response.text)
    