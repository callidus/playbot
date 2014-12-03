 
import sqlite3 as dbapi

class DataSource( object ):
    def __init__( self ):
        self.conn = None
    
    def __del__( self ):
        if self.conn:
            self.conn.close()
    
    def openDB( self, name ):
        """
        open an existing database
        """
        self.conn = dbapi.connect( name )
    
    def buildDB( self, name ):
        """
        build a new database to use
        """
        self.conn = dbapi.connect( name )
        try:
            c = self.conn.cursor()
            c.execute( '''CREATE TABLE white( id INTEGER PRIMARY KEY ASC, title TEXT, data TEXT )''' )
            c.execute( '''CREATE TABLE black( id INTEGER PRIMARY KEY ASC, title TEXT, slots INTEGER, data TEXT )''' )
            self.conn.commit()
            
        except:
            self.conn.rollback()
            raise
            
    def addWhiteCard( self, title, data ):
        c = self.conn.cursor()
        sql = '''INSERT INTO white ( title, data ) VALUES ( ?, ? )'''
        try:
            c.execute( sql, ( title, data ) )
            cardId = c.lastrowid    
            self.conn.commit()
            
        except:
            self.conn.rollback()
            raise
        
    def addBlackCard( self, title, slots, data ):
        c = self.conn.cursor()
        sql = '''INSERT INTO black ( title, slots, data ) VALUES ( ?, ?, ? )'''
        try:
            c.execute( sql, ( title, slots,data ) )
            cardId = c.lastrowid    
            self.conn.commit()
            
        except:
            self.conn.rollback()
            raise
        
        
    def delCard( self, white, itemId ):
        c = self.conn.cursor()
        sql = '''DELETE FROM black WHERE id=? '''
        if white:
            sql = '''DELETE FROM white WHERE id=? '''
            
        try:
            c.execute( sql, ( itemId, ) )
            self.conn.commit()
            
        except:
            self.conn.rollback()
            raise
        
        
    def getBlackCards( self ):
        sql = '''SELECT id, title FROM black'''    
        c = self.conn.cursor()
        c.execute( sql )
        return c.fetchall()
        
    def getWhiteCards( self ):
        sql = '''SELECT id, title FROM white'''    
        c = self.conn.cursor()
        c.execute( sql )
        return c.fetchall()
        
    def getBlackCard( self, id ):
        sql = '''SELECT title, data, slots FROM black WHERE id=?'''            
        c = self.conn.cursor()
        c.execute( sql, ( id, ) )
        return c.fetchone()

    def getWhiteCard( self, id ):
        sql = '''SELECT title, data FROM white WHERE id=?'''            
        c = self.conn.cursor()
        c.execute( sql, ( id, ) )
        return c.fetchone()
        
    
