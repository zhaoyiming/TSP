import random
import numpy as np
import math
import time
from load_data import load_data
import matplotlib.pyplot as plt

np.set_printoptions(precision=1)
mat10 = load_data("./TSP10cities.tsp")
mat100 = load_data("./TSP100cities.tsp")
dist = mat100

num_city = len(dist[0])  # 城市总数
initial_t = 1000
lowest_t = 0.001
M = 120  # 当连续多次都不接受新的状态，开始改变温度
iteration = 5000


# 计算距离
def new_dis(dis_mat, path):
    distance = 0
    for j in range(num_city - 1):
        distance = dis_mat[path[j]][path[j + 1]] + distance
    distance = dis_mat[path[num_city-1]][path[0]] + distance  # 回家
    return distance


def plot():
    plt.plot([i for i in range(len(mdistance))], mdistance)
    plt.ylabel("Fitness")
    plt.xlabel("Iteration")
    plt.savefig("data/hw21-SA/hw21-SA收敛曲线-100.png")
    plt.show()


if __name__ == '__main__':
    path = list(range(num_city))
    dis = new_dis(dist, path)
    t_current = initial_t
    start = time.process_time()
    mdistance = []
    while t_current > lowest_t:  # 外循环，改变温度
        count_m = 0
        count_iter = 0
        while count_m < M and count_iter < iteration:  # 内循环，连续多次不接受新的状态或者是迭代多次,跳出内循环
            # 防止随机了同一城市
            i = 0
            j = 0
            while i == j:
                i = random.randint(0, num_city-1)
                j = random.randint(0, num_city-1)
            #混淆数据
            path_new = path.copy()
            path_new[i], path_new[j] = path_new[j], path_new[i]  # 任意交换两个城市的位置,产生新解
            dis_new = new_dis(dist, path_new)
            dis_delta = dis_new - dis

            exp_d = math.exp(-dis_delta / t_current)
            if dis_delta < 0:
                path = path_new
                dis = dis_new
            elif exp_d > random.random():
                path = path_new
                dis = dis_new
            else:
                count_m = count_m + 1
            count_iter = count_iter + 1
        t_current = 0.99 * t_current  # 改变温度
        mdistance.append(dis)
    np.savetxt("data/hw21-SA/hw21-SA迭代数据-100.txt", mdistance)
    end = time.process_time()
    dis_min = dis
    path_min = path
    print('最短距离：', dis_min)
    print('最短路径：', path_min)
    print("耗时：", end - start)
    plot()
