from bs4 import BeautifulSoup
from scraping.planets import process_PLANETS_data
from scraping import utils


# URL
URL = "https://astroneer.fandom.com/wiki/Planets"

# --- Orchestration ---
def main():
    print("[OK] Lancement du script principal main_scrape_planets_page.py")
    # Parsing avec BeautifulSoup
    soup = utils.get_soup(URL)

    if soup:
        process_PLANETS_data.PLANETS_data_to_json(soup)
        
    print("[OK] Fin du script principal main_scrape_planets_page.py")

if __name__ == "__main__":
    main()


