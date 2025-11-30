from scraping import utils
from scraping.utils import print_log
from scraping.resources import process_atmospheric_resources_data
from scraping.resources import process_natural_resources_data
#from scraping.resources import process_planet_resources_data


# URL
URL = "https://astroneer.fandom.com/fr/wiki/Ressources"


# --- Orchestration ---
def main():
    print_log("✅ Lancement du script principal main_scrap_resources_page.py", 0)
    # Parsing avec BeautifulSoup
    soup = utils.get_soup(URL)
    if soup:
        process_atmospheric_resources_data.atmospheric_resources_data_to_json(soup)
        process_natural_resources_data.natural_resources_data_to_json(soup)

        
    print_log("✅ Fin du script principal main_scrap_resources_page.py", 0)
    print_log("✅ Fin du script principal main_scrap_resources_page.py")

if __name__ == "__main__":
    main()
    