from .models import Domain
from rest_framework import serializers


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'