import os
import sys
import ssl
import json
import urllib.request

import re
import django

import base64
import pickle
from urllib.request import urlopen
from PIL import Image
from core.classifier import Classifier


# Python이 실행될 때 DJANGO_SETTINGS_MODULE 라는 환경 변수에 현재 프로젝트의 settings.py 파일 경로를 등록
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듬
django.setup()

from shopping.models import Product, Category
from django.core.exceptions import ObjectDoesNotExist

# -- load secrets.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'PersonalPick/config/secrets.json')) as f:
    secrets = json.load(f)


def remove_tag(text):
    """
    remove html tag in text

    :param text: text for check
    :return: text without html tag
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# -- 28개 카테고리 분류를 위한 이미지 크롤링
categories = [
    '귀걸이', '남성화', '넥타이', '드레스', '모자', '목걸이', '바지',
    '반바지', '반지', '백팩', '벨트', '브래지어', '샌들', '선글라스',
    '셔츠', '스웨터', '스웻셔츠', '시계', '양말', '여성화', '운동화',
    '재킷', '지갑', '치마', '티셔츠', '팔찌', '팬티', '핸드백'
]


def update_shopping_data(image_per_category):
    """
    update shopping data for database

    :param image_per_category: image quantities per category
    :return: None
    """
    # check directory
    asset_path = os.path.join(BASE_DIR, 'PersonalPick/core/assets/product')
    if not os.path.exists(asset_path):
        os.mkdir(asset_path)

    client_id = secrets['client_id']
    client_secret = secrets['client_secret']
    ssl._create_default_https_context = ssl._create_unverified_context  # for https request
    check_point = 1  # TODO 매 호출시 체크 포인트로 확인
    for category in categories:
        # create directory for saving
        category_path = os.path.join(asset_path, category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)

        # naver shopping api 에서 한번에 요청가능한 최대 개수가 100개이므로 이를 위해 나눠서 요청
        start = 51
        repeat = image_per_category // 100 if image_per_category // 100 else 1
        image_per_repeat = image_per_category if image_per_category <= 100 else 100

        for _ in range(repeat):
            encCategory = urllib.parse.quote(category)
            url = "https://openapi.naver.com/v1/search/shop?query=" + encCategory + \
                  "&display=" + str(image_per_repeat) + "&start=" + str(start) + "&sort=sim"
            start += 100  # TODO 호출 시작 포인트

            # create request
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", client_id)
            request.add_header("X-Naver-Client-Secret", client_secret)

            # request
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
            if rescode == 200:
                response_body = response.read().decode('utf-8')
                res_data = json.loads(response_body)

                # for all response items
                for item in res_data['items']:
                    img_url = item['image']
                    product_type = int(item['productType'])

                    # ignore 단종상품
                    if product_type == 7 or product_type == 8 or product_type == 9:
                        continue

                    product_name = remove_tag(item['title'])
                    product_link = item['link']
                    low_price = item['lprice']
                    high_price = item['hprice']
                    mall_name = item['mallName']

                    # find Category table
                    try:
                        c = Category.objects.get(name=category)  # find category object
                    except ObjectDoesNotExist:
                        c = Category(name=category)
                        c.save()

                    # create embedded image
                    classifier = Classifier(28)
                    pil_img = Image.open(urlopen(img_url)).convert('RGB')
                    feature_map = classifier.embedding(input_image=pil_img)

                    # convert tensor to numpy array
                    feature_map = feature_map.data.numpy()
                    feature_bytes = pickle.dumps(feature_map)
                    feature_base64 = base64.b64encode(feature_bytes)

                    # create new record
                    new_product = Product(title=product_name, link=product_link, image=img_url,
                                          lprice=low_price, hprice=high_price, image_embedded=feature_base64,
                                          mallName=mall_name, category=c)
                    new_product.save()
                    print(check_point)
                    check_point += 1
            else:
                print('Error Code:' + rescode)


# function test
if __name__ == '__main__':
    update_shopping_data(image_per_category=50)


