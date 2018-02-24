#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
70. Climbing Stairs

本质为斐波那契数
"""
class Solution(object):
    def climbStairs(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n == 1:
            return 1
        if n == 2:
            return 2
        a, b = 1, 2
        result = 0
        for i in range(2, n):
            result = a + b
            a, b = b, a+b

        return result

