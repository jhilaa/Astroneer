from bs4 import BeautifulSoup
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urljoin
#
from scraping import utils


CATEGORY_SUFFIXE = [
    #":Small",
    #":Medium",
    #":Large",
    ":Extra_Large"
]

def main (): 
    utils.print_log("[>] Données Items",0)
    # URLs
    item_endpoint = urljoin(utils.get_env("api_endpoint"), "item")
    items_data_src = urljoin(utils.get_env("domain"), utils.get_env("items_path"))
    urls_items_list = [
        f"{items_data_src}{suffix}" for suffix in CATEGORY_SUFFIXE
    ]
    
    items_list = []
    items_data = []
    for url_items_list in urls_items_list: 
        items_list.extend (get_items_list(url_items_list))
    
    if len (items_list)>0 :
        items_data = get_items_data (items_list)
        
    if (len(items_data) > 0):
        # export json
        script_dir = os.path.dirname(os.path.abspath(__file__)) 
        utils.create_json_file (dir_name=script_dir, dataset_name="item", json_data=items_data)
        #
        utils.post_json(item_endpoint, items_data)

def get_items_list(items_list_url):
    soup = utils.get_soup(items_list_url)
    if soup:
        # On extrait les données qui nous intéressent dans l'extraction BeautifulSoup
        start = soup.find("div", {"id": "mw-pages"})
        if start:
            rows = start.find_all("li")
            if rows :
                # on va construire le tableau des équipements
                items_list = []                
                for row in rows: 
                    link = row.find("a")
                    item = {
                        "title": link.get("title") if link else None,
                        "name": row.get_text(strip=True),
                        "url": link.get("href") if link  else None,
                    }
                    items_list.append(item)
                return items_list
    return None

def get_items_data (items_list):
    items_data=[]
    if len (items_list)>0 :
        cpt=0
        for item in items_list:
            item_url = urljoin(utils.get_env("domain"), item.get("url"))
            item_data = get_item_data(item_url)  
            if item_data:
                items_data.append(item_data)
                cpt += 1
                print (f"{cpt}/{len (items_list)}")
    return items_data
 
    
def get_item_data (item_url):
    item_data = None
    img_src_url = None
    icon_src_url = None
    title = None
    name = None
    if item_url:
        soup = utils.get_soup(item_url)
        if soup:
            start = soup.select_one("table.infoboxtable")
            if start :
                headers = [tr for tr in start.select("tr") if not tr.find("td")]
                if headers :
                    title_zone = headers[0].select_one("span[title]") if len(headers) > 0  else None
                    title = title_zone.get("title") if title_zone is not None else None
                    name = headers[0].get_text(strip=True) if len(headers) > 0 else None
                    icon = headers[0].find("img") if len(headers) > 0 else None
                    if icon:
                        if icon.get("data-src") is not None:
                            icon_src_url = icon.get("data-src")
                        elif icon.get("src") is not None:
                            icon_src_url = icon.get("src")
                        else:
                            icon_src_url = None
                    else:
                        icon_src_url = None
                    img = headers[1].find("img") if len(headers) > 1 else None
                    if img:
                        if img.get("data-src") is not None:
                            img_src_url = img.get("data-src")
                        elif img.get("src") is not None:
                            img_src_url = icon.get("src")
                        else:
                            img_src_url = None
                  
                row_data = data = {
                    tr.find("th").get_text(strip=True): tr.find("td").get_text(strip=True)
                    for tr in soup.find_all("tr")
                    if tr.find("th") and tr.find("td")
                }
                
                item_data = {
                        "url" : item_url,
                        "title" : title,
                        "name" : name,
                        "icon_src_url" : icon_src_url,
                        "img_src_url" : img_src_url,
                        "tier" : row_data.get("Tier"),
                        "group" : row_data.get("Group"),           
                        "type" : row_data.get("Type") , 
                        "crafted_at" : row_data.get("Crafted at"),
                        "recipe" : row_data.get("Recipe"),
                        "unlock_cost" : row_data.get("Unlock Cost") }
    return item_data      
   
                        
# --- Orchestration ---
if __name__ == "__main__":
    main()

