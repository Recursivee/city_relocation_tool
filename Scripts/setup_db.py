from pathlib import Path
import sqlite3

# main_folder = Path(__file__).parent.parent
# database_location = Path(main_folder/'Database/comparison.db')
# schema_location = Path(main_folder/'Database/schema.sql')

# database_location.parent.mkdir(exist_ok=True, parents=True)

# connection = sqlite3.connect(main_folder/'Database/comparison.db')
# cur = connection.cursor()

# try:
#     with schema_location.open("r") as file:
#         content = file.read()
#         cur.executescript(content)
# except sqlite3.Error as e:
#     print(f"An error occured: {e}")
# finally:
#     if connection:
#         connection.close()


def initialise_database(database_location, schema_location):
    try:
        with sqlite3.connect(database_location) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
        
        with schema_location.open("r") as file:
            content = file.read()
            cursor.executescript(content)
    except sqlite3.Error as e:
        print(f"An error occurred during initialisation: {e}")
    