import numpy as np
import base64
import pickle
import torch
from operator import itemgetter


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
