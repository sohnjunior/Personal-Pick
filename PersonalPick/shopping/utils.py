import os
import sys
import ssl
import json
import urllib.request


# -- load secrets.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'shopping/secrets.json')) as f:
    secrets = json.load(f)


# 카테고리 분류를 위한 이미지 크롤링
categories = ['남성의류', '여성의류', '여성 언더웨어', '남성 언더웨어', '여성신발', '남성신발', '가방', '지갑', '시계',
            '주얼리', '모자', '기타잡화', '휴대폰', '노트북', 'PC', '태블릿PC', '모니터', '계절가전', '생활가전', '주방가전',
            '음향가전', '침실가구', '거실가구', '사무용가구']


def crawl_category_image(category_per_image):
    # check directory
    asset_path = os.path.join(BASE_DIR, 'shopping/assets/product')
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

        encCategory = urllib.parse.quote(category)
        url = "https://openapi.naver.com/v1/search/shop?query=" + encCategory + \
              "&display=" + str(category_per_image) + "&start=1&sort=sim"

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

                if img_url == "":
                    continue

                try:
                    urllib.request.urlretrieve(img_url, category_path + '/' + image_name + '.jpg')
                except Exception as e:
                    print(f'image saving fail [category: {category}, productID: {image_name}]')
        else:
            print('Error Code:' + rescode)


# 주기적으로 쇼핑 데이터를 업데이트 한 후 DB에 저장한다. (단종 제외)
def update_shopping_data():
    pass


# function test
if __name__ == '__main__':
    crawl_category_image(category_per_image=400)
    # update_shopping_data()

