# **TableGen DAG Pattern Matching Explained with Examples**

TableGen uses **Directed Acyclic Graph (DAG) patterns** to match LLVM IR instructions to target-specific machine instructions. Below is a detailed breakdown with concrete examples.

---

## **1. How DAG Pattern Matching Works**
When `llc` compiles LLVM IR to machine code:
1. **LLVM IR** is converted into a **SelectionDAG**.
2. TableGen **matches DAG patterns** from `.td` files to select machine instructions.
3. The matched instructions are **scheduled and emitted** as assembly/object code.

---

## **2. Example: Matching `add` Instruction**
### **LLVM IR Input**
```llvm
%sum = add i32 %a, %b
```

### **SelectionDAG Representation**
```tablegen
(set i32:$sum, (add i32:$a, i32:$b))
```

### **TableGen Instruction Definition**
```tablegen
// In TargetInstrInfo.td
def ADD : Instruction<(outs GPR:$dst), (ins GPR:$src1, GPR:$src2),
                   "add $dst, $src1, $src2",
                   [(set GPR:$dst, (add GPR:$src1, GPR:$src2))]>;
```
- **`(outs GPR:$dst)`** → Result register (`$sum` in IR).
- **`(ins GPR:$src1, GPR:$src2)`** → Input registers (`%a`, `%b`).
- **`[(set GPR:$dst, (add GPR:$src1, GPR:$src2))]`** → Matches IR `add`.

---

## **3. Example: Matching `load` Instruction**
### **LLVM IR Input**
```llvm
%val = load i32, i32* %ptr
```

### **SelectionDAG Representation**
```tablegen
(set i32:$val, (load i32:$ptr))
```

### **TableGen Instruction Definition**
```tablegen
def LOAD : Instruction<(outs GPR:$dst), (ins GPR:$addr),
                    "ld $dst, [$addr]",
                    [(set GPR:$dst, (load GPR:$addr))]>;
```
- Matches **`load` IR instruction** with a base address.

---

## **4. Example: Matching `store` Instruction**
### **LLVM IR Input**
```llvm
store i32 %val, i32* %ptr
```

### **SelectionDAG Representation**
```tablegen
(store i32:$val, i32:$ptr)
```

### **TableGen Instruction Definition**
```tablegen
def STORE : Instruction<(outs), (ins GPR:$addr, GPR:$val),
                     "st [$addr], $val",
                     [(store GPR:$val, GPR:$addr)]>;
```
- No output (`outs` is empty).
- Matches **`store` IR instruction**.

---

## **5. Complex Example: Memory Access with Offset**
### **LLVM IR Input**
```llvm
%val = load i32, i32* getelementptr ([i32], [i32]* %arr, i32 4)
```
(Equivalent to `arr[4]` in C.)

### **SelectionDAG Representation**
```tablegen
(set i32:$val, (load (add GPR:$arr, (i32 16))))
```
(Assuming `i32` is 4 bytes, offset `4 * 4 = 16`.)

### **TableGen Instruction Definition**
```tablegen
def LOAD_OFFSET : Instruction<(outs GPR:$dst), (ins GPR:$base, i32imm:$offset),
                            "ld $dst, [$base + $offset]",
                            [(set GPR:$dst, (load (add GPR:$base, imm:$offset))]>;
```
- Matches **`load (add base, offset)`** pattern.

---

## **6. Example: Conditional Branch**
### **LLVM IR Input**
```llvm
br i1 %cond, label %true, label %false
```

### **SelectionDAG Representation**
```tablegen
(brcond (seteq i32:$cond, 0), bb:$false, bb:$true)
```

### **TableGen Instruction Definition**
```tablegen
def BEQ : Instruction<(outs), (ins GPR:$cond, bb:$target),
                   "beq $cond, $target",
                   [(brcond (seteq GPR:$cond, 0), bb:$target)]>;
```
- Matches **`brcond`** (branch-if-equal-zero).

---

## **7. Key Takeaways**
| **IR Instruction** | **SelectionDAG** | **TableGen Pattern** |
|---------------------|------------------|----------------------|
| `add %a, %b` | `(set $dst, (add $a, $b))` | `[(set GPR:$dst, (add GPR:$a, GPR:$b))]` |
| `load %ptr` | `(set $dst, (load $ptr))` | `[(set GPR:$dst, (load GPR:$ptr))]` |
| `store %val, %ptr` | `(store $val, $ptr)` | `[(store GPR:$val, GPR:$ptr)]` |
| `load (arr + 4)` | `(load (add $arr, 16))` | `[(load (add GPR:$arr, imm:$offset))]` |
| `br %cond, %bb` | `(brcond (seteq $cond, 0), $bb)` | `[(brcond (seteq GPR:$cond, 0), bb:$target)]` |

---

## **8. How LLVM Uses These Patterns**
1. **`llc`** converts LLVM IR → **SelectionDAG**.
2. **Pattern matcher** searches `.td` files for matching DAGs.
3. **Replaces IR nodes** with machine instructions.
4. **Emits assembly** (or object code).

---

## **9. Debugging Pattern Matching**
If a pattern **doesn’t match**, use:
```sh
llc -debug-only=isel input.ll
```
This shows **why a pattern failed** (e.g., mismatched operand types).

---

## **10. Summary**
- **DAG patterns** define how LLVM IR maps to machine instructions.
- **`(set dst, (op src1, src2))`** is the most common form.
- **Complex patterns** (e.g., `load (add base, offset)`) are supported.
- **`brcond`** handles conditional branches.

This system allows LLVM to **generate efficient machine code** from high-level IR! 🚀
