import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

engine=create_engine('mysql://admin:motorcycle@florida-motorcycle.ctszlnjsvxow.us-east-1.rds.amazonaws.com:3306/motorcycle')

#create dataframe
df= pd.read_csv('D:\CUTR\dashhboard\my_sql\\fatalities_sql.csv')

df.to_sql('fatalties_bkp',con = engine, if_exists = 'replace', chunksize = 1000)
print(df.shape)

