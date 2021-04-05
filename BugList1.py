import sqlite3, pandas as pd

dbname = 'devTest'
conn = sqlite3.connect(dbname + '.sqlite')
cur = conn.cursor()

read_file = pd.read_excel (r'BugList.xlsx', sheet_name='BugsList')
read_file.to_csv (r'BugList.csv', index = None, header=True)

table_name = 'BugsList'

create_query = 'CREATE TABLE IF NOT EXISTS '+'table_name'+'''(BugListId INTEGER PRIMARY KEY,
TestCaseId TEXT,
BugTitle TEXT,
Category TEXT,
Severity TEXT,
Priority TEXT,
Source TEXT,
Status TEXT,
ModuleName TEXT,
ReporteeName TEXT,
Owner TEXT,
TypeOfBug TEXT,
Description TEXT,
PreCondition TEXT,
StepsToProduce TEXT,
PostCondition TEXT,
ExpectedResult TEXT,
ActualResult TEXT,
ModifiedDate TEXT,
DevComment TEXT,
QAComment TEXT,
BugImagesCSV TEXT,
IsActive TEXT DEFAULT 1
)'''

chunksize = 1000
for chunk in pd.read_csv('BugList.csv', chunksize=chunksize):
    #trim leading and trailing spaces
    chunk.to_sql(name='BugsList', con=conn, if_exists='append')

cur.close()