from rest_framework.views import APIView
from rest_framework.response import Response

from PIL import Image
from core.classifier import Classifier
from .serializers import ProductSerializer

from .models import Category, Product
from .utils import recommend_products
import unicodedata


class ProductQuery(APIView):
    """
    Product recommendation request
    """
    def post(self, request, *args, **kwargs):
        pil_img = Image.open(request.FILES['file'])

        # classify category
        classifier = Classifier(35)  # parameter : 분류할 클래스의 개수
        predicted = classifier.classify(input_image=pil_img)
        predicted = unicodedata.normalize('NFC', predicted)  # mac os 한글 자모 분리 이슈 해결

        # load all objects for target category
        category = Category.objects.get(name=predicted)
        products = category.product_set.all()

        # compare embedded feature map
        query_image = classifier.embedding(pil_img)
        targets = [{'pk': product.id, 'feature_map': product.image_embedded} for product in products]
        recommended = recommend_products(query=query_image, targets=targets, how_many=1)
        print(recommended)
        # find product instances with pk and serializing it
        param = [p.pk for p in recommended]
        query_set = Product.objects.filter(id__in=param)
        serializer = ProductSerializer(query_set, many=True)
        print(serializer.data)
        # response with most relevant images
        return Response(serializer.data)
