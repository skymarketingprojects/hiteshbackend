from django.db import models
from django_quill.fields import QuillField
from .UTILS.Names import Names

class ProductType(models.Model):
    Value = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.Value
class ProductBroucher(models.Model):
    File = models.FileField(upload_to='brouchers/')


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

    Broucher = models.ForeignKey(ProductBroucher, on_delete=models.SET_NULL, null=True, blank=True)
    Warranty = models.CharField(max_length=200,default="")
    Shipping = models.CharField(max_length=200,default="")
    Specification = models.JSONField(default=list,help_text='json format [\n{"label": "Roller Size",\n"value": "127 x 63mm (5\" x 2.5\")"\n}\n]')
    Application = models.JSONField(default=list,help_text='json format ["Jewelry sheet rolling","Wire rolling and reduction","Craft and custom metal forming"]')
    TechnicalAdvantage = models.JSONField(default=list,help_text='json format ["Compact footprint","Minimal maintenance required"]')

    def __str__(self):
        return f"{self.id} - {self.Name}"
        # if self.ProductType:
        #     return f"{self.Name} - {self.ProductType.Value}"
        # return f"{self.Name}"

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
    Image = models.ImageField(upload_to='Location_images/')

    TopParagraph = models.JSONField(default=list,null=True, blank=True)
    Heading = models.CharField(max_length=100, null=True, blank=True)
    SubHeading = models.CharField(max_length=100, null=True, blank=True)
    BottomParagraph = models.JSONField(default=list,null=True, blank=True)

    MetaTitle = models.CharField(max_length=100, null=True, blank=True)
    MetaDescription = models.CharField(max_length=100, null=True, blank=True)
    MetaKeywords = models.CharField(max_length=100, null=True, blank=True)
    MetaUrl = models.CharField(max_length=100, null=True, blank=True)
    MetaCanonical = models.CharField(max_length=100, null=True, blank=True)

class PageBanner(models.Model):
    page = models.ForeignKey(LocationPage,related_name='banners',on_delete=models.CASCADE)
    bannerImage = models.ImageField(upload_to='page_banners/')
    index = models.IntegerField(default=99)
    def save(self, *args, **kwargs):
        indexShifting(self)
        super().save(*args, **kwargs)
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

class ClientLogo(models.Model):
    image = models.ImageField(upload_to='client_logos/')
    index = models.IntegerField(default=99)

    def save(self, *args, **kwargs):
        indexShifting(self)
        super().save(*args, **kwargs)

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    image = models.ImageField(upload_to='testimonials/')
    content = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return self.name

class HeroImages(models.Model):
    image = models.ImageField(upload_to="banner/")
    index = models.IntegerField(default=99)

    def save(self, *args, **kwargs):
        indexShifting(self)
        super().save(*args, **kwargs)

class HomeVideo(models.Model):
    video = models.FileField(upload_to="homeVideo/videos/")
    fallback = models.ImageField(upload_to="homeVideo/fallback/", null=True, blank=True)

class Gallery(models.Model):
    image = models.ImageField(upload_to="gallery/")
    ProductType = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
    index = models.IntegerField(default=99)
    def save(self, *args, **kwargs):
        indexShifting(self)
        super().save(*args, **kwargs)


def shiftUp(model_class: models.Model, start_index: int, exclude_pk=None):
    """
    Increments the index of all instances from `start_index` onward.
    """
    objects = model_class.objects.filter(index__gte=start_index)
    if exclude_pk:
        objects = objects.exclude(pk=exclude_pk)
    objects = list(objects.order_by(f"-{Names.INDEX}"))

    for obj in objects:
        obj.index += 1

    model_class.objects.bulk_update(objects, [Names.INDEX])


def shiftDown(model_class: models.Model, start_index: int, end_index: int, exclude_pk=None):
    """
    Decrements the index of all instances between start_index and end_index.
    """
    objects = model_class.objects.filter(index__gte=start_index, index__lt=end_index+1)
    if exclude_pk:
        objects = objects.exclude(pk=exclude_pk)
    objects = list(objects.order_by(Names.INDEX))

    for obj in objects:
        obj.index -= 1

    model_class.objects.bulk_update(objects, [Names.INDEX])


def shiftUpRange(model_class: models.Model, start_index: int, end_index: int, exclude_pk=None):
    """
    Increments the index of all instances between start_index and end_index.
    """
    objects = model_class.objects.filter(index__gt=start_index-1, index__lte=end_index)
    if exclude_pk:
        objects = objects.exclude(pk=exclude_pk)
    objects = list(objects.order_by(f"-{Names.INDEX}"))

    for obj in objects:
        obj.index += 1

    model_class.objects.bulk_update(objects, [Names.INDEX])

def indexShifting(instance: models.Model):
    model_class = instance.__class__

    if instance.pk:
        old_index = model_class.objects.get(pk=instance.pk).index

        if old_index < instance.index:
            shiftDown(model_class, old_index, instance.index, exclude_pk=instance.pk)
        elif old_index > instance.index:
            shiftUpRange(model_class, instance.index, old_index, exclude_pk=instance.pk)

    else:
        if model_class.objects.filter(index=instance.index).exists():
            shiftUp(model_class, instance.index)
