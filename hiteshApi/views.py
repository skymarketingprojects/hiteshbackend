from rest_framework.decorators import api_view
from .models import Product, ProductType, BaseUrl,Location,State,Blog,HeroImages,Gallery,Testimonial,ClientLogo
from django.shortcuts import get_object_or_404
from .messages.ResponseBack import ResponseBack, LocalResponseBack
from .messages.ResponseCode import ResponseCode
from .messages.ResponseMessage import ResponseMessage
from .UTILS.Names import Names
import re

@api_view(['GET'])
def getAllProductsView(request):
    try:
        products = Product.objects.all()
        
        if not products.exists():
            return ResponseBack(
                message=ResponseMessage.PRODUCTS_NOT_FOUND,
                data=[],
                code=ResponseCode.FAILURE
            )

        data_list = []
        for product in products:
            result = getProductDisplayData(product)
            if result.code == ResponseCode.SUCCESS:
                data_list.append(result.data)
        productTypes = ProductType.objects.all()
        typeData = []
        for prodType in productTypes:
            tempData = {
                Names.ID:prodType.id,
                Names.NAME:prodType.Value
            }
            typeData.append(tempData)

        return ResponseBack(
            message=ResponseMessage.PRODUCTS_FOUND,
            data={Names.PRODUCTS:data_list,Names.PRODUCT_TYPE:typeData},
            code=ResponseCode.SUCCESS
        )

    except Exception as e:
        return ResponseBack(
            message=str(e),
            data={},
            code=ResponseCode.FAILURE
        )


@api_view(['GET'])
def getProductsView(request,productId):
    try:
        
        product = Product.objects.filter(id=productId).first()
        if not product:
            return ResponseBack(
                message=ResponseMessage.PRODUCT_NOT_FOUND,
                data={},
                code=ResponseCode.FAILURE
            )

        result = getProductData(product)
        if result.code == ResponseCode.SUCCESS:
            return ResponseBack(
                message=ResponseMessage.PRODUCT_FOUND,
                data=result.data,
                code=ResponseCode.SUCCESS
            )
        else:
            return ResponseBack(
                message=result.message,
                data={},
                code=ResponseCode.FAILURE
            )

    except Exception as e:
        return ResponseBack(
            message=str(e),
            data={},
            code=ResponseCode.FAILURE
        )


@api_view(['GET'])
def getProductsByTypeView(request,producttype):
    try:

        product_type = ProductType.objects.filter(id=producttype).first()
        if not product_type:
            return ResponseBack(
                message=ResponseMessage.PRODUCT_TYPE_NOT_FOUND,
                data={},
                code=ResponseCode.FAILURE
            )

        products = Product.objects.filter(ProductType=product_type)
        if not products.exists():
            return ResponseBack(
                message=ResponseMessage.PRODUCTS_NOT_FOUND,
                data=[],
                code=ResponseCode.FAILURE
            )

        data_list = []
        for product in products:
            result = getProductDisplayData(product)
            if result.code == ResponseCode.SUCCESS:
                data_list.append(result.data)

        return ResponseBack(
            message=ResponseMessage.PRODUCTS_FOUND,
            data=data_list,
            code=ResponseCode.SUCCESS
        )

    except Exception as e:
        return ResponseBack(
            message=str(e),
            data={},
            code=ResponseCode.FAILURE
        )

@api_view(['GET'])
def GetLocations(request):
    try:
        locations = Location.objects.all()
        locations_data = []
        for location in locations:
            locadata = {
                Names.LABLE: location.lable,
                Names.NAME: location.name,
                Names.ID: location.id}
            locations_data.append(locadata)
        return ResponseBack(
            code=ResponseCode.SUCCESS,
            message=ResponseMessage.LOCATION_FOUND_SUCESS,
            data=locations_data)
    except Exception as e:
        return ResponseBack(
            message=ResponseMessage.LOCATION_FOUND_ERROR,
            code=ResponseCode.ERROR,
            data=str(e))

