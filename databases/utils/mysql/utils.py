import pymysql

def create_mysql_connection(host, user, password, port=3306, db=None):
    """Creates a connection to the MySQL database"""
    connection = pymysql.connect(
        host = host,
        user = user,
        password = password,
        port = port,
        db = db,
    )
    return connection

def execute_query(cursor, query, params=None):
    """Executes a SQL query"""
    
    cursor.execute(query, params)
    result = cursor.fetchall()
    
    return result
