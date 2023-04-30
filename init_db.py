import sqlite3

connection = sqlite3.connect('database24.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

#cur.execute("INSERT INTO users (user_id, first_name, last_name, user_name, user_password) VALUES (?, ?, ?, ?, ?)",
#            ('1', 'Kshitija', 'Shete','kshitija793@gmail.com','kshitija@123S')
#            )

#cur.execute("INSERT INTO users (user_id, first_name, last_name, user_name, user_password) VALUES (?, ?, ?, ?, ?)",
#            ('2', 'Archana','Nikam','archana98@gmail.com','archana@123S')
#            )

#cur.execute("INSERT INTO users (user_id, first_name, last_name, user_name, user_password) VALUES (?, ?, ?, ?, ?)",
#            ('3', 'Sayali', 'Deshmukh','sayali99@gmail.com','sayali@123S')
#            )            

connection.commit()
connection.close()