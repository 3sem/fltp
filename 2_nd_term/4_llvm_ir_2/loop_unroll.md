1. First, let's start with a simple C program with a loop:

```c
// loop.c
#define N 100

int main() {
  int sum = 0;
  for (int i = 0; i < N; i++) {
    sum += i;
  }
  return sum;
}
```

2. Compile this to LLVM IR:

```
clang -O1 -emit-llvm loop.c -S -o loop.ll
```

3. Use opt to apply loop unrolling with different factors:

No unrolling (baseline):
```
opt -S loop.ll -o loop_no_unroll.ll
```

Unroll factor of 2:
```
opt -S -loop-unroll -unroll-count=2 loop.ll -o loop_unroll_2.ll
```

Unroll factor of 4:
```
opt -S -loop-unroll -unroll-count=4 loop.ll -o loop_unroll_4.ll
```

Unroll factor of 8:
```
opt -S -loop-unroll -unroll-count=8 loop.ll -o loop_unroll_8.ll
```

Full unrolling:
```
opt -S -loop-unroll -unroll-count=100 loop.ll -o loop_full_unroll.ll
```

4. You can then examine the resulting .ll files to see how the loop has been unrolled.

Some key points:

- The -loop-unroll pass enables loop unrolling
- -unroll-count specifies the unroll factor
- Setting -unroll-count to the full loop count (100 in this case) attempts full unrolling
- Other useful flags include -unroll-threshold to control the maximum code size increase
- Use -debug-only=loop-unroll for verbose output on unrolling decisions

The unrolled loops will have the body replicated multiple times, with adjusted iteration counts and exit conditions. Full unrolling eliminates the loop entirely if possible.

Remember that the actual unrolling may be limited by other heuristics in the compiler, so the resulting IR may not always match the exact unroll factor requested.

For further test: use N different from 100, use N that is not known at compile time.

---
undefined: https://labs.perplexity.ai/?utm_source=copy_output
