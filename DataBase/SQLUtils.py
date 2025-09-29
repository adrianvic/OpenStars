import pymysql
import datetime
from Utils.Logger import Logger
from Logic.Player import Player

class SQLUtils:
    def __init__(self, connection):
        self.conn = connection

    def insert_data(self, table, data: dict):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, list(data.values()))
        self.conn.commit()

    def delete_data(self, table: str, data: dict):
        conditions = " AND ".join([f"{col} = %s" for col in data.keys()])
        sql = f"DELETE FROM {table} WHERE {conditions}"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, list(data.values()))
        self.conn.commit()

    def update_document(self, table, query: dict, item, value=None):
        """
        If `item` is a dict, treat as bulk update (key=value pairs).
        If `item` is a str, update single field with `value`.
        """
        if isinstance(item, dict):
            set_clause = ", ".join([f"{k}=%s" for k in item.keys()])
            values = list(item.values())
        else:
            set_clause = f"{item}=%s"
            values = [value]

        where_clause = " AND ".join([f"{k}=%s" for k in query.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, values + list(query.values()))
        self.conn.commit()

    def update_all_documents(self, table, query: dict, item: str, value):
        # Same as update_document; SQL updates all matching rows automatically
        self.update_document(table, query, item, value)

    def delete_document(self, table, query: dict):
        where_clause = " AND ".join([f"{k}=%s" for k in query.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause} LIMIT 1"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, list(query.values()))
        self.conn.commit()

    def delete_all_documents(self, table, query: dict):
        where_clause = " AND ".join([f"{k}=%s" for k in query.keys()]) if query else "1"
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, list(query.values()) if query else [])
        self.conn.commit()

    def load_document(self, table, query: dict):
        where_clause = " AND ".join([f"{k}=%s" for k in query.keys()])
        sql = f"SELECT * FROM {table} WHERE {where_clause} LIMIT 1"
        with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, list(query.values()))
            return cursor.fetchone()

    def load_all_documents(self, table, query: dict):
        where_clause = " AND ".join([f"{k}=%s" for k in query.keys()]) if query else "1"
        sql = f"SELECT * FROM {table} WHERE {where_clause}"
        with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, list(query.values()) if query else [])
            return cursor.fetchall()

    def load_all_documents_sorted(self, table, query: dict, element, element2=None):
        where_clause = " AND ".join([f"{k}=%s" for k in query.keys()]) if query else "1"
        sql = f"SELECT * FROM {table} WHERE {where_clause} ORDER BY {element} DESC"
        with self.conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, list(query.values()) if query else [])
            rows = cursor.fetchall()
            if element2:
                # Only include rows where element2 != 0
                return [r for r in rows if r.get(element2, 0) != 0]
            return rows