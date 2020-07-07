import numpy as np
import time
from load_data import load_data
import pandas as pd
import math
np.set_printoptions(precision=1)
mat10 = load_data("./TSP10cities.tsp")
mat100 = load_data("./TSP100cities.tsp")
dist = mat10

N = dist.shape[0]
M = 1 << (N + 1)
path = np.ones([M, N])
dp = np.ones([M, N]) * -1


def memo(s, now, num):  # s为终点，init当前点，
    minvalue = 99999
    if dp[s][now] != -1:  # 若访问过则返回备忘录的值
        return dp[s][now]
    if s == (1 << N):
        return dist[0][now]
    for i in range(N):  # 递归寻找最优路径,更新各层备忘录
        if s & (1 << i):
            m = memo(s & (~(1 << i)), i, num + 1) + dist[i][now]
            if m < minvalue:
                minvalue = m
                path[s][now] = i
    dp[s][now] = minvalue

    return dp[s][now]


if __name__ == '__main__':
    s = (1 << N + 1) - 2  # 以二进制形式表示是否访问过
    start = time.process_time()
    distance = memo(s, 0, 0)  # 形成整个备忘录
    end = time.process_time()
    now = 0
    num = 0

    print(distance)
    print("路径：[ 1.0, ", end="")
    m_data = [1]
    for i in range(9):
        m_data.append(path[s][now]+1)
        if i == 8:
            print(path[s][now]+1, end='', )
        else:
            print(path[s][now]+1, end=', ', )
        now = int(path[s][now])
        s = s & (~(1 << now))

    np.savetxt("data/hw12/hw12路径数据.txt", m_data, fmt='%01d')
    print("]")
    print("程序的运行时间是：%s" % (end - start))

