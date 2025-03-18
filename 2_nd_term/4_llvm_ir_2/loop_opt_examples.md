Below are the **C code examples**, **LLVM IR before transformation**, **LLVM IR after transformation**, and a **short description of the pass meaning** for each of the **loop optimization passes** in LLVM.

---

### 1. **Loop Invariant Code Motion (LICM)**

#### C Code
```c
void licm_example(int n, int* arr) {
    int sum = 10;  // Loop-invariant computation
    for (int i = 0; i < n; i++) {
        arr[i] = sum + i;
    }
}
```

#### LLVM IR (Before)
```llvm
define void @licm_example(i32 %n, i32* %arr) {
entry:
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
  %sum = add i32 %i, 10  ; Loop-invariant computation
  store i32 %sum, i32* %arr
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop, label %exit

exit:
  ret void
}
```

#### LLVM IR (After)
```llvm
define void @licm_example(i32 %n, i32* %arr) {
entry:
  %sum = add i32 0, 10  ; Moved outside the loop
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
  store i32 %sum, i32* %arr
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop, label %exit

exit:
  ret void
}
```

#### Description
- **LICM** moves loop-invariant computations (e.g., `%sum = add i32 %i, 10`) outside the loop to reduce redundant computations.

---

### 2. **Loop Rotation**

#### C Code
```c
void rotate_example(int n, int* arr) {
    for (int i = 0; i < n; i++) {
        arr[i] = i;
    }
}
```

#### LLVM IR (Before)
```llvm
define void @rotate_example(i32 %n, i32* %arr) {
entry:
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
  store i32 %i, i32* %arr
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop, label %exit

exit:
  ret void
}
```

#### LLVM IR (After)
```llvm
define void @rotate_example(i32 %n, i32* %arr) {
entry:
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop, label %exit

exit:
  ret void
}
```

#### Description
- **Loop Rotation** simplifies loop control flow by rotating the loop to make it easier to optimize.

---

### 3. **Loop Vectorization**

#### C Code
```c
void vectorize_example(int n, int* arr) {
    for (int i = 0; i < n; i++) {
        arr[i] = i;
    }
}
```

#### LLVM IR (Before)
```llvm
define void @vectorize_example(i32 %n, i32* %arr) {
entry:
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
  %ptr = getelementptr i32, i32* %arr, i32 %i
  store i32 %i, i32* %ptr
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop, label %exit

exit:
  ret void
}
```

#### LLVM IR (After)
```llvm
define void @vectorize_example(i32 %n, i32* %arr) {
entry:
  br label %vector.body

vector.body:
  %index = phi i32 [ 0, %entry ], [ %index.next, %vector.body ]
  %wide.load = load <4 x i32>, <4 x i32>* %arr
  store <4 x i32> %wide.load, <4 x i32>* %arr
  %index.next = add i32 %index, 4
  %cond = icmp slt i32 %index.next, %n
  br i1 %cond, label %vector.body, label %exit

exit:
  ret void
}
```

#### Description
- **Loop Vectorization** transforms the loop to use SIMD instructions for parallel execution.

---

### 4. **Loop Unswitch**

#### C Code
```c
void unswitch_example(int n, int flag, int* arr) {
    for (int i = 0; i < n; i++) {
        if (flag) {
            arr[i] = i;
        } else {
            arr[i] = 0;
        }
    }
}
```

#### LLVM IR (Before)
```llvm
define void @unswitch_example(i32 %n, i1 %flag, i32* %arr) {
entry:
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
  br i1 %flag, label %true, label %false

true:
  store i32 %i, i32* %arr
  br label %merge

false:
  store i32 0, i32* %arr
  br label %merge

merge:
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop, label %exit

exit:
  ret void
}
```

#### LLVM IR (After)
```llvm
define void @unswitch_example(i32 %n, i1 %flag, i32* %arr) {
entry:
  br i1 %flag, label %loop.true, label %loop.false

loop.true:
  %i.true = phi i32 [ 0, %entry ], [ %i.next.true, %loop.true ]
  store i32 %i.true, i32* %arr
  %i.next.true = add i32 %i.true, 1
  %cond.true = icmp slt i32 %i.next.true, %n
  br i1 %cond.true, label %loop.true, label %exit

loop.false:
  %i.false = phi i32 [ 0, %entry ], [ %i.next.false, %loop.false ]
  store i32 0, i32* %arr
  %i.next.false = add i32 %i.false, 1
  %cond.false = icmp slt i32 %i.next.false, %n
  br i1 %cond.false, label %loop.false, label %exit

exit:
  ret void
}
```

