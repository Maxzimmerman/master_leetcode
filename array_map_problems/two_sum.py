class Solution:
    def twoSum1(self, nums: List[int], target: int) -> List[int]:
        remembered_nums = dict()

        for index, value in enumerate(nums):
            find = target - value
            if find in remembered_nums:
                return [remembered_nums[find], index]

            remembered_nums[value] = index
        return None

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        original_indices =[(val, idx) for idx, val in enumerate(nums)]
        original_indices.sort()

        l = 0
        r = len(nums) - 1
        for i in range(len(nums)):
            maybe_res = original_indices[l][0] + original_indices[r][0]
            
            if maybe_res > target:
                r = r - 1
            elif maybe_res < target:
                l = l + 1
            elif maybe_res == target:
                return [original_indices[l][1], original_indices[r][1]]
