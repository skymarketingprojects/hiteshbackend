from django.db import models

class ProductType(models.Model):
    Value = models.CharField(max_length=50, unique=True)

class Product(models.Model):
    Name = models.CharField(max_length=200)
    About = models.TextField()
    Rating = models.DecimalField(max_digits=2, decimal_places=1)
    Tag = models.CharField(max_length=50)
    KeyFeatures = models.TextField()
    NoOfReviews = models.IntegerField()
    ProductType = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
    RelatedProducts = models.ManyToManyField('self', blank=True)

class ProductDescription(models.Model):
    Product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='Description')
    Description = models.TextField()
    KeyPoints = models.TextField()

class ProductSpecification(models.Model):
    Product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='Specification')
    Specification = models.JSONField()

class Application(models.Model):
    Product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='Application')
    Value = models.JSONField()

class TechnicalAdvantage(models.Model):
    Product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='TechnicalAdvantage')
    Value = models.JSONField()

class ProductImage(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Images')
    Image = models.ImageField(upload_to='product_images/')

class BaseUrl(models.Model):
    url = models.URLField()
