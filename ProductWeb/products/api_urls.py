from django.urls import path, include
from . import views
from .views import *
from rest_framework import routers


# for using viewsets ---------------------

# router = routers.DefaultRouter()
# router.register('', views.ProductViewSet)

# ------------------------------------------

urlpatterns = [
    # path('', include(router.urls)),       # for using view sets
        path('FBVAPI/', views.FBVProducts),        # for FBV API to GET and POST
        path('FBVAPI/<int:id>/', views.FBVProducts_details),       # for FBV API to PUT and DELETE
        path('CBVAPI/', CBVProducts.as_view()),     # for CBV API to GET and POST
        path('CBVAPI/<int:id>/', CBVProducts_details.as_view()),      # for CBV API to PUT and DELETE
        path('GMAPI/', GMProducts.as_view()),       # for generics and mixins view API to GET and POST
        path('GMAPI/<int:id>/', GMProducts.as_view()),      # for generics and mixins view API to PUT and DELETE
]
