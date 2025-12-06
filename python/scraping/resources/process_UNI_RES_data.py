import csv
from bs4 import BeautifulSoup
from scraping import utils

import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime


def UNI_RES_data_to_json(soup: BeautifulSoup):
    print("     ✅ Lancement du script process_UNI_RES_data.py")

    UNI_RES = []
    start = soup.select_one("#Other_Resources")
    if start:
        table = start.find_next("dl")
        if table:
            rows = table.find_all("dd") 
            for row in rows:
                resource_name = row.get_text(strip=True)
                icon = row.find("img")
                icon_url = icon.get("data-src") if icon else None

                # on stocke les données dans un tableau
                UNI_RES.append({
                    "name": resource_name,
                    "icon_url": icon_url})

            
        script_dir = os.path.dirname(os.path.abspath(__file__)) 
        utils.create_json_file (dir_name=script_dir, dataset_name="UNI_RES", json_data=UNI_RES)         
        
        # On envoie le JSON au service REST
        headers = {"Content-Type": "application/json"}
        #response = requests.post(ENDPOINT_UNI_RES, json=UNI_RES, headers=headers)

        # On checke la réponse
        #print("Status:", response.status_code)
        #print("Response:", response.text)
    