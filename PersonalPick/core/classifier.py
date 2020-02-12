from .ConvNet import ConvNet
from .utils import predict

import os
import torch

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'assets/deep.pt')


# -- 상품 카테고리 분류기
class Classifier():
    def __init__(self, num_classes):
        # load model
        self.model = ConvNet(num_classes=num_classes)
        self.model.load_state_dict(torch.load(MODEL_PATH))
        self.model.eval()

    # 카테고리 분류
    def classify(self, input_image):
        result = predict(self.model, input_image)
        return result
