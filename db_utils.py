import pyodbc
from datetime import datetime

class DatabaseConnection:
    def __init__(self):
        # SQL Server connection string with correct ODBC driver
        self.connection_string = (
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost\\SQLEXPRESS;'
            'DATABASE=ProEstate;'
            'Trusted_Connection=yes;'
        )
        self.conn = None
        self.cursor = None
        self._connect()

    def _connect(self):
        """Establish database connection and create cursor"""
        try:
            self.conn = pyodbc.connect(self.connection_string)
            self.cursor = self.conn.cursor()
        except pyodbc.Error as e:
            raise Exception(f"Failed to connect to database: {str(e)}")

    def fetch_all(self, query, params=None):
        """Execute query and return all rows"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except pyodbc.Error as e:
            self.rollback()
            raise Exception(f"Database query error: {str(e)}")

    def fetch_one(self, query, params=None):
        """Execute query and return first row"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except pyodbc.Error as e:
            self.rollback()
            raise Exception(f"Database query error: {str(e)}")

    def execute(self, query, params=None):
        """Execute a query (INSERT, UPDATE, DELETE)"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor
        except pyodbc.Error as e:
            self.rollback()
            raise Exception(f"Database execution error: {str(e)}")

    def commit(self):
        """Commit current transaction"""
        try:
            if self.conn:
                self.conn.commit()
        except pyodbc.Error as e:
            raise Exception(f"Database commit error: {str(e)}")

    def rollback(self):
        """Rollback current transaction"""
        try:
            if self.conn:
                self.conn.rollback()
        except pyodbc.Error as e:
            raise Exception(f"Database rollback error: {str(e)}")

    def execute_query(self, query, params=None):
        """Execute a query and return cursor (legacy method for compatibility)"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.conn, self.cursor
        except pyodbc.Error as e:
            self.rollback()
            raise Exception(f"Database query error: {str(e)}")

    def execute_non_query(self, query, params=None):
        """Execute a non-query (INSERT, UPDATE, DELETE) (legacy method for compatibility)"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.commit()
            return self.conn, self.cursor
        except pyodbc.Error as e:
            self.rollback()
            raise Exception(f"Database execution error: {str(e)}")

    def close_connection(self, conn=None, cursor=None):
        """Close cursor and connection (legacy method for compatibility)"""
        # Since we use persistent connection, this is mainly for compatibility
        pass

    def close(self):
        """Close the persistent connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except pyodbc.Error as e:
            raise Exception(f"Error closing database connection: {str(e)}")

    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()
