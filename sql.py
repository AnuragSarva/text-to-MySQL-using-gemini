import mysql.connector
from data import *
class SQL:
    def __init__(self, user="root", host="localhost", password="", database=None):
        self.user = user
        self.host = host
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()
        print("DATABSE:", self.database)

    def show_tables(self):
        self.cursor.execute("SHOW TABLES;")
        return [t[0] for t in self.cursor.fetchall()]

    def show_schema(self, table_name):
        self.cursor.execute(f"DESCRIBE {table_name};")
        schema = self.cursor.fetchall()
        res = "| Field | Type | Null | Key | Default | Extra |"
        for f, t, n, k, d, e in schema:
            res += f"\n| {f} | {t} | {n} | {k} | {d} | {e} |"
        return res

    def get_all_schemas(self):
        """Return schema of all tables as a single string"""
        schemas = ""
        for table in self.show_tables():
            schemas += f"\nTable Name : {table} \n"
            schemas += f"\nTable Schema :  \n"
            schemas += self.show_schema(table)
        return schemas

    def execute_query(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]

        # calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(val)))

        # helper for formatting a row
        def format_row(row):
            return "| " + " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)) + " |"

        # print header separator
        line = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
        print(line)
        print(format_row(headers))
        print(line)

        # print rows
        for row in rows:
            print(format_row(row))
        print(line)

        return headers, rows

       

    def close(self, commit=False):
        if commit:
            self.conn.commit()
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    db = SQL(user=USER, password=PASSWWORD, database=DATABASE)
    db.connect()
    db.show_tables()
    db.show_schema("users")  
    db.close()
