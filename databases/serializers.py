from rest_framework import serializers
from .models import Connection

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'

    def get(self, validated_data):
        # Custom get method logic here
        pass

    def create(self, validated_data):
        # Custom create method logic here
        pass
