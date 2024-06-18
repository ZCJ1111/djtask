import sqlite3

def create_connection(sqlite_file):
    conn = None
    try:
        conn = sqlite3.connect(sqlite_file)
        print("Connected to SQLite database version:", sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    return conn

def list_tables(conn):
    
    cur = conn.cursor()
    sql = "SELECT name FROM sqlite_master WHERE type='table';"
    cur.execute(sql)
    
    tables = cur.fetchall()
    print("Tables in the database:\n")
    for table in tables:
        print(table[0])

def query_table(conn, table_name):
    
    cur = conn.cursor()
    sql = "SELECT * FROM {}".format(table_name)
    cur.execute(sql)
    rows = cur.fetchall()
    print("Data in table {}:".format(table_name))
    for row in rows:
        print(row)

def delete_data(conn, table_name, name):
    cur = conn.cursor()
    sql = "DELETE FROM {} WHERE  name=?".format(table_name)
    cur.execute(sql, (name,))
    conn.commit()


if __name__ == "__main__":
    db = 'db.sqlite3'
    conn = create_connection(db)
    delete_data(conn,'users','User0001')
