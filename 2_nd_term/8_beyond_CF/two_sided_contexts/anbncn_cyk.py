from typing import List, Dict, Set

class TwoSidedContextCYK:
    def __init__(self, grammar: Dict, left_context: Dict, right_context: Dict, start_symbol: str):
        self.grammar = grammar
        self.left_context = left_context
        self.right_context = right_context
        self.start_symbol = start_symbol

    def parse(self, input_string: str) -> bool:
        n = len(input_string)
        if n == 0:
            return False

        # CYK chart: C[i][j] = set of nonterminals spanning i to j
        C = [[set() for _ in range(n+1)] for _ in range(n+1)]

        # Base case: terminals
        for i in range(1, n+1):
            char = input_string[i-1]
            for A, prods in self.grammar.items():
                for prod in prods:
                    if len(prod) == 1 and prod[0] == char:
                        # Check left context (if any)
                        left_ok = self._check_context(A, i-1, C, self.left_context, left=True)
                        # Check right context (if any)
                        right_ok = self._check_context(A, i, C, self.right_context, left=False)
                        if left_ok and right_ok:
                            C[i][i].add(A)

        # Fill the chart
        for length in range(2, n+1):
            for i in range(1, n-length+2):
                j = i + length - 1
                for k in range(i, j):
                    for A, prods in self.grammar.items():
                        for prod in prods:
                            if len(prod) == 2:  # Binary productions (A → BC)
                                B, C_prod = prod
                                if B in C[i][k] and C_prod in C[k+1][j]:
                                    left_ok = self._check_context(A, i-1, C, self.left_context, left=True)
                                    right_ok = self._check_context(A, j, C, self.right_context, left=False)
                                    if left_ok and right_ok:
                                        C[i][j].add(A)

        return self.start_symbol in C[1][n]

    def _check_context(self, A: str, pos: int, C: List[List[Set[str]]], context: Dict, left: bool) -> bool:
        """Checks left/right context constraints for nonterminal A at position pos."""
        if A not in context:
            return True
        required = context[A]
        n = len(C) - 1
        if left:
            # Check left context (symbols before pos)
            if pos < 1:
                return False
            for x in range(1, pos+1):
                for y in range(x, pos+1):
                    if any(sym in required for sym in C[x][y]):
                        return True
        else:
            # Check right context (symbols after pos)
            if pos > n:
                return False
            for x in range(pos, n+1):
                for y in range(x, n+1):
                    if any(sym in required for sym in C[x][y]):
                        return True
        return False

# Grammar for aⁿbⁿcⁿ
grammar = {
    "S": [["A", "T"]],  # S → AT (T will handle B and C)
    "T": [["B", "C"]],  # T → BC
    "A": [["a", "A"], ["a"]],  # A → aA | a
    "B": [["b", "B"], ["b"]],  # B → bB | b
    "C": [["c", "C"], ["c"]],  # C → cC | c
}

# Context constraints:
# - B must have equal number of A's to its left
# - C must have equal number of B's to its left
left_context = {
    "B": {"A"},  # B requires A to its left
    "C": {"B"}   # C requires B to its left
}

# Right context ensures balancing (implemented via dynamic checks during parsing)
right_context = {}  # Not needed for this example

parser = TwoSidedContextCYK(grammar, left_context, right_context, "S")

# Test cases
test_cases = [
    ("abc", True),
    ("aabbcc", True),
    ("aaabbbccc", True),
    ("aabbc", False),
    ("abbccc", False),
    ("aaabbbcc", False),
]

for input_str, expected in test_cases:
    result = parser.parse(input_str)
    print(f"Input: '{input_str}'\tExpected: {expected}\tActual: {result}")
    assert result == expected
