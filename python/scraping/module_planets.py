from bs4 import BeautifulSoup
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
#
from scraping import utils


def main ():
    utils.print_log("[>] Données Planets",0)
    # URLs
    url_planet = utils.get_env("host") + utils.get_env("planet_path") 
    endpoint_planet = utils.get_env("api_endpoint") + utils.get_env("api_module_planet") 
   
    # on récupère les données planet sous forme de json
    planets_data = get_planets_data(url_planet)
    if planets_data:
        # export json
        script_dir = os.path.dirname(os.path.abspath(__file__)) 
        utils.create_json_file (dir_name=script_dir, dataset_name="planet", json_data=planets_data)
        # envoie à apex
        if endpoint_planet:
            utils.print_log("[>] Données Planets",3)
            utils.post_json(endpoint_planet, planets_data)
    return "ok"
    
def get_planets_data(url_planet):
    soup = utils.get_soup(url_planet)
    if soup:
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
                    return planets
    return None
                        
# --- Orchestration ---
if __name__ == "__main__":
    main()


