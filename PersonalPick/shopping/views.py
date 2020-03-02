from rest_framework.views import APIView
from rest_framework.response import Response

from PIL import Image
from core.classifier import Classifier


CATEGORY = 4


class ProductQuery(APIView):
    """
    Product recommendation request
    """
    def post(self, request, *args, **kwargs):
        pil_img = Image.open(request.FILES['file'])

        classifier = Classifier(CATEGORY)  # parameter : 분류할 클래스의 개수
        result = classifier.classify(input_image=pil_img)
        print(result)
        return Response({'message': 'success'})
