from django.shortcuts import render, HttpResponse
import redis
from .utils.mysql.utils import create_mysql_connection
from .models import Connection
from .serializers import ConnectionSerializer
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def connection_list(request):

    if request.method == 'GET':
        snippets = Connection.objects.filter(user=request.user)
        serializer = ConnectionSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ConnectionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class ConnectionDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Connection.objects.get(pk=pk)
        except Connection.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        conn = self.get_object(pk)
        serializer = ConnectionSerializer(conn)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        conn = self.get_object(pk)
        serializer = ConnectionSerializer(conn, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        conn = self.get_object(pk)
        conn.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    