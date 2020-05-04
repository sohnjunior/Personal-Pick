import torch
import torch.nn as nn

import torchvision.models as models
from torchvision.models.alexnet import model_urls


# 상품 이미지 분류를 위한 모델 정의 - AlexNet을 finetuning 해서 사용
# https://github.com/pytorch/vision/blob/master/torchvision/models/alexnet.py

# https://discuss.pytorch.org/t/torchvision-url-error-when-loading-pretrained-model/2544/2
# model_urls['alexnet'] = model_urls['alexnet'].replace('https://', 'http://')
#
original_model = models.alexnet(pretrained=True)


class ConvNet(nn.Module):
    def __init__(self, num_classes=20):
        super(ConvNet, self).__init__()
        self.features = original_model.features  # original model's features

        # custumize FC layer
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 6 * 6, 4096),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )

        # freeze the pre-trained weights
        for p in self.features.parameters():
            p.requires_grad = False

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x


# # -- 주어진 학습 데이터를 기반으로 ConvNet training
# from .utils import preprocess, generate_fashion_dataset, train, predict
# from PIL import Image
#
# if __name__ == '__main__':
#     # generate_fashion_dataset(root_dir='assets/fashion')  # need to be executed only once!
#
#     num_classes = 28  # fashion dataset 의 세부 분류를 예측한다.
#
#     MODEL_PATH = 'assets/deep.pt'
#     model = ConvNet(num_classes=num_classes)
#     train(model, save_at=MODEL_PATH)
#
#     IMAGE_PATH = 'assets/fashion/귀걸이/31702.jpg'
#     input_image = Image.open(IMAGE_PATH)
#     model.load_state_dict(torch.load(MODEL_PATH))
#     print(predict(model, input_image))