@api_view(['GET'])
def GetCitys(request):
    try:
        states = State.objects.all()
        states_data = []
        for state in states:
            statelocations = state.locations.all()
            locations_data = []
            for location in statelocations:
                locadata = {
                    Names.LABLE: location.lable,
                    Names.NAME: location.name,
                    Names.ID: location.id,
                    Names.IMAGE: Names.BASE_URL + location.image.url}
                locations_data.append(locadata)
            state_data = {
                Names.NAME: state.name,
                Names.LOCATIONS: locations_data
            }
            states_data.append(state_data)
        return ResponseBack(
            code=ResponseCode.SUCCESS,
            message=ResponseMessage.LOCATION_FOUND_SUCESS,
            data=states_data)
    except Exception as e:
        return ResponseBack(
            message=ResponseMessage.LOCATION_FOUND_ERROR,
            code=ResponseCode.ERROR,
            data=str(e))

@api_view(['POST'])
def GetLocationPage(request,locationId):
    try:
        loc = request.data.get(Names.LOCATION)
        location = Location.objects.filter(id=locationId).first()
        page = location.locationpage.first()
        data = {
            Names.TITLE: page.Title,
            Names.DESCRIPTION: page.Description,
            Names.IMAGE: Names.BASE_URL + page.BannerImage.url,
            Names.META_TITLE: page.MetaTitle,
            Names.META_DESCRIPTION: page.MetaDescription,
            Names.META_KEYWORD: page.MetaKeywords,
            Names.META_URL: page.MetaUrl,
            Names.META_CANONICALURL: page.MetaCanonical}
        return ResponseBack(
            code=ResponseCode.SUCCESS,
            message=ResponseMessage.ABOUT_FOUND_SUCESS,
            data=data)
    except Exception as e:
        return ResponseBack(
            message=ResponseMessage.ABOUT_FOUND_ERROR,
            code=ResponseCode.ERROR,
            data=str(e))

@api_view(['GET'])
def getAllBlogsView(request):
        try:
            blogs = Blog.objects.all()
            blogsdata = []
            for blog in blogs:
                data = getBlogData(blog)
                #if data.code == ResponseCodes.SUCCESS:
                blogsdata.append(data.data)
            return ResponseBack(message=ResponseMessage.BLOG_FOUND_SUCESS, data=blogsdata, code=ResponseCode.SUCCESS)
        except Exception as e:
            return ResponseBack(message=ResponseMessage.BLOG_FOUND_ERROR, data=str(e), code=ResponseCode.ERROR)

@api_view(['GET'])
def getBlogView(request,blogId):
    try:
        blog = Blog.objects.filter(id=blogId).first()
        blogresp = getBlogData(blog)
        return ResponseBack(
            message=blogresp.message,
            code=blogresp.code,
            data=blogresp.data
        )
    except Exception as e:
        return ResponseBack(message=ResponseMessage.BLOG_FOUND_ERROR, data=str(e), code=ResponseCode.ERROR)

@api_view(['GET'])
def getProductTypeView(request):
    try:
        productTypes = ProductType.objects.all()
        typeData = []
        for prodType in productTypes:
            tempData = {
                Names.ID:prodType.id,
                Names.NAME:prodType.Value
            }
            typeData.append(tempData)
        return ResponseBack(
            message=ResponseMessage.PRODUCT_TYPE_FOUND,
            data = typeData,
            code=ResponseCode.SUCCESS
        )
    except Exception as e:
        return ResponseBack(
            message=ResponseMessage.PRODUCT_TYPE_NOT_FOUND,
            data = str(e),
            code=ResponseCode.ERROR
        )

