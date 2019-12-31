import sqlite3


class DbHandler:
    def __init__(self, dbname):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()
        self.setup()

    def setup(self):
        # CREATE TABLE DemonSlayer (chapter_name text)
        query = '''CREATE TABLE IF NOT EXISTS DemonSlayer
                    (chapter_name text)'''
        self.cur.execute(query)
        # Commit (save) the changes
        self.conn.commit()

    def insert_values(self, ch):
        # INSERT INTO DemonSlayer VALUES('Dm 179')
        query = "INSERT INTO DemonSlayer(chapter_name) VALUES(?)"
        args = (ch, )
        self.cur.execute(query, args)
        self.conn.commit()

    
    def update_values(self, old_chapter, chapter):
        # INSERT INTO DemonSlayer VALUES('Dm 179')
        query = "UPDATE DemonSlayer SET chapter_name = ? WHERE chapter_name = ?"
        args = (old_chapter, chapter, )
        self.cur.execute(query, args)
        self.conn.commit()


    def retrieve_data(self):
        data = []
        query = 'SELECT chapter_name FROM DemonSlayer'
        for x in self.cur.execute(query):
            data.append(x)
        return data[0]