#### Description
- **Loop Unswitch** moves loop-invariant conditionals (e.g., `if (flag)`) outside the loop to reduce control flow overhead.

---

### 5. **Loop Interchange**

#### C Code
```c
void interchange_example(int n, int m, int* arr) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            arr[i * m + j] = i;
        }
    }
}
```

#### LLVM IR (Before)
```llvm
define void @interchange_example(i32 %n, i32 %m, i32* %arr) {
entry:
  br label %outer

outer:
  %i = phi i32 [ 0, %entry ], [ %i.next, %outer.latch ]
  br label %inner

inner:
  %j = phi i32 [ 0, %outer ], [ %j.next, %inner ]
  %idx = mul i32 %i, %m
  %idx2 = add i32 %idx, %j
  %ptr = getelementptr i32, i32* %arr, i32 %idx2
  store i32 %i, i32* %ptr
  %j.next = add i32 %j, 1
  %cond = icmp slt i32 %j.next, %m
  br i1 %cond, label %inner, label %outer.latch

outer.latch:
  %i.next = add i32 %i, 1
  %cond2 = icmp slt i32 %i.next, %n
  br i1 %cond2, label %outer, label %exit

exit:
  ret void
}
```

#### LLVM IR (After)
```llvm
define void @interchange_example(i32 %n, i32 %m, i32* %arr) {
entry:
  br label %inner

inner:
  %j = phi i32 [ 0, %entry ], [ %j.next, %inner.latch ]
  br label %outer

outer:
  %i = phi i32 [ 0, %inner ], [ %i.next, %outer ]
  %idx = mul i32 %i, %m
  %idx2 = add i32 %idx, %j
  %ptr = getelementptr i32, i32* %arr, i32 %idx2
  store i32 %i, i32* %ptr
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %outer, label %inner.latch

inner.latch:
  %j.next = add i32 %j, 1
  %cond2 = icmp slt i32 %j.next, %m
  br i1 %cond2, label %inner, label %exit

exit:
  ret void
}
```

#### Description
- **Loop Interchange** swaps nested loops to improve cache locality and enable other optimizations.

---

### 6. **Loop Distribution**

#### C Code
```c
void distribute_example(int n, int* arr1, int* arr2) {
    for (int i = 0; i < n; i++) {
        arr1[i] = i;
        arr2[i] = i;
    }
}
```

#### LLVM IR (Before)
```llvm
define void @distribute_example(i32 %n, i32* %arr1, i32* %arr2) {
entry:
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
  %ptr1 = getelementptr i32, i32* %arr1, i32 %i
  store i32 %i, i32* %ptr1
  %ptr2 = getelementptr i32, i32* %arr2, i32 %i
  store i32 %i, i32* %ptr2
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop, label %exit

exit:
  ret void
}
```

#### LLVM IR (After)
```llvm
define void @distribute_example(i32 %n, i32* %arr1, i32* %arr2) {
entry:
  br label %loop1

loop1:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop1 ]
  %ptr1 = getelementptr i32, i32* %arr1, i32 %i
  store i32 %i, i32* %ptr1
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop1, label %loop2

loop2:
  %j = phi i32 [ 0, %loop1 ], [ %j.next, %loop2 ]
  %ptr2 = getelementptr i32, i32* %arr2, i32 %j
  store i32 %j, i32* %ptr2
  %j.next = add i32 %j, 1
  %cond2 = icmp slt i32 %j.next, %n
  br i1 %cond2, label %loop2, label %exit

exit:
  ret void
}
```

#### Description
- **Loop Distribution** splits a loop into multiple loops to enable parallelization or other optimizations.

---

### 7. **Loop Fusion**

#### C Code
```c
void fusion_example(int n, int* arr1, int* arr2) {
    for (int i = 0; i < n; i++) {
        arr1[i] = i;
    }
    for (int i = 0; i < n; i++) {
        arr2[i] = i;
    }
}
```

