from bs4 import BeautifulSoup
import requests
import json

item_data = None
img_src_url = None
icon_src_url = None
title = None
name = None

# Récupère les données brutes d'une page web
def get_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def get_item_data (item_url):
    if item_url:
        soup = get_soup(item_url)
        if soup:
            start = soup.select_one("table.infoboxtable")
            if start :
                headers = [tr for tr in start.select("tr") if not tr.find("td")]
                if headers :
                    title_zone = headers[0].select_one("span[title]") if len(headers) > 0  else None
                    title = title_zone.get("title") if title_zone is not None else None
                    name = headers[0].get_text(";", strip=True) if len(headers) > 0 else None
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
                    tr.find("th").get_text(";", strip=True): tr.find("td").get_text(";", strip=True)
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
  
    #json_object = json.loads(item_data)
    json_formatted_str = json.dumps(item_data, indent=2)
    print(json_formatted_str)
    
get_item_data("https://astroneer.fandom.com/wiki/Large_Rover_Seat")
get_item_data("https://astroneer.fandom.com/wiki/Large_Fog_Horn")
get_item_data("https://astroneer.fandom.com/wiki/Buggy")