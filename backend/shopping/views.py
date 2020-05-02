from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from PIL import Image
from .classifier import Classifier
from .serializers import ProductSerializer

from .models import Category, Product
from .utils import recommend_products
import unicodedata


class ProductQuery(APIView):
    """
    Product recommendation request
    """
    def post(self, request, format=None):
        pil_img = Image.open(request.FILES['file'])

        # classify category
        classifier = Classifier(28)  # parameter : 분류할 클래스의 개수
        predicted = classifier.classify(input_image=pil_img)
        predicted = unicodedata.normalize('NFC', predicted)  # mac os 한글 자모 분리 이슈 해결

        # load all objects for target category
        category = Category.objects.get(name=predicted)
        products = category.product_set.all()

        # compare embedded feature map
        query_image = classifier.embedding(pil_img)
        targets = [{'pk': product.id, 'feature_map': product.image_embedded} for product in products]
        recommended = recommend_products(query=query_image, targets=targets, how_many=30)

        # find product instances with pk and serializing it
        param = [p['pk'] for p in recommended]
        query_set = Product.objects.filter(id__in=param)
        serializer = ProductSerializer(query_set, many=True)

        # response with most relevant images
        return Response(serializer.data)


class ProductCart(APIView):
    """
    shopping cart
    """
    def get(self, request, format=None):
        user = request.user
        if user.is_authenticated:
            product_from_cart = user.product_set.all()
            serializer = ProductSerializer(product_from_cart, many=True)
            return Response(serializer.data)
        else:
            content = {'Validation Error': 'Not authorized user'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, format=None):
        user = request.user
        if user.is_authenticated:
            product_id = request.data['id']
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                content = {'Internal Server Error': 'Product not found'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            user.product_set.add(product)
            return Response({'message': 'Successfully added'})
        else:
            content = {'Validation Error': 'Not authorized user'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, format=None):
        user = request.user
        if user.is_authenticated:
            product_id = request.data['id']
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                content = {'Internal Server Error': 'Product not found'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            user.product_set.remove(product)
            return Response({'message': 'Successfully removed'})
        else:
            content = {'Validation Error': 'Not authorized user'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)

