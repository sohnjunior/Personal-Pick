import numpy as np


def l2_distance(a, b):
    """
    measure l2-distance between image a and b

    :param a: image 1
    :param b: image 2
    :return: distance between a and b
    """
    return np.sqrt(np.sum(a - b, axis=1) ** 2)


def recommend_products(query, targets, how_many):
    """
    recommend products with l2-distance

    :param query: query image
    :param targets: images to check (with 'pk' and 'feature map')
    :param how_many: result count
    :return: recommended images
    """
    distance_list = [{'distance': l2_distance(query - target['feature_map']), 'target': target} for target in targets]
    sorted(distance_list, key=lambda x: x['distance'])
    recommend_list = [p['target'] for p in distance_list[:how_many]]
    return recommend_list
