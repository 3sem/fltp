### **How the Memoization Table Works in Packrat Parsing**

The **memoization table** is the key innovation in Bryan Ford's Packrat algorithm that ensures **O(n) linear-time parsing** for PEGs. Here's a deep dive into how it prevents exponential backtracking:

---

## **1. Structure of the Memoization Table**
The table stores results of parsing attempts at every **(position, rule)** pair in the input:

```python
memo = {
    (0, "rule_A"): MemoEntry(ast="a", pos=1, state="success"),
    (1, "rule_B"): MemoEntry(ast=None, pos=1, state="fail"),
    (2, "rule_S"): MemoEntry(ast=["a","b"], pos=3, state="success"),
    ...
}
```

- **Key** = `(position_in_input, grammar_rule)`
- **Value** = Cached result (`success`/`fail` + parsed AST + next position)

---

## **2. How It Prevents Exponential Backtracking**
### **Problem Without Memoization**
In naive recursive descent parsing:
- The same rule may be tried **multiple times at the same input position**.
- This leads to **combinatorial explosion** (O(2ⁿ) time) for grammars with backtracking.

**Example:**
```
Rule:  A ← 'a' A / 'a'
Input: "aaa"
```
Without memoization, parsing `A` at position `0` would re-parse `A` at positions `1`, `2`, etc., redundantly.

### **Solution: Memoization**
1. **Before parsing a (position, rule) pair**, check the memo table.
2. **If cached**, reuse the result (success/fail + AST).
3. **If not cached**, parse and store the result.

**Effect:**  
- Each `(position, rule)` pair is evaluated **only once**.
- Reduces time complexity from **O(2ⁿ) → O(n)**.

---

## **3. Step-by-Step Example**
### **Grammar:**
```
S ← A B
A ← 'a' A / 'a'
B ← 'b' B / 'b'
```
### **Input:** `"aabb"`

#### **Parsing Steps:**
1. **Parse `S` at pos=0:**
   - Calls `A` at pos=0 → `'a' A` → succeeds (ast=`"a"`, next pos=1)
   - Calls `A` at pos=1 → `'a' A` → succeeds (ast=`"a"`, next pos=2)
   - Calls `B` at pos=2 → `'b' B` → succeeds (ast=`"b"`, next pos=3)
   - Calls `B` at pos=3 → `'b' B` → succeeds (ast=`"b"`, next pos=4)
   - **Result:** `S → ["a","a","b","b"]`

2. **Memo Table After Parsing:**
   | Position | Rule | Result              |
   |----------|------|---------------------|
   | 0        | A    | Success (ast="a", pos=1) |
   | 1        | A    | Success (ast="a", pos=2) |
   | 2        | B    | Success (ast="b", pos=3) |
   | 3        | B    | Success (ast="b", pos=4) |

3. **If we parsed `"aabb"` again:**
   - All `(pos, rule)` pairs would **hit the cache**.
   - No redundant computation!

---

## **4. Handling Left Recursion (Original Limitation)**
Ford’s original algorithm **did not support left recursion**:
```
A ← A 'a' / 'a'  # Infinite loop at pos=0!
```
### **Why?**
- `A` at pos=0 calls `A` at pos=0 → infinite recursion.
- **Solution:** Later extensions (Warth et al., 2008) added left-recursion support by:
  1. Detecting cycles in the memo table.
  2. Growing the parse incrementally.

---

## **5. Space-Time Tradeoff**
| Metric       | Without Memoization | With Memoization |
|--------------|---------------------|------------------|
| **Time**     | O(2ⁿ)               | O(n)             |
| **Space**    | O(1)                | O(n)             |

**Optimizations:**
- **Garbage collection**: Discard memo entries for unreachable positions.
- **Lazy cleaning**: Only memoize "hot" rules.

---

## **6. Python Pseudocode for Memoization**
```python
def parse(rule, pos):
    key = (pos, rule)
    if key in memo:
        return memo[key]  # Cache hit
    
    # Mark as "in progress" to detect left recursion
    memo[key] = MemoEntry(state="parsing")
    
    # Actual parsing (recursive calls)
    result = rule(pos)
    
    # Store result
    memo[key] = MemoEntry(
        ast=result.ast,
        pos=result.pos,
        state="success" if result else "fail"
    )
    return memo[key]
```

---

### **Key Takeaways**
1. **Memoization eliminates redundant work** by caching rule results per position.
2. **Guarantees O(n) time** for any PEG (but uses O(n) space).
3. **Left recursion requires extensions** (not in Ford’s original algorithm).
4. **Real-world implementations** (like Python’s `pegen`) use optimizations to reduce memory usage.

