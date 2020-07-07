import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
np.set_printoptions(precision=1)

def get_neighborhood(center, radix, domain):   # 获得
    if radix < 1:
        radix = 1
    deltas = np.absolute(center - np.arange(domain))
    distances = np.minimum(deltas, domain - deltas)
    return np.exp(-(distances * distances) / (2 * (radix * radix)))


def get_route(cities, network):  # 获得现网络的路径
    cities['winner'] = cities[['x', 'y']].apply(
        lambda c: e_distance(network, c).argmin(),
        axis=1, raw=True)
    return cities.sort_values('winner').index


def e_distance(a, b):
    return np.linalg.norm(a - b, axis=1)


def route_distance(cities):  # 计算总距离
    points = cities[['x', 'y']]
    distances = e_distance(points, np.roll(points, 1, axis=0))
    return np.sum(distances)


def normalize(points):  # 归一化
    ratio = (points.x.max() - points.x.min()) / (points.y.max() - points.y.min()), 1
    ratio = np.array(ratio) / max(ratio)
    norm = points.apply(lambda c: (c - c.min()) / (c.max() - c.min()))
    return norm.apply(lambda p: ratio * p, axis=1)


def plotit(mdistance):
    plt.plot([i for i in range(len(mdistance))], mdistance)
    plt.ylabel("Fitness")
    plt.xlabel("Iteration")
    plt.savefig("data/hw22-SOM/hw22-SOM收敛曲线-100.png")
    plt.show()



def som(data_mat, iterations, learning_rate=0.8):
    cities = data_mat.copy()
    cities[['x', 'y']] = normalize(cities[['x', 'y']])  # 归一化以加快运算速度
    n = cities.shape[0] * 8  # 生成八倍的神经元
    network = np.random.rand(n, 2)  # 随机生成神经元位置
    plot_fix = []
    for i in range(iterations):
        city = cities.sample(1)[['x', 'y']].values
        winner_idx = e_distance(network, city).argmin()
        gaussian = get_neighborhood(winner_idx, n // 10, network.shape[0])
        network += gaussian[:, np.newaxis] * learning_rate * (city - network)
        # 衰减参数来进行收敛
        learning_rate = learning_rate * 0.99997
        n = n * 0.9997
        if n < 1:
            print("神经元优胜领域达到最低")
            break
        if learning_rate < 0.001:
            print("学习率达到最低")
            break
        # 记录每次总路径
        route = get_route(cities, network)
        data_mat = data_mat.reindex(route)
        distance = route_distance(data_mat)
        plot_fix.append(distance)
    np.savetxt("data/hw22-SOM/hw22-SOM迭代数据-100.txt",plot_fix)
    plotit(plot_fix)
    return route


if __name__ == '__main__':
    start = time.process_time()
    data_mat = pd.read_csv("TSP100cities.tsp", sep=' ',
            names=['city', 'y', 'x'],
            dtype={'city': str, 'x': np.float64, 'y': np.float64})
    route = som(data_mat, 80000)  # 通过SOM得到最佳路径
    print(route)
    data_mat = data_mat.reindex(route)  # 调整路径到原先的数据中
    distance = route_distance(data_mat)  # 计算总长
    end = time.process_time()

    print("耗时：", end-start)
    print('总长度 {}'.format(distance))
