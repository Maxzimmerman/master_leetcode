# LC 217 — Contains Duplicate
# Given an integer array, return True if any value appears at least twice.
#
# Trigger: "are all elements distinct? / any value twice?" -> the UNIQUENESS family.
#   -> hash-set membership, OR sort + adjacent scan.
# Constraints: n up to 1e5 -> brute force O(n^2) = 1e10 > ~1e8/sec -> times out.
#   Target must be O(n log n) or O(n).


class Solution:
    # --- Tier 1: one-pass set (best general answer) --------------------------
    # Redundancy in the brute force is re-scanning to ask "have I seen this?".
    # A set answers that in O(1). Invariant: `s` holds exactly nums[0..i-1].
    # Check-then-insert (never insert first, or every element looks like its own dup).
    # Time O(n), space O(n). Early-exits at the first repeat.
    def containsDuplicate1(self, nums: List[int]) -> bool:
        s = set()
        for i in nums:
            if i in s:
                return True
            s.add(i)
        return False

    # --- Tier 2: sort + adjacent scan ---------------------------------------
    # Sorting drags every copy of a value into one contiguous run, so any
    # duplicate MUST become an adjacent equal pair -> checking neighbours suffices.
    # Time O(n log n), but only O(1) EXTRA space (mutates input).
    # Prefer this over the set when RAM is the scarce resource (set trades the
    # other way: more RAM, less CPU).
    def containsDuplicate2(self, nums: List[int]) -> bool:
        nums.sort()
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                return True
        return False

    # --- Tier 3: set-size comparison (the bulk one-liner) --------------------
    # Self-Q: "can I answer this with a whole-collection op instead of a loop?"
    # Uniqueness <=> dedup changes the size. Shortest, still O(n)/O(n), but NO
    # early exit and it hides the mechanism (an interviewer may push back).
    def containsDuplicate3(self, nums: List[int]) -> bool:
        return len(set(nums)) != len(nums)

    # --- Baseline: brute force (ruled out by the constraints) ----------------
    # Compares every pair. O(n^2) time, O(1) space. Kept only as the baseline
    # the optimal is measured against — TLEs at n ~ 1e5 exactly as predicted.
    def containsDuplicate(self, nums: List[int]) -> bool:
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                if nums[i] == nums[j]:
                    return True
        return False
