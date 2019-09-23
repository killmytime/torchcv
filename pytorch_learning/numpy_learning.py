# -*- coding: utf-8 -*-
import numpy as np

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 64, 1000, 100, 10  # 隐藏层即没有展示出实现的层

# Create random input and output data
x = np.random.randn(N, D_in)  # 标准正态分布选取的随机数
y = np.random.randn(N, D_out)

# Randomly initialize weights权重
w1 = np.random.randn(D_in, H)
w2 = np.random.randn(H, D_out)

learning_rate = 1e-6#学习率
for t in range(500):
    # Forward pass: compute predicted y
    h = x.dot(w1)  # 内积，矩阵积   这里注重理解没有考虑偏置bias了
    h_relu = np.maximum(h, 0)  # relu即激活函数，这里就是意思意思取正值吧
    y_pred = h_relu.dot(w2)#前馈

    # Compute and print loss
    loss = np.square(y_pred - y).sum()#损失
    print(t, loss)

    # Backprop to compute gradients of w1 and w2 with respect to loss
    grad_y_pred = 2.0 * (y_pred - y)
    grad_w2 = h_relu.T.dot(grad_y_pred)
    grad_h_relu = grad_y_pred.dot(w2.T)
    grad_h = grad_h_relu.copy()
    grad_h[h < 0] = 0
    grad_w1 = x.T.dot(grad_h)

    # Update weights通过更新权重达到修正的效果
    w1 -= learning_rate * grad_w1
    w2 -= learning_rate * grad_w2
