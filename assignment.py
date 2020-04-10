import sqlite3

from xlrd import open_workbook

# open connection to database
conn = sqlite3.connect('club.db')
c = conn.cursor()


def read_excel_file(file):
    book = open_workbook('{}'.format(file))
    global sheet
    sheet = book.sheet_by_index(0)

    #loop in every record in the worksheet and store them in a list
    total_rows = sheet.nrows
    total_cols = sheet.ncols

    flist = list()
    record = list()

    for x in range(total_rows):
        for y in range(total_cols):
            record.append(sheet.cell(x,y).value)
        flist.append(record)
        record = []
        x +=1
    return (flist)

def column_type(a):
    v = type(flist[1][a])
    if v == float:
        return str(flist[0][a]) + " real"
    elif v == int:
        return str(flist[0][a]) + " integer"
    else:
        return str(flist[0][a]) + " text"
        

def create_table(table):
    # drop table if already exists
    c.execute('DROP TABLE IF EXISTS {}'.format(table))
    
    global sheet
    column = ""
    for i in range(0, sheet.ncols):
        if i < sheet.ncols - 1:
            column += column_type(i) + ", "
        else:
            column += column_type(i)
    with conn:
	    Query = """CREATE TABLE {1}({0})""".format(column,table)
	    
	    c.execute(Query)
	    
 
def insert_from_file(table,flist):
    # generate multiple values from the list to be placed in a query
    del flist[0]
    
    with conn:
	    rows = ''
	    for i in range(len(flist)):
	        t = tuple([x for x in flist[i]])
	        Query = "INSERT INTO {1} VALUES {0}".format(t, table)
	        c.execute(Query)
    # execute the sql command
    

def get_members_by_id(table, id):
    with conn:
        c.execute('''SELECT * FROM {} WHERE ID=:ID'''.format(table), {'TABLE': table, 'ID':id})
    return c.fetchall()


def update_sem(table, id, column,value):

	with conn:
		c.execute('''UPDATE {} SET {}={}
        WHERE ID={}
         '''.format(table,column,value,id))


def remove_members(table, id):
	with conn:
		c.execute('''DELETE FROM {} WHERE
        ID=:ID
        '''.format(table), {'ID': id})

def insert_from_class(table, t):
	with conn:
		Query = "INSERT INTO {1} VALUES {0}".format(t, table)
		c.execute(Query)


class Employee:
    def data(self, **kwargs):
    	for k, v in kwargs.items():
            setattr(self, k, v)
    	list= kwargs.values()
    	
    	return tuple(i for i in list)
        


#	flist=Employee()
#	t=flist.data(**{'first_name':'SOMYA', 'last_name':'RAGHUWANSHI', 'id':'02654', 'gender':'MALE', 'sem':'6'})
#	insert_from_class('SPORTSCLUB',t)

#	flist=read_excel_file('sportsclub.xlsx')
#	create_table('SPORTSCLUB')
#	insert_from_file('SPORTSCLUB',flist)
#	remove_members('SPORTSCLUB', '258763')
#	update_sem('SPORTSCLUB','02654','SEMESTER','4')
#	s=get_members_by_id('SPORTSCLUB', '02654')
#	print(s)


conn.close()
