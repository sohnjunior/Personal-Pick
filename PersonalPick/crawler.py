import os
import sys
import ssl
import json
import urllib.request

import re
import django


# Python이 실행될 때 DJANGO_SETTINGS_MODULE 라는 환경 변수에 현재 프로젝트의 settings.py 파일 경로를 등록
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듬
django.setup()

from shopping.models import Product, Category
from django.core.exceptions import ObjectDoesNotExist

# -- load secrets.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'PersonalPick/secrets.json')) as f:
    secrets = json.load(f)


# -- 스트링에 포함된 html 태그 삭제
def remove_tag(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# -- 카테고리 분류를 위한 이미지 크롤링
'''
categories = ['남성의류', '여성의류', '여성 언더웨어', '남성 언더웨어', '여성신발', '남성신발', '가방', '지갑', '시계',
              '주얼리', '모자', '기타잡화', '휴대폰', '노트북', 'PC', '태블릿PC', '모니터', '계절가전', '생활가전', '주방가전',
              '음향가전', '침실가구', '거실가구', '사무용가구']
'''
categories = ['사무용가구']


def update_shopping_data(image_per_category, mode):
    # check directory
    asset_path = os.path.join(BASE_DIR, 'PersonalPick/core/assets/product')
    if not os.path.exists(asset_path):
        os.mkdir(asset_path)

    client_id = secrets['client_id']
    client_secret = secrets['client_secret']
    ssl._create_default_https_context = ssl._create_unverified_context  # for https request

    for category in categories:
        # create directory for saving
        category_path = os.path.join(asset_path, category)
        if not os.path.exists(category_path):
            os.mkdir(category_path)

        # naver shopping api 에서 한번에 요청가능한 최대 개수가 100개이므로 이를 위해 나눠서 요청
        start = 1
        repeat = image_per_category // 100 if image_per_category // 100 else 1
        image_per_repeat = image_per_category if image_per_category <= 100 else 100

        for _ in range(repeat):
            encCategory = urllib.parse.quote(category)
            url = "https://openapi.naver.com/v1/search/shop?query=" + encCategory + \
                  "&display=" + str(image_per_repeat) + "&start=" + str(start) + "&sort=sim"
            start += 100

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
                    image_name = item['productId']
                    product_type = int(item['productType'])

                    if mode == 'CLASSIFICATION':
                        try:
                            save_path = category_path + '/' + image_name + '.jpg'
                            if not os.path.exists(save_path):
                                urllib.request.urlretrieve(img_url, save_path)
                        except Exception as e:
                            print(f'image saving fail [category: {category}, productID: {image_name}]')
                            continue
                    elif mode == 'DB':
                        # ignore 단종상품
                        if product_type == 7 or product_type == 8 or product_type == 9:
                            continue

                        product_name = remove_tag(item['title'])
                        product_link = item['link']
                        mall_name = item['mallName']

                        # create new record
                        try:
                            c = Category.objects.get(name=category)  # find category object
                        except ObjectDoesNotExist:
                            c = Category(name=category)
                            c.save()

                        new_product = Product(title=product_name, link=product_link, image=img_url,
                                              mallName=mall_name, category=c)
                        new_product.save()
            else:
                print('Error Code:' + rescode)


# function test
if __name__ == '__main__':
    update_shopping_data(image_per_category=400, mode='CLASSIFICATION')
    # update_shopping_data(image_per_category=1, mode='DB')


