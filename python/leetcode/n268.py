#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
268. Missing Number
"""


class Solution(object):
    """
    位操作，骚操作，没想明白这个理论依据是什么。。
    missing =4∧(0∧0)∧(1∧1)∧(2∧3)∧(3∧4)
            =(4∧4)∧(0∧0)∧(1∧1)∧(3∧3)∧2
            =0∧0∧0∧0∧2
            =2
    """
    def missingNumber_1(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        missing = len(nums)
        for i in range(len(nums)):
            missing ^= i ^ nums[i]
        return missing

    """
    用等差数列求和公式
    """
    def missingNumber_2(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        length = len(nums)
        expect = length * (length + 1) / 2
        actual = 0
        for i in range(length):
            actual += nums[i]
        return expect - actual
