from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision import transforms
import torch
import torch.nn as nn
import torch.optim as optim

import os
import copy
import time
import urllib.request
import pandas as pd
from PIL import Image, ImageFile

''' required parameter '''
ImageFile.LOAD_TRUNCATED_IMAGES = True  # allow truncated image
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
GENERATE_DATA_PHASE = False  # fashion 데이터 셋을 생성할때를 제외하고는 False 로 설정해야 한다

# 데이터 전처리
# Handnet은 (3 x H x W) 크기의 입력 데이터를 요구하므로 사이즈가 다를경우 전처리 과정을 거쳐야 한다.
# 각 이미지의 H와 W는 224이어야 하며 3-channel (RGB) 을 가지고 있다.

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 데이터 불러오기
if not GENERATE_DATA_PHASE:
    data_dir = os.path.join(os.path.dirname(__file__), 'assets/fashion')
    dataset = ImageFolder(root=data_dir, transform=preprocess)
    data_loader = torch.utils.data.DataLoader(dataset, batch_size=4, shuffle=True, num_workers=4)


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
    class_labels = dataset.class_to_idx
    for label, index in class_labels.items():
        if index == preds:
            pred_class = label
            break

    return pred_class


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

