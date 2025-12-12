from bs4 import BeautifulSoup
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urljoin
#
from scraping import utils

# codes branchs
ATMRES_BRANCH = "atmres"
ATMRESRATE_BRANCH = "atmresrate"
COMPRES_BRANCH = "compres"
NATRES_BRANCH = "natres"
NATRESRATE_BRANCH = "natresrate"
REFRES_BRANCH = "refres"

def main (): 
    utils.print_log("[>] Données Resources",0)
    # URLs
    resources_data_src = urljoin(utils.get_env("domain"),utils.get_env("resources_path")) 
    
    # point d'api par branch
    resource_api = {
        ATMRES_BRANCH: "atmores",
        ATMRESRATE_BRANCH: "atmoresrate",
        COMPRES_BRANCH: "compres",
        NATRES_BRANCH: "natres",
        NATRESRATE_BRANCH: "natresrate",
        REFRES_BRANCH: "refres",
     }
    # récupération de tous les types de ressources + génération json + envoi REST 
    resources_data = get_resources_data (resources_data_src)
    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    if resources_data: 
        for branch, data in resources_data.items():
            utils.create_json_file (dir_name=script_dir, dataset_name=branch, json_data=data)
            #
            branch_endpoint = urljoin(utils.get_env("api_endpoint"),branch)
            print("branch_endpoint ----------")
            print(branch_endpoint)
            utils.print_log("[>] Envoi des données",1)
            utils.post_json(branch_endpoint, data)
    return "ok"       
    
def get_resources_data (resources_data_src):
    soup = utils.get_soup(resources_data_src)
    if soup: 
        return (get_atmres(soup)  # atmres et atmresrate
              | get_compres(soup)
              | get_natres(soup)  # natres et natresrate
              | get_refres(soup))
    return None

def get_atmres(soup):
    atmo_res_data = []
    atmo_res_rate_data = []
    start = soup.select_one("#Atmospheric_Resources")
    if start:
        table = start.find_next("table")
        if table:
            print(" 1")
            rows = table.find_all("tr")  
            # On extrait les noms de planètes depuis l'entête
            planet_names = [th.get_text(strip=True) for th in rows[0].find_all("th")[1:]]
            for row in rows[1:]:
                cells = row.find_all("td")
                resource_name = cells[0].get_text(strip=True)
                icon = cells[0].find("img")
                icon_url = icon.get("data-src") if icon else None
                
                # Données référentielles
                atmo_res_data.append({
                    "name": resource_name,
                    "icon_url": icon_url})
                # Données par planète
                for i, cell in enumerate(cells[1:]):
                    rate = cell.get_text(strip=True)
                    atmo_res_rate_data.append ({
                        "resource_name" : resource_name,
                        "planete": planet_names[i],
                        "taux": rate})
        return {ATMRES_BRANCH:atmo_res_data,
                 ATMRESRATE_BRANCH:atmo_res_rate_data}
    print(" xxx")
    return None

def get_compres(soup):
    comp_res = []
    start = soup.select_one("#Composite_Resources")
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

               comp_res.append ({
                   "name" : resource_name,
                   "icon_url" : icon_url,
                   "resource_1_name" : resource_1_name,
                   "resource_2_name" : resource_2_name,
                   "gaz_name" : gaz_name
               })          
       return {COMPRES_BRANCH :comp_res}          
    return None
    
def get_natres (soup):
    nat_res_data = []
    nat_res_rate_data = []
    start = soup.select_one("#Natural_Resources")
    if start:
        table = start.find_next("table")
        if table:
            rows = table.find_all("tr") 
            # On extrait les noms de planètes depuis l'entête
            planet_names = [th.get_text(strip=True) for th in rows[0].find_all("th")[1:-1]]
            
            # On saute la 1ère ligne
            for row in rows[1:]:
                cols = row.find_all("td")[:-1]
                # Données référentielles dans la 1ère colonne
                resource_name = cols[0].get_text(strip=True)
                icon = cols[0].find("img")
                icon_url = icon.get("data-src") if icon else None
                nat_res_data.append({
                    "name": resource_name,
                    "icon_url": icon_url})
                    
                # Données par planète
                for i, col in enumerate(cols[1:]):
                    concentration = col.get_text(strip=True)
                    nat_res_rate_data.append ({
                        "resource_name" : resource_name,
                        "planete": planet_names[i],
                        "taux": concentration})
           
        return {NATRES_BRANCH:nat_res_data,
                 NATRESRATE_BRANCH:nat_res_rate_data}
    return None
    
def get_refres(soup):
    ref_res = []
    start = soup.select_one("#Refined_Resources")
    if start:
        table = start.find_next("table")
        if table:
            rows = table.find_all("tr")
            for row in rows[1:]:
                cells = row.find_all("td")
                icon = cells[0].find("img")
                resource_name = cells[0].get_text(strip=True)
                icon_url = icon.get("data-src") if icon else None
                raw_resource_name = cells[1].get_text(strip=True)  

                ref_res.append ({
                    "name" : resource_name,
                    "icon_url" : icon_url,
                    "raw_resource_name" : raw_resource_name
                })           
        return {REFRES_BRANCH:ref_res}          
    return None
    
    

if __name__ == "__main__": 
    main()
    