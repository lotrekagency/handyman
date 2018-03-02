from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Domain
from .serializer import DomainSerializer


class ProductList(APIView):
    def get(self, request, format=None):
        products = Domain.objects.all()
        serializer = DomainSerializer(products, many=True)
        return Response(serializer.data)