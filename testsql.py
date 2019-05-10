import MySQLdb

usename = 'test1' 

conn = MySQLdb.connect("localhost","testuser","inicio123","bucketlist")
		
conn.autocommit(True)	
conn.set_character_set('utf8')

cursor = conn.cursor()

cursor.execute("SELECT * FROM tbl_users WHERE user_name = %s", ['test1'])

rows = cursor.fetchall()
print('Total Row(s):', cursor.rowcount)

for row in rows:
	print(row[3])