# 用DBSCAN算法对GPS数据点进行聚类，获得包含若干簇的列表
# 列表中的每个元素包含了该簇中全部的点

import utils


# 超参数，可自行调整
eqs = 0.2  # 半径，单位：km
minpts = 100  # 半径内最小点数

# 读取文件，要求文件为.csv格式，每行两个字段，分别为一点的经纬度
filename = 'extracted_data/longitudes_latitudes'
dataset = utils.dataloader(filename)  # 存储经纬度的列表
# 初始化
cluster = []  # 存储若干个簇
c = 0  # 存储簇的个数
k = 0

# 对数据集中每个点进行处理
for origin_point in dataset:
    k = k + 1
    print(f'Processing: {k}')
    # 判断是否已经在某个簇中，若是，则可以跳过，若否，则判断是否为核心点
    if utils.is_in_cluster(origin_point, cluster):
        continue
    else:
        # 获取该点的去心邻域包含的全部点
        decentered_neighborhood_judgment = utils.decentered_neighborhood(origin_point, dataset, eqs)
        # 判断是否为核心点
        if (len(decentered_neighborhood_judgment) + 1) < minpts:
            continue
        else:
            pending_point = []  # 待处理的核心点
            c = c + 1

            pending_point.append(origin_point)
            # 建立一个新簇
            cluster.append([])
            cluster[c - 1].append(origin_point)

            while pending_point:

                # test
                num = len(pending_point)
                print(f'The number of pending_point is {num}')

                # 取出一个待处理的核心点，并找到其去心邻域包含的全部点
                point_processing = pending_point.pop()
                decentered_neighborhood_processing = utils.decentered_neighborhood(point_processing, dataset, eqs)

                # 去掉这个邻域里已在某个簇中的点
                point_added = []
                for point in decentered_neighborhood_processing:
                    if utils.is_in_cluster(point, cluster):
                        continue
                    else:
                        point_added.append(point)

                # 对待添加的点进行处理
                # 1. 加入当前簇中
                # 2. 判断是否为核心点，若是，则加入待处理的点集
                for point in point_added:
                    cluster[c - 1].append(point)
                    decentered_neighborhood_judgment = utils.decentered_neighborhood(point, dataset, eqs)
                    if (len(decentered_neighborhood_judgment) + 1) >= minpts:
                        pending_point.append(point)

                # test
                num = len(cluster[c - 1])
                print(f'The number of this cluster is {num}')

# 后处理
# 存储文件
i = 0
for one_cluster in cluster:
    i = i + 1
    filename = f'cluster/cluster{i}'
    utils.write_file(filename, one_cluster)
