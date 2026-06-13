PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS cities (
    city_id INTEGER PRIMARY KEY,
    city_name TEXT NOT NULL UNIQUE,
    country TEXT,
    base_currency TEXT
);

CREATE TABLE IF NOT EXISTS cost_metrics (
    metric_id INTEGER PRIMARY KEY,
    category TEXT,
    item_name TEXT,
    cost_aud REAL,
    city_id INTEGER,
    CONSTRAINT fk_cost_city
    FOREIGN KEY (city_id)
    REFERENCES cities(city_id)
);


CREATE TABLE IF NOT EXISTS psych_utility (
    utility_id INTEGER PRIMARY KEY AUTOINCREMENT,
    qol_item_name TEXT,
    qol_item_score REAL, 
    city_id INTEGER,
    CONSTRAINT fk_qol_city
    FOREIGN KEY (city_id)
    REFERENCES cities(city_id)
);