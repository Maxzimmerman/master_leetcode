# LC 1 — Two Sum
# Given an array and a target, return the indices of the two numbers that sum
# to target. Exactly one solution; can't reuse the same element.
#
# Trigger: "find a pair summing to a target" -> for each x you know EXACTLY what
#   you need: the complement (target - x). Knowing what you're looking for ->
#   look it up (hash map), don't loop.


class Solution:
    # --- Hash map, one pass (O(n) time, O(n) space) --------------------------
    # Invariant: `remembered_nums` holds every value seen so far (nums[0..i-1])
    # mapped to its index. Because it only holds EARLIER elements, any match is a
    # distinct, earlier index -> handles self-pairing for free.
    # Check the complement FIRST, then insert (insert-first could match yourself).
    def twoSum1(self, nums: List[int], target: int) -> List[int]:
        remembered_nums = dict()

        for index, value in enumerate(nums):
            find = target - value
            if find in remembered_nums:
                return [remembered_nums[find], index]

            # Note: keying by value collapses duplicates (last write wins), but
            # that's safe here — the complement is always found on an earlier pass.
            remembered_nums[value] = index
        return None

    # --- Sort + two pointers (O(n log n) time, O(1) extra space) -------------
    # Trade-off vs the hash map: slower, but no extra hash structure.
    # Two pointers only works BECAUSE we sort — on unsorted input the converge
    # trick is meaningless.
    # The answer needs ORIGINAL indices, but sorting destroys order -> sort a
    # list of (value, index) tuples so each element carries its own index through.
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        original_indices = [(val, idx) for idx, val in enumerate(nums)]
        original_indices.sort()

        # Converge from both ends. Invariant: moving l up can only raise the sum,
        # moving r down can only lower it — so each move safely discards pairs.
        # (Loop with `while l < r`; the for-range here happens to work only
        #  because a solution is guaranteed before the pointers cross.)
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
