from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.getAllProductsView, name='get_all_products'),
    path('product/<int:productId>/', views.getProductsView, name='get_product_by_name'),
    path('products/<int:producttype>/', views.getProductsByTypeView, name='get_products_by_type'),
    path('locations/', views.GetLocations, name='get_locations'),
    path('citys/', views.GetCitys, name='get_citys'),
    path('location-page/<int:locationId>/',views.GetLocationPage,name='get_about_page'),
]

#hiteshuser
#hiteshpass