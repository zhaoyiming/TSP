import numpy as np
import math
import time
from load_data import load_data


def greedy(distance):
    num = len(distance[:, 0])
    # n表示初始城市,num为城市数,path为旅行路径

    arrived = np.zeros(num)
    path = np.zeros(num + 1)
    start = time.clock()
    for i in range(num):  # arrived表示是否到达过此城市,初始化所有城市的到达标志为否
        arrived[i] = 0
    cost = 0  # cost表示总距离
    first = 0
    path[0] = first
    p = first  # p表示目前到达的城市
    arrived[first] = True
    for i in range(1, num):
        min_distance = 10000000  # 初始化最小距离
        for j in range(num):
            if (not arrived[j]) & (distance[p][j] < min_distance):  # 遍历与该节点相邻城市,若还没有到达过并且与该城市距离最近,遍去往.
                k = j
                min_distance = distance[p][j]
        #   更新选择城市后的参数
        cost = cost + distance[p][k]
        path[i] = k
        arrived[k] = True
        p = k
    # 最后回到初始城市
    path[num] = first
    cost = cost + distance[p][0]

    np.savetxt("data/hw11/hw11路径数据.txt", path+1, fmt='%01d')
    end = time.clock()
    atime = end - start
    return path, cost, atime


if __name__ == '__main__':
    mat10 = load_data("./TSP10cities.tsp")
    path, cost, atime = greedy(mat10)
    # mat100 = load_data("./TSP100cities.tsp")
    # path, cost, atime = greedy(mat100)

    print("运动路径:", path + 1)
    print("最小距离:", cost)
    print("程序的运行时间是：", atime)
