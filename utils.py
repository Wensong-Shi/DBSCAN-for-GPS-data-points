import csv
import math


def dataloader(filename):
    """
    读取提取过的数据
    :param filename: 存储提取过的数据的文件名
    :return: 存储经纬度的列表：[[lon1, lat1], [lon2, lat2], ...]
    """
    dataset = []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            dataset.append(row)
    return dataset


def is_in_cluster(point, cluster):
    """
    判断某点是否在已有的簇中
    :param point: 要判断的点
    :param cluster: 已有的簇
    :return: bool值
    """
    if len(cluster) == 0:
        return False
    else:
        for i in range(0, len(cluster)):
            if point in cluster[i]:
                return True
        return False


def calculate_distance(point1, point2):
    """
    用半正矢公式计算给定两点经纬度的距离
    :param point1:点1
    :param point2:点2
    :return:距离，单位：km
    """
    r = 6371.393  # 地球平均半径，单位：km
    # 弧度制
    lon1 = float(point1[0]) * math.pi / 180.0
    lat1 = float(point1[1]) * math.pi / 180.0
    lon2 = float(point2[0]) * math.pi / 180.0
    lat2 = float(point2[1]) * math.pi / 180.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    h = (math.sin(dlat / 2) ** 2) + (math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
    theta = math.asin(math.sqrt(h))
    d = 2 * r * theta

    return d


def decentered_neighborhood(point, dataset, eqs):
    """
    返回某点的去心邻域包含的全部点
    :param point: 中心点
    :param dataset: 数据集
    :param eqs: 半径
    :return: 该点的去心邻域包含的全部点
    """
    decentered_neighborhood = []
    for origin_point in dataset:
        d = calculate_distance(point, origin_point)
        if d <= eqs:
            decentered_neighborhood.append(origin_point)
    decentered_neighborhood.remove(point)

    return decentered_neighborhood


def write_file(filename, data_list):
    """
    将数据列表逐个元素按行写入文件
    :param filename: 待写入的文件名
    :param data_list: 数据列表
    :return: 无
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for data in data_list:
            writer.writerow(data)