#### LLVM IR (Before)
```llvm
define void @fusion_example(i32 %n, i32* %arr1, i32* %arr2) {
entry:
  br label %loop1

loop1:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop1 ]
  %ptr1 = getelementptr i32, i32* %arr1, i32 %i
  store i32 %i, i32* %ptr1
  %i.next = add i32 %i, 1
  %cond1 = icmp slt i32 %i.next, %n
  br i1 %cond1, label %loop1, label %loop2

loop2:
  %j = phi i32 [ 0, %loop1 ], [ %j.next, %loop2 ]
  %ptr2 = getelementptr i32, i32* %arr2, i32 %j
  store i32 %j, i32* %ptr2
  %j.next = add i32 %j, 1
  %cond2 = icmp slt i32 %j.next, %n
  br i1 %cond2, label %loop2, label %exit

exit:
  ret void
}
```

#### LLVM IR (After)
```llvm
define void @fusion_example(i32 %n, i32* %arr1, i32* %arr2) {
entry:
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
  %ptr1 = getelementptr i32, i32* %arr1, i32 %i
  store i32 %i, i32* %ptr1
  %ptr2 = getelementptr i32, i32* %arr2, i32 %i
  store i32 %i, i32* %ptr2
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop, label %exit

exit:
  ret void
}
```

#### Description
- **Loop Fusion** combines multiple loops into a single loop to reduce loop overhead and improve cache locality.

---

### 8. **Loop Deletion**

#### C Code
```c
void deletion_example(int n) {
    for (int i = 0; i < n; i++) {
        // No effect
    }
}
```

#### LLVM IR (Before)
```llvm
define void @deletion_example(i32 %n) {
entry:
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop, label %exit

exit:
  ret void
}
```

#### LLVM IR (After)
```llvm
define void @deletion_example(i32 %n) {
entry:
  ret void
}
```

#### Description
- **Loop Deletion** removes loops that have no effect (e.g., loops with no side effects or infinite loops with no exits).

---

### 9. **Loop Idiom Recognition**

#### C Code
```c
void idiom_example(int n, char* arr) {
    for (int i = 0; i < n; i++) {
        arr[i] = 0;
    }
}
```

#### LLVM IR (Before)
```llvm
define void @idiom_example(i32 %n, i8* %arr) {
entry:
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
  %ptr = getelementptr i8, i8* %arr, i32 %i
  store i8 0, i8* %ptr
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop, label %exit

exit:
  ret void
}
```

#### LLVM IR (After)
```llvm
define void @idiom_example(i32 %n, i8* %arr) {
entry:
  call void @llvm.memset.p0i8.i32(i8* %arr, i8 0, i32 %n, i1 false)
  ret void
}
```

#### Description
- **Loop Idiom Recognition** recognizes common loop patterns (e.g., `memset`) and replaces them with more efficient implementations.

---

### 10. **Loop Rerolling**

#### C Code
```c
void reroll_example(int n, int* arr) {
    for (int i = 0; i < n; i++) {
        arr[i] = i;
    }
}
```

#### LLVM IR (Before)
```llvm
define void @reroll_example(i32 %n, i32* %arr) {
entry:
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
  %ptr1 = getelementptr i32, i32* %arr, i32 %i
  store i32 %i, i32* %ptr1
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop, label %exit

exit:
  ret void
}
```

#### LLVM IR (After)
```llvm
define void @reroll_example(i32 %n, i32* %arr) {
entry:
  br label %loop

loop:
  %i = phi i32 [ 0, %entry ], [ %i.next, %loop ]
  %ptr1 = getelementptr i32, i32* %arr, i32 %i
  store i32 %i, i32* %ptr1
  %i.next = add i32 %i, 1
  %cond = icmp slt i32 %i.next, %n
  br i1 %cond, label %loop, label %exit

exit:
  ret void
}
```

#### Description
- **Loop Rerolling** re-rolls partially unrolled loops to reduce code size and improve performance.

---

### Summary
Each example demonstrates the **C code**, **LLVM IR before transformation**, **LLVM IR after transformation**, and a **short description of the pass meaning**. These examples illustrate how each loop optimization pass transforms the IR to improve performance, efficiency, or correctness.
