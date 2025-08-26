from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.getAllProductsView, name='get_all_products'),
    path('product/', views.getProductsView, name='get_product_by_name'),
    path('products/<str:producttype>/', views.getProductsByTypeView, name='get_products_by_type'),
]
