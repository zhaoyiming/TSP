import numpy as np
import math


def load_data(file):
    f = open(file)
    lines = f.readlines()
    rows = len(lines)  # 文件行数
    data_mat = np.zeros((rows, 3)).astype(int)  # 初始化矩阵
    row = 0
    for line in lines:
        line = line.strip('\n').split(' ')
        data_mat[row, :] = line[:]
        row += 1
    num = len(data_mat[:, 0])
    distance = np.zeros((num, num)).astype(float)
    # 计算距离
    for i in range(num):
        for j in range(num):
            distance[i, j] = math.sqrt(np.sum((data_mat[i, :] - data_mat[j, :]) ** 2))
    return distance



