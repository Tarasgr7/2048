import sqlite3

bd = sqlite3.connect("2048.sqlite")

cur = bd.cursor()
cur.execute(''' create table if not exists RECORDS (name text, score integer)
''')


def get_best():
    cur.execute('''SELECT  name,max(score) score  from RECORDS
    GROUP by name 
    ORDER by score DESC
    LIMIT 3''')
    return cur.fetchall()


def insert_result(name, score):
    cur.execute('''insert into RECORDS  values (?,?)''', (name, score))
    bd.commit()



