import sqlite3
try:
    connection = sqlite3.connect('emaildb.sqlite')
except Error as e:
    print(e)
cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS counts')
cursor.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input("Enter File Name: ")
if (len(fname)< 1):
    fname = "mbox.txt"
fh = open(fname)
for line in fh:
    if (not line.startswith("From: ")): continue
    pieces = line.split() 
    split_line = pieces[1]
    start = split_line.find("@")
    end = split_line.find(".", start)
    org = split_line[start + 1:]
#     email = pieces[1]
#    print(org)
#     print(split_line)
    cursor.execute('SELECT count FROM Counts WHERE org = ?', (org, ) )
    row = cursor.fetchone()
    if (row is None):
        cursor.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cursor.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
connection.commit()
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cursor.execute(sqlstr):
    print(str(row[0]), row[1])

# cursor.close()