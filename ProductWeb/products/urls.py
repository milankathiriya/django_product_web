from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_list, name = 'list'),
    path('create/', views.product_create, name='create'),
    path('<int:id>/', views.products_detail, name='detail'),
    path('edit/<int:id>/', views.product_edit, name='edit'),
    path('delete/<int:id>/', views.product_delete, name='delete'),
]
