from collections import Counter
from typing import List
import heapq


class Solution:
    def topKFrequent1(self, nums: List[int], k: int) -> List[int]:
        # Approach ①: BUCKET SORT — O(n) time, O(n) space. Beats the O(n log n) bar.
        mapp = Counter(nums)  # {num: count} in one pass, O(n)

        # buckets[i] = list of numbers that appear exactly i times.
        # The INDEX itself is the frequency. A value appears at most n times,
        # so n+1 slots is enough. Each bucket is a LIST — multiple numbers can
        # share a count (e.g. [1,1,2,2] -> both land in buckets[2]).
        res = [[] for _ in range(len(nums) + 1)]
        for number, count in mapp.items():
            res[count].append(number)

        # No sort needed: walk indices high -> low and we visit numbers in
        # descending-frequency order for free (array indices are already ordered).
        result = []
        for i in range(len(nums), -1, -1):
            if len(res[i]) >= 1:
                for x in res[i]:
                    result.append(x)

            # Safe to check once per bucket because "the answer is unique" is
            # guaranteed => no tie at the k/k+1 frequency boundary, so a single
            # bucket never overshoots k.
            if len(result) == k:
                return result
        return []

    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # Approach ②: SIZE-k MIN-HEAP — O(n log k) time. Beats O(n log n) when k < n.
        mapp = Counter(nums)
        heap = []
        for number, count in mapp.items():
            # Push (count, number): heapq compares the FIRST tuple element, so
            # the heap orders by count; number is only a tiebreaker.
            heapq.heappush(heap, (count, number))

            # Cap the heap at k. The root is the weakest survivor (lowest count);
            # evict it the moment the heap overflows. So each op stays log k, and
            # what remains at the end is exactly the k most frequent.
            if len(heap) > k:
                heapq.heappop(heap)

        result = []
        for key, value in heap:  # key = count (unused), value = number
            result.append(value)

        return result


# ─────────────────────────────────────────────────────────────────────────────
# USEFUL COMMANDS / IDIOMS  (LC 347 — Top K Frequent, Arrays & Hashing)
# ─────────────────────────────────────────────────────────────────────────────
#
# Trigger:  "top-k / k most frequent / k largest / k closest"
#   -> heap of size k  (O(n log k)),  OR if the key is a small bounded integer,
#      bucket sort by that key  (O(n)).
#
# Bucket-sort precondition (the gate): the sort key must be a SMALL BOUNDED
#   INTEGER so it can be an array index. Here frequencies run 1..n -> fine.
#   Continuous / huge-range keys (e.g. Euclidean distance in K-Closest-Points,
#   up to ~1e9) CANNOT be indexed -> use a heap instead.
#
# Container choice: each bucket is a LIST, not a scalar — many numbers can share
#   a count. (collect-many => list; "whether it exists" => set.)
#
# Complexity arithmetic (the easy-to-botch part):
#   O(a) + O(b) = O(max(a, b))        # dominant term wins; NOT O(a)
#     -> Counter O(n) + sort O(n log n) = O(n log n)   (this is what's FORBIDDEN)
#   Nested loops: multiply ONLY if the inner runs full-length every pass.
#     The bucket-spill inner loop's TOTAL iterations = #unique numbers <= n,
#     so the extraction is O(n) overall, NOT O(n * k).
#
# Two heap variants — say WHICH:
#   heapify all unique + pop k  -> O(n log n)   (no better than sorting)
#   size-k heap (this file)     -> O(n log k)   (beats it when k < n)
#
# Handy Python idioms:
#   from collections import Counter
#   Counter(nums)                       # {num: count} in one pass
#   Counter(nums).most_common(k)        # THE one-liner: [(num, count), ...], O(n log k)
#   [n for n, _ in Counter(nums).most_common(k)]
#   import heapq
#   heapq.heappush(h, (count, num)); heapq.heappop(h)   # min-heap; key first
#   heapq.nlargest(k, count, key=count.get)             # general top-k, O(n log k)
#   [[] for _ in range(len(nums) + 1)]  # bucket array (fresh lists, not [[]]*n!)
#
# Sibling problems (same pattern in disguise):
#   LC 973 K Closest Points to Origin  -> heap (distance key is NOT bucket-able)
#   LC 215 Kth Largest Element         -> size-k heap, or quickselect
#   LC 75  Sort Colors                 -> counting sort (key range is 0..2)
#
# Quick local smoke test:
#   python3 -c "from top_k_frequent_elements import Solution; \
#     print(Solution().topKFrequent([1,1,1,2,2,3], 2))"   # -> [2, 1] (any order)
