from rest_framework.decorators import api_view
from .models import Product, ProductType, BaseUrl
from django.shortcuts import get_object_or_404
from .messages.ResponseBack import ResponseBack, LocalResponseBack
from .messages.ResponseCode import ResponseCode
from .messages.ResponseMessage import ResponseMessage


def get_base_url():
    base_url_obj = BaseUrl.objects.first()
    return base_url_obj.url if base_url_obj else ''


def getProductData(product):
    try:
        base_url = get_base_url()

        data = {
            "id": product.id,
            "Name": product.Name,
            "About": product.About,
            "Rating": float(product.Rating),
            "Tag": product.Tag,
            "KeyFeatures": product.KeyFeatures,
            "NoOfReviews": product.NoOfReviews,
            "ProductType": product.ProductType.Value if product.ProductType else None,
            "RelatedProducts": [rel.Name for rel in product.RelatedProducts.all()],
            "Images": [base_url + img.Image.url for img in product.Images.all()],
            "Description": {
                "Description": product.Description.Description,
                "KeyPoints": product.Description.KeyPoints
            } if hasattr(product, 'Description') else {},
            "Specification": product.Specification.Specification if hasattr(product, 'Specification') else {},
            "Application": product.Application.Value if hasattr(product, 'Application') else {},
            "TechnicalAdvantage": product.TechnicalAdvantage.Value if hasattr(product, 'TechnicalAdvantage') else {},
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
            result = getProductData(product)
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
def getProductsView(request):
    try:
        name = request.GET.get('name')
        if not name:
            return ResponseBack(
                message=ResponseMessage.MISSING_NAME_PARAM,
                data={},
                code=ResponseCode.FAILURE
            )

        product = Product.objects.filter(Name=name).first()
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
        type_value = request.GET.get('type')
        if not type_value:
            return ResponseBack(
                message=ResponseMessage.MISSING_TYPE_PARAM,
                data={},
                code=ResponseCode.FAILURE
            )

        product_type = ProductType.objects.filter(Value=producttype).first()
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
            result = getProductData(product)
            if result.code == ResponseCode.SUCCESS:
                data_list.append(result.data)

        return ResponseBack(
            message=f"{ResponseMessage.PRODUCTS_FOUND} of type '{type_value}'",
            data=data_list,
            code=ResponseCode.SUCCESS
        )

    except Exception as e:
        return ResponseBack(
            message=str(e),
            data={},
            code=ResponseCode.FAILURE
        )
