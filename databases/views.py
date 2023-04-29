from django.shortcuts import render, HttpResponse
import redis
from .utils.mysql.utils import create_mysql_connection
from .models import Connection

mysql_connections = {}


def get_mysql_connection(connection_name, connectionObj):
    try:
        conn = mysql_connections[connection_name]
    except KeyError:
        conn = create_mysql_connection(connectionObj.properties__host, 
                                        connectionObj.properties__user, 
                                        connectionObj.properties__password, 
                                        connectionObj.properties__port, 
                                        connectionObj.properties__db
                                        )
        mysql_connections[connection_name] = conn
        
    return conn


def get_connection_metadata(request, connection_name):
    connectionObj = Connection.objects.get(name=connection_name)

    if connectionObj.type == 'mysql':
        conn = get_mysql_connection(connection_name, connectionObj)

        requirement = request.POST.get('requirement')
        if requirement == 'GET_TABLES':
            cursor = conn.cursor()
            cursor.execute("SHOW TABLES;")
            data = cursor.fetchall()
            cursor.close()
            return data 
        elif requirement == 'GET_TABLE_DETAILS':
            table_name = request.POST.get('table_name')
            cursor = conn.cursor()
            cursor.execute("use table_name")
            cursor.execute("SHOW TABLES DETAILS;")
            data = cursor.fetchall()
            cursor.close()
            return data 

    return HttpResponse("OK")