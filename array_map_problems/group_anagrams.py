from collections import defaultdict
from typing import List, Tuple


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        r = dict()

        for word in strs:
            pattern = self.calc_pattern2(word)

            if pattern in r:
                r[pattern].append(word)
            else:
                r[pattern] = [word]

        return list(r.values())

    def calc_pattern(self, word: str) -> str:
        # Canonical key #1: sort the letters. Two anagrams sort to the same string.
        # O(k log k) per word.
        return "".join(sorted(word))

    def calc_pattern2(self, word: str) -> Tuple[int, ...]:
        # Canonical key #2: 26-length letter-count tuple. Immutable => hashable.
        # O(k) per word — asymptotically leaner than sorting.
        counts = [0] * 26
        for char in word:
            counts[ord(char) - ord("a")] += 1  # ord('a')=97 -> index 0..25
        return tuple(counts)

    def groupAnagrams_idiomatic(self, strs: List[str]) -> List[List[str]]:
        # Same algorithm, defaultdict(list) drops the `if key in d` branch.
        groups = defaultdict(list)
        for word in strs:
            groups["".join(sorted(word))].append(word)  # append the WORD, not the key
        return list(groups.values())


# ─────────────────────────────────────────────────────────────────────────────
# USEFUL COMMANDS / IDIOMS  (LC 49 — group-by-canonical-key, Arrays & Hashing)
# ─────────────────────────────────────────────────────────────────────────────
#
# Trigger:  problem says "GROUP items that share property X"
#   -> compute a canonical key (identical for equivalent items AND hashable),
#      bucket into a dict  key -> list of members.
#
# Set vs dict:  "do I only care WHETHER it exists (set), or must I COLLECT/attach
#               data to it (dict)?"  group/bucket/count-per/index-by => dict.
# Key & counts: "does my key need to remember HOW MANY?"  if yes, a set of chars
#               is disqualified ({a,b} for both 'aab' and 'abb') -> use counts.
#
# Complexity:  n words, k = max length.
#   sorted-string key : O(n * k log k)      count-tuple key : O(n * k)
#
# Handy Python idioms:
#   "".join(sorted(s))            # canonical anagram key (sorted string)
#   ord(c) - ord('a')             # lowercase char -> index 0..25 (no magic 96)
#   tuple(counts)                 # list -> hashable dict key
#   from collections import defaultdict
#   groups = defaultdict(list); groups[key].append(item)   # no membership check
#   d.setdefault(key, []).append(item)                     # plain-dict equivalent
#   collections.Counter(s)                                 # {char: count} in one call
#   list(d.values())              # the grouped buckets
#
# Sibling problems (same pattern in disguise):
#   LC 242 Valid Anagram          -> two-item special case: do the keys match?
#   LC 249 Group Shifted Strings  -> key = tuple of gaps between consecutive letters
#   LC 347 Top K Frequent         -> Counter + bucket sort / size-k heap
#
# Quick local smoke test:
#   python3 -c "from group_anagrams import Solution; \
#     print(Solution().groupAnagrams(['eat','tea','tan','ate','nat','bat']))"
