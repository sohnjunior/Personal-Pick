from .ConvNet import ConvNet
from .utils import predict, preprocess

import os
import torch
from .apps import ShoppingConfig


# -- 상품 카테고리 분류기
class Classifier():
    """
    Image class(label) classifier
    """
    def __init__(self, num_classes):
        """
        Initializer
        :param num_classes: number of class to classify
        """
        # load model
        self.model = ConvNet(num_classes=num_classes)
        self.model.load_state_dict(torch.load(ShoppingConfig.model_params))
        self.model.eval()

    def classify(self, input_image):
        """
        Classify the query image

        :param input_image: query image
        :return: class of query image
        """
        result = predict(self.model, input_image)
        return result

    def embedding(self, input_image):
        """
        Image embedding with pre-trained model

        :param input_image: base64 image from request
        :return: embedded feature map
        """
        # create a mini-batch
        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0)

        # embedded feature map
        output = self.model(input_batch)

        return output