@api_view(['GET'])
def getHeroImagesView(request):
    try:
        images = HeroImages.objects.all()
        imageData = []
        baseUrl = get_base_url()
        for image in images:
            data = {
                Names.ID:image.id,
                Names.IMAGE:baseUrl+image.image.url,
                Names.INDEX:image.index
            }
            imageData.append(data)
        return ResponseBack(
            message=ResponseMessage.IMAGES_FOUND_SUCCESS,
            data=imageData,
            code=ResponseCode.SUCCESS
        )
    except Exception as e:
        return ResponseBack(
            message=ResponseMessage.IMAGE_FOUND_ERROR,
            data=str(e),
            code=ResponseCode.ERROR
        )

@api_view(['GET'])
def getGalleryImage(request):
    try:
        galleryImages = Gallery.objects.all()
        baseUrl = get_base_url()
        imageData = []
        for gallery in galleryImages:
            data= {
                Names.ID:gallery.id,
                Names.IMAGE:baseUrl+gallery.image.url,
                Names.INDEX: gallery.index,
                Names.PRODUCT_TYPE:{Names.NAME:gallery.ProductType.Value,Names.ID:gallery.ProductType.id} 
            }
            imageData.append(data)
        return ResponseBack(
            message=ResponseMessage.IMAGES_FOUND_SUCCESS,
            data=imageData,
            code=ResponseCode.SUCCESS
        )
    except Exception as e:
        return ResponseBack(
            message=ResponseMessage.IMAGE_FOUND_ERROR,
            data=str(e),
            code=ResponseCode.ERROR
        )

@api_view(['GET'])
def getTestimonialView(request):
    try:
        testimonials = Testimonial.objects.all()
        testimonialData = []
        baseUrl = get_base_url()
        for testimonial in testimonials:
            data = {
                Names.ID:testimonial.id,
                Names.NAME:testimonial.name,
                Names.POSITION:testimonial.position,
                Names.COMPANY:testimonial.company,
                Names.IMAGE: baseUrl+testimonial.image.url,
                Names.CONTENT:testimonial.content,
                Names.RATING:testimonial.rating
            }
            testimonialData.append(data)
        return ResponseBack(
            message=ResponseMessage.IMAGES_FOUND_SUCCESS,
            data=testimonialData,
            code=ResponseCode.SUCCESS
        )
    except Exception as e:
        return ResponseBack(
            message=ResponseMessage.IMAGE_FOUND_ERROR,
            data=str(e),
            code=ResponseCode.ERROR
        )  

@api_view(['GET'])
def getProductDropdownView(request):
    try:
        products = Product.objects.all()
        productData = []
        for product in products:
            slug = generate_blog_slug(product.Name, product.id)
            data = {
                Names.ID:product.id,
                Names.LABLE:product.Name,
                Names.URL:f"/products/{slug}"
            }
            productData.append(data)
        return ResponseBack(
            message=ResponseMessage.PRODUCTS_FOUND,
            data=productData,
            code=ResponseCode.SUCCESS
        )
    except Exception as e:
        return ResponseBack(
            message=str(e),
            data={},
            code=ResponseCode.FAILURE
        )
@api_view(['GET'])
def getClientLogoView(request):
    try:
        logos = ClientLogo.objects.all()
        logoData = []
        baseUrl = get_base_url()
        for logo in logos:
            data = {
                Names.ID:logo.id,
                Names.IMAGE: baseUrl+logo.image.url,
                Names.INDEX:logo.index
            }
            logoData.append(data)
        return ResponseBack(
            message=ResponseMessage.IMAGES_FOUND_SUCCESS,
            data=logoData,
            code=ResponseCode.SUCCESS
        )
    except Exception as e:
        return ResponseBack(
            message=ResponseMessage.IMAGE_FOUND_ERROR,
            data=str(e),
            code=ResponseCode.ERROR
        ) 
# ***************************** Helper functions *****************************

def get_base_url():
    base_url_obj = BaseUrl.objects.first()
    return base_url_obj.url if base_url_obj else Names.BASE_URL

