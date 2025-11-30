import csv
from bs4 import BeautifulSoup
import scraping.utils.utils as utils

def planet_resources_data_to_csv(soup: BeautifulSoup):
    print("     ✅ Lancement du script process_resources_planet_data.py")
    # On récupére la table ciblée
    planet_resources_data_table = utils.get_table_by_first_th(soup, "Ressource")

    # En-tête
    data = []
    # Extraire les lignes si la table existe
    if planet_resources_data_table is not None:
        for tr in planet_resources_data_table.find_all("tr"):
            cells = tr.find_all(["th", "td"])
            row = [el.get_text(strip=True) for el in cells]
            if row:  
                data.append(row)

    # Export en CSV
    utils.export_csv(r"scraping\data\planet_resources.csv", data, ";")

    print("✅ Scraping terminé, fichier planet_resources.csv généré")

