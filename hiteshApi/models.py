from django.db import models
from django_quill.fields import QuillField

class ProductType(models.Model):
    Value = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.Value

class Product(models.Model):
    Name = models.CharField(max_length=200)
    About = models.TextField()
    Model = models.CharField(max_length=200,default='')
    Sku = models.CharField(max_length=200,default='')
    Rating = models.DecimalField(max_digits=2, decimal_places=1)
    Tag = models.CharField(max_length=50)
    Price = models.CharField(max_length=10,default="0")
    OrignalPrice = models.CharField(max_length=10,default="0")
    Image = models.ImageField(upload_to='product_hero/',null=True,blank=True)
    KeyFeatures = models.JSONField(default=list,help_text=' json format ["feature1","feature2"]')
    NoOfReviews = models.IntegerField()
    ProductType = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
    RelatedProducts = models.ManyToManyField('self', blank=True)


    Warranty = models.CharField(max_length=200,default="")
    Shipping = models.CharField(max_length=200,default="")
    Specification = models.JSONField(default=list,help_text='json format [\n{"label": "Roller Size",\n"value": "127 x 63mm (5\" x 2.5\")"\n}\n]')
    Application = models.JSONField(default=list,help_text='json format ["Jewelry sheet rolling","Wire rolling and reduction","Craft and custom metal forming"]')
    TechnicalAdvantage = models.JSONField(default=list,help_text='json format ["Compact footprint","Minimal maintenance required"]')

    def __str__(self):
        return self.Name

class ProductDescription(models.Model):
    Product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='Description')
    Description = models.TextField()
    KeyPoints = models.JSONField()

class ProductImage(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='Images')
    Image = models.ImageField(upload_to='product_images/')

class BaseUrl(models.Model):
    url = models.URLField()

#states
class State(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

#location
class Location(models.Model):
    name = models.CharField(max_length=100)
    lable = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE,related_name='locations')
    image = models.ImageField(upload_to='Location_images/')
    def __str__(self):
        return f"{self.name}"

class LocationPage(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE,related_name='locationpage')
    BannerImage = models.ImageField(upload_to='Location_images/')

    Title = models.CharField(max_length=100, null=True, blank=True)
    Description = models.TextField(null=True, blank=True)

    MetaTitle = models.CharField(max_length=100, null=True, blank=True)
    MetaDescription = models.CharField(max_length=100, null=True, blank=True)
    MetaKeywords = models.CharField(max_length=100, null=True, blank=True)
    MetaUrl = models.CharField(max_length=100, null=True, blank=True)
    MetaCanonical = models.CharField(max_length=100, null=True, blank=True)

class Blog(models.Model):
    writer = models.CharField( max_length=50)
    title = models.CharField( max_length=200)
    image_sq = models.ImageField( upload_to='blog/images')
    image_hr = models.ImageField( upload_to='blog/images')
    discription = models.TextField(default="")
    text = QuillField()

    created_at = models.DateField( auto_now=True)

    def __str__(self):
        return self.title