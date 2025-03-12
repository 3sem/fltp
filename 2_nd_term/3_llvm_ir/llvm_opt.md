Here are examples of how to use **LLVM's `opt` tool** to apply the optimizations you mentioned. The `opt` tool is part of the LLVM project and is used to apply optimizations to LLVM Intermediate Representation (IR) code. Below, I provide commands and explanations for each optimization.

---

### 1. **Constant Folding**
   - **Description**: Evaluates constant expressions at compile time.
   - **LLVM `opt` Command**:
     ```bash
     opt -O1 -S input.ll -o output.ll
     ```
   - **Example**:
     ```llvm
     ; Input IR
     define double @example(double %x) {
         %y = fmul double 2.000000e+00, 0x3FE279A74590331C ; 2 * sin(0.5)
         %result = fmul double %y, %x
         ret double %result
     }
     ```
     After constant folding:
     ```llvm
     ; Output IR
     define double @example(double %x) {
         %result = fmul double 1.919034e+00, %x ; Folded constant
         ret double %result
     }
     ```

---

### 2. **Constant Propagation**
   - **Description**: Replaces variables with their constant values.
   - **LLVM `opt` Command**:
     ```bash
     opt -constprop -S input.ll -o output.ll
     ```
   - **Example**:
     ```llvm
     ; Input IR
     define double @example(double %r) {
         %pi = fadd double 3.141500e+00, 0.000000e+00
         %l = fmul double 2.000000e+00, %pi
         %result = fmul double %l, %r
         ret double %result
     }
     ```
     After constant propagation:
     ```llvm
     ; Output IR
     define double @example(double %r) {
         %result = fmul double 6.283000e+00, %r ; Propagated constant
         ret double %result
     }
     ```

---

### 3. **Dead Store Elimination (DSE)**
   - **Description**: Removes stores to variables that are never read.
   - **LLVM `opt` Command**:
     ```bash
     opt -dse -S input.ll -o output.ll
     ```
   - **Example**:
     ```llvm
     ; Input IR
     define i32 @example(i32 %a, i32 %b) {
         %c = add i32 %a, %b
         %z = add i32 1, %c
         store i32 %z, i32* @global_var
         %c_new = mul i32 %a, %b
         ret i32 %z
     }
     ```
     After DSE:
     ```llvm
     ; Output IR
     define i32 @example(i32 %a, i32 %b) {
         %c = add i32 %a, %b
         %z = add i32 1, %c
         ret i32 %z
     }
     ```

---

### 4. **Dead Code Elimination (DCE)**
   - **Description**: Removes code that does not affect the program's output.
   - **LLVM `opt` Command**:
     ```bash
     opt -dce -S input.ll -o output.ll
     ```
   - **Example**:
     ```llvm
     ; Input IR
     define i32 @example(i32 %a, i32 %b) {
         %c = add i32 %a, %b
         %d = mul i32 %c, %c
         ret i32 %c
     }
     ```
     After DCE:
     ```llvm
     ; Output IR
     define i32 @example(i32 %a, i32 %b) {
         %c = add i32 %a, %b
         ret i32 %c
     }
     ```

---

### 5. **Common Subexpression Elimination (CSE)**
   - **Description**: Eliminates redundant computations.
   - **LLVM `opt` Command**:
     ```bash
     opt -gvn -S input.ll -o output.ll
     ```
   - **Example**:
     ```llvm
     ; Input IR
     define double @example(double %v, double %u, double %w) {
         %t1 = call double @sin(double %u)
         %t2 = fdiv double %t1, 2.000000e+00
         %t3 = call double @cos(double %v)
         %t4 = fadd double 1.000000e+00, %t2
         %t5 = fmul double %t3, %t4
         %t6 = call double @sin(double %w)
         %t7 = fsub double 1.000000e+00, %t2
         %t8 = fmul double %t6, %t7
         %result = fadd double %t5, %t8
         ret double %result
     }
     ```
     After CSE:
     ```llvm
     ; Output IR
     define double @example(double %v, double %u, double %w) {
         %t1 = call double @sin(double %u)
         %t2 = fdiv double %t1, 2.000000e+00
         %t3 = call double @cos(double %v)
         %t4 = fadd double 1.000000e+00, %t2
         %t5 = fmul double %t3, %t4
         %t6 = call double @sin(double %w)
         %t7 = fsub double 1.000000e+00, %t2
         %t8 = fmul double %t6, %t7
         %result = fadd double %t5, %t8
         ret double %result
     }
     ```

---

### 6. **Function Inlining**
   - **Description**: Replaces function calls with the function's body.
   - **LLVM `opt` Command**:
     ```bash
     opt -inline -S input.ll -o output.ll
     ```
   - **Example**:
     ```llvm
     ; Input IR
     define i32 @add(i32 %a, i32 %b) {
         %result = add i32 %a, %b
         ret i32 %result
     }
     define i32 @example() {
         %x = call i32 @add(i32 2, i32 3)
         ret i32 %x
     }
     ```
     After inlining:
     ```llvm
     ; Output IR
     define i32 @example() {
         %x = add i32 2, 3
         ret i32 %x
     }
     ```

---

### 7. **Loop Unrolling**
   - **Description**: Unrolls loops to reduce overhead.
   - **LLVM `opt` Command**:
     ```bash
     opt -loop-unroll -S input.ll -o output.ll
     ```
   - **Example**:
     ```llvm
     ; Input IR
     define void @example(i32 %n) {
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
     After loop unrolling:
     ```llvm
     ; Output IR (partially unrolled)
     define void @example(i32 %n) {
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

---

These examples demonstrate how to use LLVM's `opt` tool to apply various optimizations. You can combine multiple passes using `-O1`, `-O2`, or `-O3` for higher-level optimizations.
