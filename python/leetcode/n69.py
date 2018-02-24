#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
69. Sqrt(x)
求正整数x开方的整数值
先对结果变量赋值r=x，当r的平方大于x的时候，说明r值大于目标值,因此，x/r必定小于目标值
求r和x/r的平均数，结果大于等于目标值（根据y=1/x的函数图像观察出来的，具体推导就不清楚了）
重复取平均数，直到r的平方<=x
"""
class Solution(object):
    def mySqrt(self, x):
        """
        :type x: int
        :rtype: int
        """
        r = x
        while r*r > x:
            r = (r + x/r) / 2
        return r