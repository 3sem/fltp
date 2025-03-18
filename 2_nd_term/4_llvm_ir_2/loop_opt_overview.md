In LLVM's **`opt` tool**, there are several **loop optimization passes** available besides **loop unrolling**. These passes are designed to improve the performance, efficiency, and correctness of loops in LLVM Intermediate Representation (IR). Below is a list of **loop optimization passes** in LLVM, along with a brief description of each:

---

### 1. **Loop Invariant Code Motion (LICM)**
   - **Description**: Moves loop-invariant code (code that does not change across loop iterations) outside the loop to reduce redundant computations.
   - **Command**: `-licm`

---

### 2. **Loop Rotation**
   - **Description**: Rotates loops to simplify loop control flow and enable other optimizations (e.g., LICM).
   - **Command**: `-loop-rotate`

---

### 3. **Loop Vectorization**
   - **Description**: Transforms loops to execute multiple iterations in parallel using SIMD (Single Instruction, Multiple Data) instructions.
   - **Command**: `-loop-vectorize`

---

### 4. **Loop Unswitch**
   - **Description**: Moves loop-invariant conditional branches (e.g., `if` conditions) outside the loop to reduce control flow overhead.
   - **Command**: `-loop-unswitch`

---

### 5. **Loop Interchange**
   - **Description**: Interchanges nested loops to improve cache locality and enable other optimizations.
   - **Command**: `-loop-interchange`

---

### 6. **Loop Distribution**
   - **Description**: Splits a loop into multiple loops to enable parallelization or other optimizations.
   - **Command**: `-loop-distribute`

---

### 7. **Loop Fusion**
   - **Description**: Combines multiple loops into a single loop to reduce loop overhead and improve cache locality.
   - **Command**: `-loop-fusion`

---

### 8. **Loop Deletion**
   - **Description**: Removes loops that have no effect (e.g., loops with no side effects or infinite loops with no exits).
   - **Command**: `-loop-deletion`

---

### 9. **Loop Idiom Recognition**
   - **Description**: Recognizes and optimizes common loop patterns (e.g., memset, memcpy) into more efficient implementations.
   - **Command**: `-loop-idiom`

---

### 10. **Loop Rerolling**
   - **Description**: Re-rolls loops that have been partially unrolled to reduce code size and improve performance.
   - **Command**: `-loop-reroll`

---

### 11. **Loop Strength Reduction**
   - **Description**: Replaces expensive loop operations (e.g., multiplications) with cheaper equivalents (e.g., additions).
   - **Command**: `-loop-strength-reduce`

---

### 12. **Loop Predication**
   - **Description**: Converts control flow (e.g., `if` conditions) into predicated instructions to reduce branching overhead.
   - **Command**: `-loop-predication`

---

### 13. **Loop Versioning**
   - **Description**: Creates multiple versions of a loop optimized for different runtime conditions (e.g., aliasing, bounds).
   - **Command**: `-loop-versioning`

---

### 14. **Loop Sink**
   - **Description**: Sinks loop-invariant instructions (e.g., loads) into the loop to reduce register pressure.
   - **Command**: `-loop-sink`

---

### 15. **Loop Simplify**
   - **Description**: Simplifies loop structures to make them easier to analyze and optimize.
   - **Command**: `-loop-simplify`

---

### 16. **Loop Load Elimination**
   - **Description**: Eliminates redundant loads within loops to improve performance.
   - **Command**: `-loop-load-elim`

---

### 17. **Loop Data Prefetch**
   - **Description**: Inserts prefetch instructions to reduce memory latency in loops.
   - **Command**: `-loop-data-prefetch`

---

### 18. **Loop Flatten**
   - **Description**: Flattens nested loops into a single loop to simplify control flow and enable other optimizations.
   - **Command**: `-loop-flatten`

---

### 19. **Loop Unroll and Jam**
   - **Description**: Unrolls outer loops and fuses (jams) inner loops to improve parallelism and cache locality.
   - **Command**: `-loop-unroll-and-jam`

---

### 20. **Loop Guard Widening**
   - **Description**: Widens loop guards (e.g., bounds checks) to reduce the number of checks performed in the loop.
   - **Command**: `-loop-guard-widening`

---

### Summary of Loop Optimization Passes

| Pass Name                  | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| **LICM**                   | Moves loop-invariant code outside the loop.                                 |
| **Loop Rotation**          | Rotates loops to simplify control flow.                                     |
| **Loop Vectorization**     | Transforms loops to use SIMD instructions.                                  |
| **Loop Unswitch**          | Moves loop-invariant conditionals outside the loop.                         |
| **Loop Interchange**       | Interchanges nested loops for better cache locality.                        |
| **Loop Distribution**      | Splits loops into multiple loops for parallelization.                       |
| **Loop Fusion**            | Combines multiple loops into one.                                           |
| **Loop Deletion**          | Removes ineffective loops.                                                  |
| **Loop Idiom Recognition** | Optimizes common loop patterns (e.g., memset, memcpy).                      |
| **Loop Rerolling**         | Re-rolls partially unrolled loops.                                          |
| **Loop Strength Reduction**| Replaces expensive operations with cheaper ones.                            |
| **Loop Predication**       | Converts control flow into predicated instructions.                         |
| **Loop Versioning**        | Creates multiple versions of a loop for different conditions.               |
| **Loop Sink**              | Sinks loop-invariant instructions into the loop.                            |
| **Loop Simplify**          | Simplifies loop structures for easier optimization.                         |
| **Loop Load Elimination**  | Eliminates redundant loads in loops.                                        |
| **Loop Data Prefetch**     | Inserts prefetch instructions to reduce memory latency.                     |
| **Loop Flatten**           | Flattens nested loops into a single loop.                                   |
| **Loop Unroll and Jam**    | Unrolls outer loops and fuses inner loops.                                  |
| **Loop Guard Widening**    | Widens loop guards to reduce checks.                                        |

---

### Example Usage in `opt`
To apply these passes using the `opt` tool, you can use the following command:
```bash
opt -pass1 -pass2 -pass3 ... -o output.bc input.bc
```
For example, to apply **Loop Vectorization** and **Loop Unswitch**:
```bash
opt -loop-vectorize -loop-unswitch -o output.bc input.bc
```

---

### Summary
LLVM provides a rich set of **loop optimization passes** that can be used to improve the performance, efficiency, and correctness of loops in LLVM IR. These passes can be combined and applied using the `opt` tool or integrated into custom optimization pipelines.
