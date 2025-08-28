from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.getAllProductsView, name='get_all_products'),
    path('product/<int:productId>/', views.getProductsView, name='get_product_by_name'),
    path('products/<int:producttype>/', views.getProductsByTypeView, name='get_products_by_type'),
    path('category/',views.getProductTypeView,name ='get_product_type'),
    path('locations/', views.GetLocations, name='get_locations'),
    path('citys/', views.GetCitys, name='get_citys'),
    path('location-page/<int:locationId>/',views.GetLocationPage,name='get_about_page'),
    path("blogs/",views.getAllBlogsView,name="get_all_blogs"),
    path("blog/<int:blogId>/",views.getBlogView,name="get_all_blogs"),
    path("hero/",views.getHeroImagesView,name="get_hero_image"),
    path("gallery/",views.getGalleryImage,name="get_gallery"),
    path("testimonials/",views.getTestimonialView,name="get_testimonial"),
    path("client-logos/",views.getClientLogoView,name="get_client_logos"),
    path("product-dropdown/",views.getProductDropdownView,name="get_product_dropdown"),
]

#hiteshuser
#hiteshpass