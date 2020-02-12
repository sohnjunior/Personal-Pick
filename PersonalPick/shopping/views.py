from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from PIL import Image
from core.classifier import Classifier


# 요청 상품 이미지 처리
@method_decorator(csrf_exempt, name='dispatch')
class ProductQuery(View):

    def post(self, request, *args, **kwargs):
        pil_img = Image.open(request.FILES['file'])

        classifier = Classifier(4)
        result = classifier.classify(input_image=pil_img)
        print(result)
        return JsonResponse({'message': 'success'})
