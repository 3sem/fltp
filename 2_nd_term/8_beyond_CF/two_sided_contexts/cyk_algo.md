# Two-Sided Context Parsing Algorithm (Extended from CYK)

## Introduction
This algorithm extends the Cocke-Younger-Kasami (CYK) algorithm to handle grammars with two-sided context constraints. It maintains the CYK approach of dynamic programming with a chart data structure, but adds context checking on both left and right sides of productions.

## Algorithm: Two-Sided Context CYK Parser

### Input:
- A context-sensitive grammar G = (V, Σ, P, S) where productions may have left and right context constraints
- An input string w = a₁a₂...aₙ ∈ Σ*

### Data Structures:
- A chart C[n+1][n+1] where each cell C[i,j] contains a set of nonterminals
- For each nonterminal A, maintain left and right context sets: left_context(A) and right_context(A)

### Initialization:
```
for i = 1 to n:
    for each production A → a where a = w[i]:
        if (left_context(A) is satisfied by left neighbors) AND 
           (right_context(A) is satisfied by right neighbors):
            add A to C[i,1]
```

### Main Algorithm:
```
for length = 2 to n:                // Length of span
    for i = 1 to n-length+1:        // Starting position
        j = i + length - 1          // Ending position
        for k = i to j-1:           // Partition point
            for each production A → BC:
                if B ∈ C[i,k] AND C ∈ C[k+1,j]:
                    // Check left context of A (symbols to the left of position i)
                    left_ok = check_left_context(A, i-1)
                    
                    // Check right context of A (symbols to the right of position j)
                    right_ok = check_right_context(A, j+1)
                    
                    if left_ok AND right_ok:
                        add A to C[i,j]
```

### Context Checking Functions:

```
function check_left_context(A, pos):
    if pos < 1: 
        return True if left_context(A) permits sentence start
    for each symbol X in left_context(A):
        if X matches any nonterminal in C[1,pos]:
            return True
    return False

function check_right_context(A, pos):
    if pos > n: 
        return True if right_context(A) permits sentence end
    for each symbol Y in right_context(A):
        if Y matches any nonterminal in C[pos,n]:
            return True
    return False
```

### Acceptance:
The input string w is accepted if S ∈ C[1,n] with all context constraints satisfied.

## Complexity Analysis:
- Time complexity: O(n³·|P|·c) where c is the cost of context checking
- Space complexity: O(n²)

## Example Grammar Handling:
For a production like:
A → BC | X _ Y
(where X is left context and Y is right context)

The algorithm would:
1. Find B and C in the appropriate chart cells
2. Verify that X appears somewhere to the left of the span
3. Verify that Y appears somewhere to the right of the span
4. Only then add A to the chart cell

## Extensions:
- Can be modified to handle bounded context-sensitive grammars
- Can incorporate probabilistic weights for probabilistic parsing
- Can be optimized with memoization of context checks
