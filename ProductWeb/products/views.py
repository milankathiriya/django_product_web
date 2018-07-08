from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core import serializers
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import ProductSerializer
from django.views.decorators.csrf import csrf_exempt



# API related views -------------------------------------------------------------------------------


# [1] Using viewsets----

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# end [1] -------------------------------------------


# [2] Using FBV (Function Based Views)

@csrf_exempt
def FBVProducts(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many = True)
        return JsonResponse(serializer.data, safe = False)
    elif request.method == 'POST':
        jp = JSONParser()
        # print("DATA: " , request.body)
        # data = jp.parse(request.body)
        data = jp.parse(request)
        serializer = ProductSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.data.errors, status = 400)


@csrf_exempt
def FBVProducts_details(request, id):
    try:
        instance = Product.objects.get(id=id)
    except Product.DoesNotExist as e:
        return JsonResponse({'error': 'Given product object not found.'}, status = 404)

    if request.method == 'GET':
        serializer = ProductSerializer(instance)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        jp = JSONParser()
        data = jp.parse(request)
        serializer = ProductSerializer(instance, data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200)
        return JsonResponse(serializer.errors, status = 400)

    elif request.method == 'DELETE':
        instance.delete()
        return HttpResponse(status = 204)

# end [2] ------------------------------------------


# [3] Using CBV (Class Based Views)

class CBVProducts(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status = 200)

    def post(self, request):
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status = 400)


class CBVProducts_details(APIView):
    def get_object(self, id):
        try:
            return Product.objects.get(id = id)
        except Product.DoesNotExist:
            return Response({'error': 'Given product object not found.'}, status = 404)

    def get(self, request, id, format=None):
        product = self.get_object(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        product = self.get_object(id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id, format=None):
        product = self.get_object(id)
        product.delete()
        return Response(status=204)

# end [3] ------------------------------------------


# [4] Generics view and Mixins based view ----------

class GMProducts(generics.GenericAPIView, mixins.ListModelMixin,
                                          mixins.CreateModelMixin,
                                          mixins.UpdateModelMixin,
                                          mixins.RetrieveModelMixin,
                                          mixins.DestroyModelMixin):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminUser]
    permission_classes = [IsAuthenticated]

    def get(self, request, id = None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    # execute below method automatically when calling above post method
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

    def put(self, request, id = None):
        return self.update(request, id)

    # execute below method automatically when calling above put method
    def perform_update(self, serializer):
        serializer.save(owner = self.request.user)

    def delete(self, request, id = None):
        return self.destroy(request, id)

# end [4] ------------------------------------------

# -------------------------------------------------------------------------------------------------




# Create your views here.

def products_list(request):
    products = Product.objects.all().order_by('-date')
    updated_date = serializers.serialize( "python", Product.objects.all(), fields=('updated_date'))
    return render(request, 'products/products_list.html', {'products': products, 'updated_date': updated_date})

def products_detail(request, id):
    product = Product.objects.get(id = id)
    updated_date = serializers.serialize( "python", Product.objects.all(), fields=('updated_date'))
    return render(request, 'products/products_detail.html', {'product': product, 'updated_date': updated_date})

@login_required(login_url='/accounts/login/')
def product_create(request):
    if request.method == 'POST':
        form = CreateProduct(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.owner = request.user
            instance.save()
            return redirect('products:list')
    else:
        form = CreateProduct()
    return render(request, 'products/products_create.html', {'form': form})


def product_edit(request, id):
    product = Product.objects.get(id = id)
    if request.method == 'POST':
        form = CreateProduct(request.POST, request.FILES, instance = product)
        if form.is_valid():
            form.save()
            return redirect("products:list")
    return render(request, 'products/product_edit.html', {'product': product})


def product_delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("products:list")
