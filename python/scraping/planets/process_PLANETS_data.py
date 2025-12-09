from bs4 import BeautifulSoup
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

from scraping import utils

def PLANETS_data_to_json(soup: BeautifulSoup):
    print("    [OK]  Lancement du script principal process_PLANETS_DATA.py")
    ENDPOINT_PLANET = utils.get_env("ENDPOINT_PLANET")
    
    # On extrait les données qui nous intéresse dans l'extraction BeautifulSoup
    start = soup.find("span", {"id": "Planets"})
    if start:
        h2 = start.find_parent("h2")
        if h2 :
            table = h2.find_next("table")
            if table:    
                rows = table.find_all("tr")
                # on va construire le tableau des planetes
                planets = []                
                for tr in rows[1:]:  # sauter l'entête
                    planet_data = []
                    for index, td in enumerate (tr.select("th, td")):
                        planet_data.append(td.get_text(separator=";", strip=True))
                        # cas particulier du core symbol
                        if (index == 9) :
                            icon_data = td.select_one("a:has(img)")
                            img = icon_data.select_one("img")
                            core_symbol = img.get("data-src")
                    if not planet_data:
                        continue
                    planet = {
                        "name": planet_data[0] if len(planet_data) > 0 else None,
                        "type": planet_data[1] if len(planet_data) > 1 else None,
                        "primary_resource": planet_data[2] if len(planet_data) > 2 else None,
                        "secondary_resource": planet_data[3] if len(planet_data) > 3 else None,
                        "atmosphere": planet_data[4] if len(planet_data) > 4 else None,
                        "difficulty": planet_data[5] if len(planet_data) > 5 else None,
                        "solar_power": planet_data[6] if len(planet_data) > 6 else None,
                        "wind_power": planet_data[7] if len(planet_data) > 7 else None,
                        "gateway_chamber_power_required": planet_data[8] if len(planet_data) > 8 else None,
                        "core_symbol_url": core_symbol,
                        "core_material": planet_data[10] if len(planet_data) > 10 else None
                    }
                    planets.append(planet)

            script_dir = os.path.dirname(os.path.abspath(__file__)) 
            utils.create_json_file (dir_name=script_dir, dataset_name="PLANET", json_data=planets)
            
            try:
                url = ENDPOINT_PLANET
                headers = {
                  'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=json.dumps(planets))

            except Exception as e:
                print("Erreur :", e)
                
               