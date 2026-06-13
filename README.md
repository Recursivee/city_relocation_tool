# Relocation City Comparison to Adelaide

A tool for use in helping determine relocation tradeoffs between cities with user selected currency serving as the currency base. 

## Use Case
This program acts as a data-driven comparison tool between considered cities to evaluate mobility opportunities via normalising Purchasing Power Parity (PPP) and qualitative lifestyle metrics across disparate geographical locations.

## Key Features
*   **Dynamic Income Adjustment:** Automatically normalises wages into a chosen currency. 
*   **COL adjustment:** Draws Cost of Living data from webscraped source.
*   **QOL adjustment:** Calculates Quality of Life data for comparison, this is calculated through consideration of crime rates, traffic, health care and pollution data.
*   **Relational Logic:** Uses a SQLite backend to handle calculations between cities, cost metrics and psychological utility. 

## Data Pipeline
*   **1:** Webscraped data respecting rate limiting 
*   **2:** Python cleans data with Pandas
*   **3:** Cleaned data implemented into SQLite Database
*   **4:** Semantic data modeling and interactive visualisation via PowerBI

## Database Schema

### `cities`
Tracks interested cities.
* `city_id`: Integer (PK)
* `city_name`: String
* `country`: String
* `base_currency`: String

### `cost_metrics`
* `metric_id`: Integer (PK)
* `city_id`: Integer (FK, cities.city_id)
* `category`: String
* `item_name`: String
* `cost_aud`: Real

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

## File Tree:
```
city-relocation-pipeline/
│
├── data/
│   └── cities_list.json             # JSON list of considered countries
│
├── database/
│   ├── schema.sql                   # SQL table definitions
│   └── comparison.db                # The SQLite database file
│
├── scripts/
│   ├── setup_db.py                  # Python script to setup database 
│   ├── fetch_data.py                # Python script to pull from API
│   └── populate_db.py               # Python script to clean & load into SQLite, this is data pipeline file
│
├── dashboards/
│   └── cost_of_living_analysis.pbix # Final Power BI file
│
├── README.md                        # This document
└── requirements.txt                 # List of Python packages used
```
