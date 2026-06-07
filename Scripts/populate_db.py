from pathlib import Path
import sqlite3
from setup_db import initialise_database
from fetch_data import cities_considered, scrape_data


main_folder = Path(__file__).parent.parent
database_location = Path(main_folder/'Database/comparison.db')
schema_location = Path(main_folder/'Database/schema.sql')

database_location.parent.mkdir(exist_ok=True, parents=True)


def populate_db():
    initialise_database(database_location, schema_location)
    
    chosen_cities = cities_considered()
    
    data_to_insert = scrape_data(chosen_cities)
    
    with sqlite3.connect(main_folder/'Database/comparison.db') as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
            
        for city_record in data_to_insert:
            #sql insertion of cities (parent)
            cursor.execute(
                "INSERT OR IGNORE INTO cities (city_name) VALUES (?);",
                (city_record["city_label"],)
            )
            
            parent_id = cursor.lastrowid
            
            if not parent_id or parent_id == 0:
                cursor.execute(
                    "SELECT city_id FROM cities WHERE city_name = ?;"
                )
                parent_id = cursor.fetchone()[0]
            
            

            
            #sql insertion of item data (child)
            for metric_item in city_record["sub_items"]:
                cursor.execute(
                    """
                    INSERT INTO cost_metrics (category, item_name, cost_aud, city_id)
                    VALUES (?, ?, ?, ?);
                    """,
                    ("Housing", metric_item["name"], metric_item["value"], parent_id)
                )
            
        print("Completed")    


if __name__ == "__main__":
    populate_db()