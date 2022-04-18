import databaseConnections as dc
import pandas as pd
from config import sqlPath
from config import sqlPassword

#connection = dc.create_db_connection("localhost", "root", sqlPassword, db)
#below when you don't want to specify a table to connect to, ie you are creating one
connection = dc.create_server_connection("localhost", "root", sqlPassword)

create_database = "CREATE DATABASE cryptoData"
dc.execute_query(connection, create_database) # Execute our defined query



#create_teacher_table = """
#CREATE TABLE teacher (
#  teacher_id INT PRIMARY KEY,
#  first_name VARCHAR(40) NOT NULL,
#  last_name VARCHAR(40) NOT NULL,
#  language_1 VARCHAR(3) NOT NULL,
#  language_2 VARCHAR(3),
#  dob DATE,
#  tax_id INT UNIQUE,
#  phone_no VARCHAR(20)
#  );
# """



#df = pd.DataFrame({'teacher_id': [4], 'first_name':['Bob'], 'last_name':['Smith'], 'language_1':['English'],
#'language_2':['Swedish'], 'dob':['26/11/22'],'tax_id':[222], 'phone_no':[1277] })

#df.to_sql(con=connection, name='teacher', if_exists='replace')
#dc.execute_query(connection, create_teacher_table)