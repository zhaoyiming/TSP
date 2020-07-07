from hw11 import greedy
import math
import time
from queue import Queue
from load_data import load_data
import numpy as np
mat10 = load_data("./TSP10cities.tsp")
mat100 = load_data("./TSP100cities.tsp")
dist = mat10
CityNum = dist.shape[0]
Dist = dist


class Node:
    def __init__(self, citynum):
        self.visited = [False] * citynum  # 是否去过
        self.s = 0
        self.e = 0
        self.current = 0
        self.num = 0  # 走过数量
        self.pathsum = 0
        self.lb = 0  # 下界
        self.listc = []  # path


def get_up():  # 用贪心法获得上界
    path, cost, atime = greedy(Dist)
    return cost


def get_lb(node):  # 获得下界
    min_path = node.pathsum * 2
    # 距离起点和终点最近城市距离
    min1 = 99999
    min2 = 99999
    for i in range(CityNum):
        if node.visited[i] == False and min1 > Dist[i][node.s]:
            min1 = Dist[i][node.s]
    if min1 != 99999:
        min_path = min_path + min1
    for i in range(CityNum):
        if node.visited[i] == False and min2 > Dist[node.e][i]:
            min2 = Dist[node.e][i]
    if min2 != 99999:
        min_path = min_path + min2

    # 未遍历城市到达和离开的最小距离
    for i in range(CityNum):
        if not node.visited[i]:
            min1 = min2 = 99999
            for j in range(CityNum):
                if min1 > Dist[i][j]:
                    min1 = Dist[i][j]
                    temp = j
            for k in range(CityNum):
                if min2 > Dist[k][i] and k != temp:
                    min2 = Dist[i][k]
            if min1 != 99999:
                min_path = min_path + min1
            if min2 != 99999:
                min_path = min_path + min2
    return min_path / 2


def create_node(cur_node, next_city):  # 拓展新节点
    next_node = Node(CityNum)
    next_node.s = cur_node.s  # 沿着cur_node走到next，起点不变
    next_node.pathsum = cur_node.pathsum + Dist[cur_node.e][next_city]  # 更新当前走过的路程值
    next_node.e = next_city
    next_node.num = cur_node.num + 1
    next_node.listc = cur_node.listc.copy()
    next_node.listc.append(next_city)  # 更新路径
    next_node.visited = cur_node.visited.copy()
    next_node.visited[next_city] = True
    next_node.lb = get_lb(next_node)
    return next_node


def bab(num, Dist):
    global minpath
    max_v = get_up()
    node = Node(num)  # 出发城市的节点信息
    node.e = 0  # 到0结束
    node.num += 1
    node.listc.append(0)
    node.visited[0] = True
    node.lb = max_v  # 初始目标值等于上界

    min_path = 99999
    pri_queue = Queue()
    pri_queue.put(node)
    while pri_queue.qsize() != 0:
        cur_node = pri_queue.get()
        if cur_node.num == num:  # 遍历完
            ans = cur_node.pathsum + Dist[cur_node.s][cur_node.e]  # 总路径
            max_v = min(ans, max_v)  # 更新
            if min_path > ans:
                min_path = ans
                minpath = cur_node.listc.copy()
        for i in range(num):  # 向下扩展的点入队
            if not cur_node.visited[i]:
                next_node = create_node(cur_node, i)
                if next_node.lb >= max_v:
                    continue
                pri_queue.put(next_node)
    minpath.append(1)
    return min_path, minpath


if __name__ == "__main__":
    s = time.process_time()  # 程序计时开始
    value, Path = bab(CityNum, Dist)  # 调用分支限定法
    np.savetxt("data/hw13/hw13路径数据.txt", Path, fmt='%01d')
    e = time.process_time()  # 程序计时结束
    print("最短路径为：")
    for m in range(CityNum):
        print(str(Path[m] + 1) + "—>", end="")
    print(Path[CityNum])
    print("总路径长为：" + str(value))
    print("程序的运行时间是：%s" % (e - s))
