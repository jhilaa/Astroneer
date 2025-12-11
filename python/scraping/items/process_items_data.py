from bs4 import BeautifulSoup
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from scraping import utils

BASE_URL = utils.get_env("BASE_URL")


        
#1 appelé dans le script principal    
def items_data_to_json (category) :
    items_data = get_items_data (category) #2 récupère les données de tous les items d'un catégory donnée
    if items_data: 
        # export json
        script_dir = os.path.dirname(os.path.abspath(__file__)) 
        utils.create_json_file (dir_name=script_dir, dataset_name=category, json_data=items_data)
    return "ok"
        
#2 récupère les données de tous les items d'un catégory donnée   
def get_items_data (category):
    url = BASE_URL + "/wiki/Category:" + category
    items_list = get_items_list(url)  #3 ramène la liste des items à partir de la page d'une catégorie donnée, avec l'url de la page de l'item
    if items_list:
        items_data = []
        cpt = 0
        nb_items= len(items_list)
        for item in items_list: 
            item_url = BASE_URL+item.get("url")
            item_data = get_item_data (item_url) #4 ramène les données d'un item à partir de l'url sa page
            print (item_url)
            if item_data:
                items_data.append(item_data)
                cpt+=1
                print (f"{cpt}/{nb_items}")
    return items_data     

#3 ramène la liste des items à partir de la page d'une catégorie donnée
def get_items_list(items_list_url):
    print("    [>]  process_items_data.get_items_list")
    soup = utils.get_soup(items_list_url)
    
    if soup:
        # On extrait les données qui nous intéressent dans l'extraction BeautifulSoup
        start = soup.find("div", {"id": "mw-pages"})
        if start:
            print("start")
            rows = start.find_all("li")
            if rows :
                print("step 1")
                print(len(rows))
                # on va construire le tableau des équipements
                items_list = []                
                for row in rows: 
                    link = row.find("a")
                    item = {
                        "title": link.get("title") if link else None,
                        "name": row.get_text(strip=True),
                        "url": link.get("href") if link  else None
                    }
                    items_list.append(item)
                return items_list
    return None

#4 ramène les données d'un item à partir de l'url sa page
def get_item_data (item_url):
    item_data = {}
    img_src_url = None
    icon_src_url = None
    title = None
    name = None

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
      
  
    