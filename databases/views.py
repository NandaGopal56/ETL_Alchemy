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
        

    return HttpResponse("OK")