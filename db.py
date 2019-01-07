import sqlite3
import sys
import datetime

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
            (
                id INTEGER PRIMARY KEY,
                description string,
                detail string,
                locations string,
                times string,
                people string,
                deadline timestamp,
                deleted_at timestamp
            )
            ''')
        self.cursor.execute('''INSERT INTO tasks (description, detail) VALUES ('this is description', 'more...')''')
        self.cursor.execute(
            '''INSERT INTO tasks (description, detail) VALUES ('finish proj on wednesday', 'just do it')''')
        self.commit()

    def read_all(self):
        cursor = self.cursor.execute('''SELECT * FROM tasks WHERE deleted_at is NULL ORDER BY deadline DESC''')
        res = cursor.fetchall()

        tasks = [{
            "id": row[0],
            "description": row[1],
            "detail": row[2],
            "locations": row[3],
            "times": row[4],
            "people": row[5],
            "deadline": row[6],
        } for row in res]

        return tasks

    def create(self, action):
        self.cursor.execute(
            '''INSERT INTO tasks (
                description,
                detail,
                locations,
                times,
                people,
                deadline)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (
                action['description'],
                action['detail'],
                action['locations'],
                action['times'],
                action['people'],
                action['deadline'],
            )
        )
        self.commit()

    def delete(self, task_id):
        self.cursor.execute('''
            UPDATE tasks
            SET deleted_at = ?
            where id = ?
        ''', (
            datetime.datetime.now(), str(task_id)
        ))

        self.commit()

db = DB()

# python db.py reset
if 'reset' in sys.argv:
    db.reset()

# python db.py seed
if 'seed' in sys.argv:
    db.seed()
    tasks = db.read_all()
    print(tasks)

if 'temp' in sys.argv:
    tasks = db.read_all()
    print(tasks)
