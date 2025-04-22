from typing import Dict, Set, Tuple

def two_sided_context_hellings(
    grammar: Dict[str, List[List[str]]],
    left_context: Dict[str, Set[str]],
    right_context: Dict[str, Set[str]],
    input_string: str
) -> bool:
    """Hellings-style relational algebra implementation of two-sided context CYK."""
    n = len(input_string)
    if n == 0:
        return False

    # Initialize relations
    N = {nt: set() for nt in grammar}  # Nonterminal relations (i,j)
    L = {nt: set() for nt in grammar}  # Left context relations
    R = {nt: set() for nt in grammar}  # Right context relations

    # Base case: terminals
    for i in range(n):
        char = input_string[i]
        for A, prods in grammar.items():
            for prod in prods:
                if len(prod) == 1 and prod[0] == char:
                    # Add to N_A if contexts are satisfied
                    left_ok = not left_context.get(A) or any(
                        (k, i) in L[lc] for lc in left_context[A] for k in range(i)
                    )
                    right_ok = not right_context.get(A) or any(
                        (i+1, k) in R[rc] for rc in right_context[A] for k in range(i+1, n+1)
                    )
                    if left_ok and right_ok:
                        N[A].add((i, i+1))

    # Initialize context relations
    for A in grammar:
        L[A] = N[A].copy()
        R[A] = N[A].copy()

    # Main algorithm
    changed = True
    while changed:
        changed = False
        for A, prods in grammar.items():
            for prod in prods:
                if len(prod) == 2:  # A → BC
                    B, C = prod
                    # Standard composition
                    new_pairs = {
                        (i, k) for (i, j) in N[B] for (j2, k) in N[C] 
                        if j == j2
                    }
                    # Apply left context
                    if left_context.get(A):
                        new_pairs = {
                            (i, k) for (i, k) in new_pairs
                            if any((m, i) in L[lc] for lc in left_context[A] for m in range(i))
                        }
                    # Apply right context
                    if right_context.get(A):
                        new_pairs = {
                            (i, k) for (i, k) in new_pairs
                            if any((k, m) in R[rc] for rc in right_context[A] for m in range(k, n+1))
                        }
                    # Update N_A
                    prev_size = len(N[A])
                    N[A].update(new_pairs)
                    if len(N[A]) > prev_size:
                        changed = True
                        # Update context relations
                        L[A].update((i, j) for (i, j) in new_pairs)
                        R[A].update((i, j) for (i, j) in new_pairs)

    return (0, n) in N['S']
