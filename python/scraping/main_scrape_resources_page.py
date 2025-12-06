from scraping import utils
from scraping.utils import print_log
from scraping.resources import process_ATMO_RES_data
from scraping.resources import process_NAT_RES_data
from scraping.resources import process_UNI_RES_data
from scraping.resources import process_COMP_RES_data
from scraping.resources import process_UNI_RES_data


# URL
URL = "https://astroneer.fandom.com/wiki/Resources"


# --- Orchestration ---
def main():
    print_log("✅ Lancement du script principal main_scrap_resources_page.py", 0)
    # Parsing avec BeautifulSoup
    soup = utils.get_soup(URL)
    if soup:
        process_ATMO_RES_data.ATMO_RES_data_to_json(soup)
        process_COMP_RES_data.COMP_RES_data_to_json(soup)
        process_NAT_RES_data.NAT_RES_data_to_json(soup)
        #process_UNI_RES_data.REF_RES_data_to_json(soup)
        #process_UNI_RES_data.UNI_RES_data_to_json(soup)

        
    print_log("✅ Fin du script principal main_scrap_resources_page.py", 0)
    print_log("✅ Fin du script principal main_scrap_resources_page.py")

if __name__ == "__main__":
    main()
    