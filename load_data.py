"""
create and load data into posgres
"""

import pandas as pd
from sqlalchemy import create_engine


sales_uri = "s3://d2b-academy-dbt-public/supermarket_sales.csv"
product_uri = "s3://d2b-academy-dbt-public/product.csv"

CREATE_TABLE_SALES = \
    """
CREATE TABLE IF NOT EXISTS SALES (
    invoice_id TEXT PRIMARY KEY,
    branch TEXT,
    city INTEGER,
    customer TEXT,
    gender TEXT,
    product_line INTEGER,
    price FLOAT,
    quantity INTEGER,
    tax FLOAT,
    total FLOAT,
    date TEXT,
    time TEXT,
    payment TEXT,
    cogs FLOAT,
    gross_income FLOAT,
    rating INTEGER,
    FOREIGN KEY(product_line) REFERENCES PRODUCTS(product_id)
);
"""

CREATE_TABLE_PRODUCT = \
    """
CREATE TABLE IF NOT EXISTS PRODUCTS (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT
);
"""


def establish_connection(host, port, db, user, password):
    """
    :param host: postgres  host
    :param port: postgres port
    :param db: postgres db
    :param user:
    :param password:
    :return: engine
    """

    # connection for pandas
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    # connection for psycopg2 to postgres

    return engine


def run_sql_query(engine, query):
    """
    :param engine
    :param query
    """

    with engine.connect() as con:
        try:
            con.execute(query)
            print(f"query executed successfully")
        except Exception as e:
            print(f"Error running:\n {query}")
            print(e)

def load_data_to_table(table_name, s3_uri, engine):
    """
    :param table_name
    :param s3_uri
    :param engine
    """
    df = pd.read_csv(s3_uri)

    if table_name == "sales":
        df.rename(columns={"gross income": "gross_income"}, inplace=True)

    print(f"loading data into the {table_name} table")
    df.to_sql(name=table_name, con=engine, if_exists="append", index=False)

    print("loading completed")


def main():
    # create tables
    engine = establish_connection(host="pgdatabase", port="5432", db="data2bots", user="d2b_user", password="data2bots")
    run_sql_query(engine=engine, query=CREATE_TABLE_PRODUCT)
    run_sql_query(engine=engine, query=CREATE_TABLE_SALES)


    # load data into tables
    load_data_to_table(table_name="products", s3_uri=product_uri, engine=engine)
    load_data_to_table(table_name="sales", s3_uri=sales_uri, engine=engine)

if __name__ == "__main__":
    main()
