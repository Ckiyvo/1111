from rest_framework import serializers
from .models import DataResource

class DataResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataResource
        fields = '__all__'