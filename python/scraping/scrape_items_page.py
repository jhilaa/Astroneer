import os
from scraping import utils
from scraping.utils import print_log
from scraping.items import process_items_data


# URL
BASE_URL = utils.get_env("BASE_URL")

# --- Orchestration ---
def main():
    print_log(" [>] Lancement du script principal main_scrap_ITEMS_page.py", 0)
    # Parsing avec BeautifulSoup
    process_items_data.items_data_to_json("small")
    print_log("[>] Fin du script principal scrap_items_page.py", 0)

if __name__ == "__main__":
    main()
    