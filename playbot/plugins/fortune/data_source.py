
from __future__ import absolute_import

import sqlite3 as dbapi


class DataSource(object):
    def __init__(self):
        self.conn = None

    def __del__(self):
        if self.conn:
            self.conn.close()

    def open_db(self, name):
        """open an existing database."""
        self.conn = dbapi.connect(name)

    def build_db(self, name):
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

    def get_count(self):
        sql = 'SELECT Count(*) FROM fortune'
        c = self.conn.cursor()
        c.execute(sql)
        return c.fetchone()[0]

    def add_fortune(self, data):
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

    def del_fortune(self, itemId):
        c = self.conn.cursor()
        sql = 'DELETE FROM fortune WHERE id=?'

        try:
            c.execute(sql, (itemId,))
            self.conn.commit()

        except Exception:
            self.conn.rollback()
            raise

    def get_fortunes(self):
        sql = 'SELECT id, data FROM fortune'
        c = self.conn.cursor()
        c.execute(sql)
        return c.fetchall()

    def get_fortune(self, id):
        sql = 'SELECT data FROM fortune WHERE id=?'
        c = self.conn.cursor()
        c.execute(sql, (id,))
        return c.fetchone()[0]
