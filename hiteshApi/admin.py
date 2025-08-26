from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Product)
admin.site.register(models.ProductType)
admin.site.register(models.ProductDescription)
admin.site.register(models.BaseUrl)
admin.site.register(models.State)
admin.site.register(models.Location)
admin.site.register(models.LocationPage)
admin.site.register(models.ProductImage)