import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd  # noqa: E402

from my_fapi.db import engine  # noqa: E402

CSV_PATH = Path("/home/nikhil/Documents/python/notebooks/data/titanic/training.csv")
TABLE_NAME = "passengers"

# Matches the snake_case column names used elsewhere in the API (see tb.py examples).
COLUMN_RENAME = {
    "PassengerId": "passenger_id",
    "Survived": "survived",
    "Pclass": "pclass",
    "Name": "name",
    "Sex": "sex",
    "Age": "age",
    "SibSp": "sibsp",
    "Parch": "parch",
    "Ticket": "ticket",
    "Fare": "fare",
    "Cabin": "cabin",
    "Embarked": "embarked",
}


def main() -> None:
    df = pd.read_csv(CSV_PATH)
    df = df.rename(columns=COLUMN_RENAME)
    # if_exists="append" creates the table (with pandas-inferred types, no primary key)
    # if it doesn't exist yet. Create it first via POST /tables if you want passenger_id
    # set as the primary key for the row-level GET/PUT/DELETE endpoints to work on it.
    df.to_sql(TABLE_NAME, engine, if_exists="append", index=False)
    print(f"Imported {len(df)} rows into '{TABLE_NAME}'")


if __name__ == "__main__":
    main()
