from bs4 import BeautifulSoup
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

from scraping import utils


def planets_data_to_json(soup: BeautifulSoup):
    # On récupère le endpoint pour l'envoi des données
    ENDPOINT_PLANET = utils.get_env("ENDPOINT_PLANET")
    # On extrait les données qui nous intéresse dans l'extraction BeautifulSoup
    table_rows = (
        soup.find("span", {"id": "Liste_des_planètes"})
            .find_parent("h2")
            .find_next("table")
            .find_all("tr")
    )
    
    # On construit le tableau des planète à partir des données extraites
    planets = []
    for tr in table_rows[1:]:  # sauter l'entête
        #data = [td.get_text(separator=";", strip=True) for td in tr.select("th, td")]       
        data = []
        for index, td in enumerate (tr.select("th, td")):
            data.append(td.get_text(separator=";", strip=True))
            # cas particulier du core symbol
            if (index == 8) :
                icon_data = td.select_one("a:has(img)")
                img = icon_data.select_one("img")
                core_symbol = img.get("data-src")
        if not data:
            continue
        planet = {
            "name": data[0] if len(data) > 0 else None,
            "type": data[1] if len(data) > 1 else None,
            "primary_resource": data[2] if len(data) > 2 else None,
            "secondary_resource": data[3] if len(data) > 3 else None,
            "atmosphere": data[4] if len(data) > 4 else None,
            "difficulty": data[5] if len(data) > 5 else None,
            "solar_power": data[6] if len(data) > 6 else None,
            "wind_power": data[7] if len(data) > 7 else None,
            "core_symbol_url": core_symbol,
            "core_material": data[9] if len(data) > 9 else None
        }
        planets.append(planet)

    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    utils.create_json_file (dir_name=script_dir, dataset_name="planets", json_data=planets)
    
    # On envoie le JSON au service REST
    headers = {"Content-Type": "application/json"}
    #response = requests.post(ENDPOINT_PLANET, json=planets, headers=headers)
    # On checke la réponse
    #print("Status:", response.status_code)
    #print("Response:", response.text)
    
    return planets
   


