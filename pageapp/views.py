from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Gullar,Category
from .serializers import CategorySerializers,GullarSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
# Create your views here.

class ListCreateApi(APIView):
    def get(self,request):
        gullar = Gullar.objects.all()
        category = request.GET.get('category')
        name = request.GET.get('name')
        price = request.GET.get('price')
        price_gt = request.GET.get('price_gt')
        price_lt = request.GET.get('price_lt')
        search = request.GET.get('search')
        ordering = request.GET.get("ordering")
        if category:
            gullar = gullar.filter(category = category)
        if name:
            gullar = gullar.filter(name__icontains=name)
        if price:
            gullar = gullar.filter(price = price)
        if price_gt:
            gullar = gullar.filter(price__gt = price_gt)
        if price_lt:
            gullar = gullar.filter(price__lt = price_lt)
        if search:
            gullar = gullar.filter(Q(name__icontains = search) | Q(price__icontains = search))
        if ordering:
            gullar = gullar.order_by(ordering)
        paginator = PageNumberPagination()
        paginator.page_size = 3
        result_page = paginator.paginate_queryset(gullar,request)
        serializers = GullarSerializer(result_page , many=True)
        return paginator.get_paginated_response(serializers.data)

    def post(self,request):
        serializer = GullarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data,"status":status.HTTP_200_OK})
        return Response({'data': serializer.errors, "status": status.HTTP_400_BAD_REQUEST})

class DetailUpdateDeleteApi(APIView):
    def get(self,request,pk):
        gullar = Gullar.objects.get(id = pk)
        serializer = GullarSerializer(gullar)
        return Response({'data': serializer.data, "status": status.HTTP_200_OK})

    def put(self,request,pk):
        gullar = Gullar.objects.get(id = pk)
        serializer = GullarSerializer(gullar,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, "status": status.HTTP_200_OK})
        return Response({'data': serializer.errors, "status": status.HTTP_400_BAD_REQUEST})

    def patch(self,request,pk):
        gullar = Gullar.objects.get(id = pk)
        serializer = GullarSerializer(gullar,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, "status": status.HTTP_200_OK})
        return Response({'data': serializer.errors, "status": status.HTTP_400_BAD_REQUEST})

    def delete(self,request,pk):
        gullar = Gullar.objects.get(id=pk)
        gullar.delete()
        return Response({'data': "O'chirildi", "status": status.HTTP_200_OK})




