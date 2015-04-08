
import sqlite3 as dbapi


class DataSource(object):
    def __init__(self):
        self.conn = None

    def __del__(self):
        if self.conn:
            self.conn.close()

    def openDB(self, name):
        """open an existing database."""
        self.conn = dbapi.connect(name)

    def buildDB(self, name):
        """build a new database to use."""
        self.conn = dbapi.connect(name)
        try:
            c = self.conn.cursor()
            c.execute('CREATE TABLE fortune('
                      'id INTEGER PRIMARY KEY ASC, data TEXT)')
            self.conn.commit()

        except Exception:
            self.conn.rollback()
            raise

    def getCount(self):
        sql = 'SELECT Count(*) FROM fortune'
        c = self.conn.cursor()
        c.execute(sql)
        return c.fetchone()[0]

    def addFortune(self, data):
        c = self.conn.cursor()
        sql = 'INSERT INTO fortune (data) VALUES (?)'
        try:
            c.execute(sql, (data,))
            fortuneId = c.lastrowid
            self.conn.commit()
            return fortuneId

        except Exception:
            self.conn.rollback()
            raise

    def delCard(self, itemId):
        c = self.conn.cursor()
        sql = 'DELETE FROM fortune WHERE id=?'

        try:
            c.execute(sql, (itemId,))
            self.conn.commit()

        except Exception:
            self.conn.rollback()
            raise

    def getFortunes(self):
        sql = 'SELECT id, data FROM fortune'
        c = self.conn.cursor()
        c.execute(sql)
        return c.fetchall()

    def getFortune(self, id):
        sql = 'SELECT data FROM fortune WHERE id=?'
        c = self.conn.cursor()
        c.execute(sql, (id,))
        return c.fetchone()[0]
