import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://d2b_user:data2bots@localhost:5432/data2bots")

df = pd.read_sql_query("SELECT * FROM sales;", con=engine)

print(df)