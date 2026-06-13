## Interactive Dashboard Preview
![All Cities](/Images/all_cities_dashboard.png)
![Sydney Exmaple](/Images/sydney_dashboard.png)


# City Relocation Comparison Tool

A tool for use in helping determine relocation tradeoffs between cities with user selected currency serving as the currency base. 

## Use Case
This program acts as a data-driven comparison tool between considered cities to aid evaluation of mobility opportunities. This is achieved through normalising cost of living, average net incomes and quality of life metrics across disparate geographical locations.

## Key Features
*   **Dynamic Financial Adjustment:** Automatically normalises financial data into a chosen currency. 
*   **COL adjustment:** Draws Cost of Living data from webscraped source.
*   **QOL adjustment:** Draws Quality of Life data from webscraped source.
*   **Relational Logic:** Uses a SQLite backend to handle calculations between cities, cost metrics and psychological utility. 

## Data Pipeline
*   **1:** Webscraped data respecting rate limiting 
*   **2:** Python cleans data with Pandas and BeautifulSoup
*   **3:** Cleaned data implemented into SQLite Database
*   **4:** Interactive visualisation of data modeling with use of a PowerBI dashboard

## Database Schema

### `cities`
Tracks interested cities.
* `city_id`: Integer (PK)
* `city_name`: String


### `cost_metrics`
* `metric_id`: Integer (PK)
* `city_id`: Integer (FK, cities.city_id)
* `category`: String
* `item_name`: String
* `cost_aud`: Real -- note that cost_aud is leftover from original, this just records the cost in whichever chosen currency NOT specifically aud. 

### `psych_utility`
* `utility_id`: Integer (PK) 
* `city_id`: Integer (FK, cities.city_id)
* `qol_item_name`: String
* `qol_item_score`: Real


##  Getting Started
1. **Setup Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
    ```

2. **Run Pipeline**:
   ```bash
   run python scripts/populate_db.py to generate SQLite database locally, then open dashboard/dashboard.pbix in PowerBi Desktop and click refresh. 
    ```

## File Tree:
```
City_Relocation_Tool/
├── Dashboards
│   └── Dashboard.pbix
├── Data
│   └── cities_list.json
├── Database
│   └── schema.sql
├── Images
│   ├── all_cities_dashboard.png
│   └── sydney_dashboard.png
├── Scripts
│   ├── fetch_data.py
│   ├── populate_db.py
│   └── setup_db.py
├── .gitignore
├── README.md
└── requirements.txt
```