def getBlogData( blog):
        try:
            base_url = Names.BASE_URL
            data = {
                Names.ID: blog.id,
                Names.TITLE: blog.title,
                Names.CONTENT: blog.text.html,
                Names.WRITER: blog.writer,
                Names.DESCRIPTION: blog.discription,
                Names.IMAGE_SQ: base_url + blog.image_sq.url,
                Names.IMAGE_HR: base_url + blog.image_hr.url,
                Names.CREATED_AT: blog.created_at
            }
            return LocalResponseBack(ResponseMessage.BLOG_FOUND_SUCESS, data=data, code=ResponseCode.SUCCESS)
        except Exception as e:
            return LocalResponseBack(ResponseMessage.BLOG_FOUND_ERROR, data=str(e), code=ResponseCode.ERROR)

def getProductDisplayData(product):
    try:
        base_url = get_base_url()

        slug = generate_blog_slug(product.Name, product.id)

        data = {
            Names.ID: product.id,
            Names.SLUG: slug,
            Names.NAME: product.Name,
            Names.ABOUT: product.About,
            Names.RATING: float(product.Rating),
            Names.IMAGE:base_url+product.Image.url,
            Names.PRICE: product.Price,
            Names.TAG: product.Tag,
            Names.KEY_FEATURES: product.KeyFeatures,
            Names.NO_OF_REVIEWS: product.NoOfReviews,
            Names.PRODUCT_TYPE: {Names.NAME:product.ProductType.Value,Names.ID:product.ProductType.id} if product.ProductType else None,
            Names.IMAGES: [base_url + img.Image.url for img in product.Images.all()],
        }

        return LocalResponseBack(
            message=ResponseMessage.PRODUCT_FOUND,
            data=data,
            code=ResponseCode.SUCCESS
        )

    except Exception as e:
        return LocalResponseBack(
            message=str(e),
            data={},
            code=ResponseCode.FAILURE
        )
def getProductData(product):
    try:
        base_url = get_base_url()
        related_products = []
        relProds = product.RelatedProducts.all()
        slug = generate_blog_slug(product.Name, product.id)
        for rel in relProds:
            reldata = getProductDisplayData(rel)
            if reldata.code == ResponseCode.SUCCESS:
                related_products.append(reldata.data)
        data = {
            Names.ID: product.id,
            Names.NAME: product.Name,
            Names.ABOUT: product.About,
            Names.SLUG: slug,
            Names.MODEL:product.Model,
            Names.SKU:product.Sku,
            Names.PRICE:product.Price,
            Names.WARRENTY:product.Warranty,
            Names.SHIPPING:product.Shipping,
            Names.ORIGNAL_PRICE:product.OrignalPrice,
            Names.RATING: float(product.Rating),
            Names.TAG: product.Tag,
            Names.KEY_FEATURES: product.KeyFeatures,
            Names.NO_OF_REVIEWS: product.NoOfReviews,
            Names.PRODUCT_TYPE:{Names.NAME:product.ProductType.Value,Names.ID:product.ProductType.id}  if product.ProductType else None,
            Names.RELATED_PRODUCTS: related_products,
            Names.IMAGES: [base_url + img.Image.url for img in product.Images.all()],
            Names.DESCRIPTION: product.Description.Description,
            Names.KEY_POINTS: product.Description.KeyPoints,
            Names.SPECIFICATION: product.Specification,
            Names.APPLICATION: product.Application,
            Names.TECHNICAL_ADVANTAGE: product.TechnicalAdvantage,
        }

        return LocalResponseBack(
            message=ResponseMessage.PRODUCT_FOUND,
            data=data,
            code=ResponseCode.SUCCESS
        )

    except Exception as e:
        return LocalResponseBack(
            message=ResponseMessage.PRODUCT_FOUND_ERROR,
            data=str(e),
            code=ResponseCode.FAILURE
        )

def generate_blog_slug(title, id):
    slug = title.lower()
    slug = slug.replace(" ", "-")
    slug = re.sub(r"[^\w\-]+", "", slug)
    return f"{slug}-{id}"