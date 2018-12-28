import sqlite3
import sys

DB_NAME = 'todo.db'
conn = sqlite3.connect(DB_NAME)


class DB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = conn.cursor()

    def commit(self):
        self.cursor.execute('commit')

    def reset(self):
        self.cursor.execute('''DROP TABLE tasks''')

    def seed(self):
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS tasks 
            (id INTEGER PRIMARY KEY, description string, detail string, locations string, times string, people string)
            ''')
        self.cursor.execute('''INSERT INTO tasks (description, detail) VALUES ('this is description', 'more...')''')
        self.cursor.execute(
            '''INSERT INTO tasks (description, detail) VALUES ('finish proj on wednesday', 'just do it')''')
        self.commit()

    def get(self):
        cursor = self.cursor.execute('''SELECT * FROM tasks''')
        res = cursor.fetchall()

        for row in res:
            print(row)

    def create(self, action):
        self.cursor.execute(
            '''INSERT INTO tasks (description, detail, locations, times, people) VALUES (?, ?, ?, ?, ?)''',
            (action['description'], action['detail'], action['locations'], action['times'], action['people'])
        )
        self.commit()


db = DB()

# python db.py reset
if 'reset' in sys.argv:
    db.reset()
    db.seed()
    db.get()
