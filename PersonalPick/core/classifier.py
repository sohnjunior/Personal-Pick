from .ConvNet import ConvNet
from .utils import predict

import torch


# -- 상품 카테고리 분류기
class Classifier():
    def __init__(self):
        # load model
        self.model = ConvNet()
        self.model.load_state_dict(torch.load('assets/deep.pt'))
        self.model.eval()

    # 카테고리 분류
    def classify(self, input_image):
        # input image를 PIL image로 변환한다.
        result = predict(self.model, input_image)
        print(result)
