from pathlib import Path
import json
import time
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
import re
import pandas as pd

main_folder = Path(__file__).parent.parent
database_location = Path(main_folder/'Database/comparison.db')
city_location = Path(main_folder/'Data/cities_list.json')

#creates directory if not existing prior to writing later in script
database_location.parent.mkdir(exist_ok=True, parents=True)
city_location.parent.mkdir(exist_ok=True, parents=True)


#loads json file as list, if no file creates empty list
try:
    with city_location.open("r") as file:
        current_cities = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    current_cities = []
    
    
    
#loop to choose cities and dump into json list    
def cities_considered():
    checker = True
    while checker == True:
        print(f"These are the currently considered cities: {current_cities}")
        print(f"Select from the following options: ")
        print(f"1: Accept the current cities")
        print(f"2: Add a city")
        print(f"3: Remove a city")
        city_choice = input("Enter your selection: ")
        
        if city_choice == "1":
            with city_location.open("w") as file:
                json.dump(current_cities, file, indent=4, sort_keys=True)            
            break
        
        elif city_choice == "2":
            added_city = input("Enter the name of the city to add: ").strip().title()
            
            if added_city in current_cities:
                print("that city is already added, no updates made")
            else:
                current_cities.append(added_city)
                print(f"{added_city} has been added to the list.")
                
                
        elif city_choice == "3":
            remove_city = input("Enter the name of the city to remove: ").strip().title()
            
            if remove_city in current_cities:
                current_cities.remove(remove_city)
                print(f"{remove_city} has been removed from the list.")
            else:
                print(f"{remove_city} is not currently on the list, no updates made.")
            
        else:
            print(f"Please make a valid selection")
            
    return current_cities
    
    

    
    
#loop to scrape and parse data for cities listed in json    
def scrape_data(target_cities):
    headers = {'User-Agent': 'COL_Test_Project/1.0'}    
    base_url = "https://www.numbeo.com/cost-of-living/in/"    
    all_scraped_data = []
    base_currency = input("Enter the 3 digit currency code for chosen base currency: ") or "AUD"
    normalised_base_currency = base_currency.upper()
    
    for city_names in target_cities:
        city_record = {
            "city_label": city_names,
            "sub_items": [],
            "qol_items": []
        }

        new_url = f"https://www.numbeo.com/cost-of-living/in/{city_names}?displayCurrency={normalised_base_currency}"
        qol_url = f"https://www.numbeo.com/quality-of-life/in/{city_names}"
        
        
        try:
            response = requests.get(new_url, headers=headers, timeout=10)
            response.raise_for_status()
            raw_html_data = response.text
            
            #bs4 integration here
            soup = BeautifulSoup(raw_html_data, "html.parser")
            data_table = soup.find("table", class_="data_wide_table new_bar_table")
            
            if data_table:
                rows = data_table.find_all("tr")
                current_category = "General"
                header_checker = False
                
                for row in rows:
                    row_classes = row.get("class", [])
                    
                    if "break_category" in row_classes:
                        header_checker = True
                        continue
                    
                    if header_checker:
                        category_div = row.find("div", class_="category_title")
                        if category_div:
                            current_category = category_div.text.strip()
                        header_checker = False
                        continue
                    
                    cells = row.find_all("td")
                    
                    if len(cells) >= 2:
                        item_name = cells[0].text.strip()
                        item_value_string = cells[1].text.strip()
                        clean_string = re.sub(r"[^\d.]", "", item_value_string)
                        item_value = Decimal(clean_string)
                        #sqlite doesnt like decimal oops
                        item_value_float = float(item_value)
                        print(f"[{current_category}] Found {item_name}, {item_value_float}")
                        
                        #output to list of dictionaries, each city is its own dictionary with metrics listed inside
                        metric = {
                            "category": current_category,
                            "name": item_name,
                            "value": item_value_float
                        }
                        city_record["sub_items"].append(metric)                        
        
        except requests.exceptions.RequestException as error:
            print(f"Skipping {city_names} due to error: {error}")
                
        time.sleep(10)
        
        try:
            qol_response = requests.get(qol_url, headers=headers, timeout=10)
            qol_response.raise_for_status()
            raw_qol_data = qol_response.text
            
            #bs4 integration here
            qol_soup = BeautifulSoup(raw_qol_data, "html.parser")
            qol_data_table = qol_soup.find("table", class_="qol-breakdown")
            
            if qol_data_table:
                qol_rows = qol_data_table.find_all("tr")

                for row in qol_rows:
                    qol_row_classes = row.get("class", [])
                    qol_cells = row.find_all("td")
                    
                    if len(qol_cells) >= 2:
                        qol_item_name = qol_cells[0].text.strip()
                        qol_item_value_string = qol_cells[1].text.strip()
                        qol_clean_string = re.sub(r"[^\d.]", "", qol_item_value_string)
                        
                        if qol_clean_string:
                            qol_item_value_float = float(qol_clean_string)
                            print(f"Found {qol_item_name}, {qol_item_value_float}")

                            qol_metric = {
                                "qol_name": qol_item_name,
                                "qol_score": qol_item_value_float
                            }
                            city_record["qol_items"].append(qol_metric)

        except requests.exceptions.RequestException as error:
            print(f"Skipping {city_names} QOL due to error: {error}")
                
        time.sleep(10)
        
        all_scraped_data.append(city_record)                    
        
    return all_scraped_data
    
    



if __name__ == "__main__":
    target_cities = cities_considered()
    scrape_data()