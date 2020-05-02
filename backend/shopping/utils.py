import numpy as np
import base64
import pickle
import torch
from operator import itemgetter
from torchvision import transforms
from PIL import Image, ImageFile


def l2_distance(a, b):
    """
    measure l2-distance between image a and b

    :param a: image 1
    :param b: image 2
    :return: distance between a and b
    """
    val = torch.sqrt(torch.sum(a - b, dim=1) ** 2)
    return val.item()


def bytes_to_tensor(bytes_data):
    """
    convert byte data to tensor

    :param bytes_data: target bytes data
    :return: converted tensor
    """
    # convert bytes to numpy
    np_bytes = base64.b64decode(bytes_data)
    np_array = pickle.loads(np_bytes)

    # convert numpy to tensor
    converted = torch.from_numpy(np_array)
    return converted


def recommend_products(query, targets, how_many):
    """
    recommend products with l2-distance

    :param query: query image
    :param targets: images to check (with 'pk' and 'feature map')
    :param how_many: result count
    :return: recommended images
    """
    distance_list = [{'distance': l2_distance(query, bytes_to_tensor(target['feature_map'])), 'target': target}
                     for target in targets]
    distance_list.sort(key=itemgetter('distance'))
    recommend_list = [p['target'] for p in distance_list[:how_many]]
    return recommend_list


# Handnet은 (3 x H x W) 크기의 입력 데이터를 요구하므로 사이즈가 다를경우 전처리 과정을 거쳐야 한다.
# 각 이미지의 H와 W는 224이어야 하며 3-channel (RGB) 을 가지고 있다.
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def predict(model, input_image):
    """
    Predict class of query image

    :param model: pre-trained classification model
    :param input_image: query image
    :return: class of image
    """
    model.eval()  # evaluation mode

    # create a mini-batch
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)

    output = model(input_batch)
    _, preds = torch.max(output, 1)

    pred_class = ''
    class_labels = {
        0: '귀걸이', 1: '남성화', 2: '넥타이', 3: '드레스', 4: '모자', 5: '목걸이', 6: '바지',
        7: '반바지', 8: '반지', 9: '백팩', 10: '벨트', 11: '브래지어', 12: '샌들', 13: '선글라스',
        14: '셔츠', 15: '스웨터', 16: '스웻셔츠', 17: '시계', 18: '양말', 19: '여성화', 20: '운동화',
        21: '재킷', 22: '지갑', 23: '치마', 24: '티셔츠', 25: '팔찌', 26: '팬티', 27: '핸드백'
    }
    for index, label in class_labels.items():
        if index == preds:
            pred_class = label
            break
    return pred_class



'''
# 데이터 불러오기 - 초기 학습 데이터 구성할때만 필요
ImageFile.LOAD_TRUNCATED_IMAGES = True  # allow truncated image

GENERATE_DATA_PHASE = False  # fashion 데이터 셋을 생성할때를 제외하고는 False 로 설정해야 한다
import os
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

if GENERATE_DATA_PHASE:
    data_dir = os.path.join(os.path.dirname(__file__), 'assets/fashion')
    dataset = ImageFolder(root=data_dir, transform=preprocess)
    data_loader = torch.utils.data.DataLoader(dataset, batch_size=4, shuffle=True, num_workers=4)
'''
'''
# 모델 학습용 함수
import torch.nn as nn
import torch.optim as optim
import time
import copy

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

def train(model, save_at='assets/deep.pt'):
    """
    Train the model

    :param model: model to train
    :param save_at: model save path
    :return: None
    """
    # optim, loss function
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    # training
    since = time.time()
    best_acc = 0.0
    best_model_wts = copy.deepcopy(model.state_dict())
    for epoch in range(2):

        running_loss = 0.0
        running_corrects = 0
        for batch_idx, (inputs, labels) in enumerate(data_loader):
            inputs = inputs.to(device)
            labels = labels.to(device)

            # zero the parameter gradient
            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            _, preds = torch.max(outputs, 1)

            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)

            print(f'\t--> epoch{epoch + 1} {100 * batch_idx / len(data_loader):.2f}% done...')

        epoch_loss = running_loss / len(data_loader.dataset)
        epoch_acc = running_corrects.double() / len(data_loader.dataset)

        print(f'{epoch + 1} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

        if epoch_acc > best_acc:
            best_acc = epoch_acc
            best_model_wts = copy.deepcopy(model.state_dict())

    time_elapsed = time.time() - since
    print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
    print(f'Best val Acc: {best_acc:4f}')

    torch.save(best_model_wts, save_at)
'''

'''
# kaggle의 fashion 데이터 셋 디렉토리 구조 생성을 위한 함수

import urllib.request

def generate_fashion_dataset(root_dir=None):
    """
    fashion dataset 이 다음과 같은 구조를 가지도록 폴더 구조를 생성한다.
    images.csv와 styles.csv 파일을 통해 이미지를 다운받아 생성

    * ex)
      root/shirts/xxx.png
      root/shirts/xxy.png
      root/shirts/xxz.png

      root/shoes/123.png
      root/shoes/nsdf3.png

      root/hat/asd932_.png
    """
    image_frame = pd.read_csv('assets/images.csv')
    style_frame = pd.read_csv('assets/styles.csv', usecols=['id', 'articleType'])  # 특정 열의 데이터만 읽어온다

    total = image_frame.shape[0]
    for idx in range(total):
        image_name = image_frame.iloc[idx, 0]
        img_url = image_frame.iloc[idx, 1]
        category = style_frame.iloc[idx, 1]

        # if category folder not exist, create new folder
        category_folder_path = root_dir + '/' + category + '/'
        if not os.path.exists(category_folder_path):
            os.mkdir(category_folder_path)
        try:
            save_path = category_folder_path + '/' + image_name
            if not os.path.exists(save_path):
                urllib.request.urlretrieve(img_url, save_path)
        except Exception as e:
            print(e)
            continue

        print(f'{idx * 100 / total:.2f} done...')
'''