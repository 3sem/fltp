# **TableGen Syntax Deep Dive**

TableGen (`.td`) is a declarative language used in LLVM to define **target descriptions** (instructions, registers, scheduling, etc.). Below is a comprehensive breakdown of its syntax with examples.

---

## **1. Basic Structure**
A TableGen file consists of:
- **Definitions** (`def`): Concrete instances (e.g., an instruction).
- **Classes** (`class`): Reusable templates.
- **Multiclasses** (`multiclass`): Groups of related definitions.
- **`let`** statements: Override default values.

### **Example: Basic Class and Definition**
```tablegen
// Define a class for arithmetic instructions
class ArithInst<dag outs, dag ins, string asmstr> {
  dag OutOperandList = outs;
  dag InOperandList = ins;
  string AsmString = asmstr;
  bit isCommutable = 1;  // Instruction is commutative (e.g., ADD)
}

// Define an ADD instruction
def ADD : ArithInst<(outs GPR:$dst), (ins GPR:$src1, GPR:$src2), "add $dst, $src1, $src2">;
```

---

## **2. Data Types in TableGen**
| Type | Example | Description |
|------|---------|-------------|
| **`int`** | `int value = 5;` | Integer value. |
| **`string`** | `string name = "ADD";` | Text string. |
| **`bit`** | `bit isReturn = 0;` | Boolean (`0` or `1`). |
| **`dag`** | `(outs GPR:$dst)` | Directed Acyclic Graph (DAG) for operands. |
| **`list<T>`** | `list<Register> regs = [R0, R1];` | List of elements. |
| **`code`** | `code asm = "{ return true; }";` | Embedded C++ code. |

---

## **3. DAG (Directed Acyclic Graph) Syntax**
Used for **operands** and **pattern matching**:
```tablegen
// Format: (operator operand1, operand2, ...)
def ADD : Instruction {
  let OutOperandList = (outs GPR:$dst);          // Output operand
  let InOperandList = (ins GPR:$src1, GPR:$src2); // Input operands
  let Pattern = [(set GPR:$dst, (add GPR:$src1, GPR:$src2))]; // IR → MachineInstr
}
```

### **Common DAG Operators**
| Operator | Meaning | Example |
|----------|---------|---------|
| `set` | Defines a result | `(set R0, (add R1, R2))` |
| `add` | Integer addition | `(add GPR:$a, GPR:$b)` |
| `load` | Memory load | `(load GPR:$addr)` |
| `store` | Memory store | `(store GPR:$val, GPR:$addr)` |
| `brcond` | Conditional branch | `(brcond (seteq R0, 0), label)` |

---

## **4. Register Definitions**
### **Register Class**
```tablegen
// Define a register class (GPR = General Purpose Registers)
def GPR : RegisterClass<"SimpleRISC", [i32], 32, (add R0, R1, R2, R3)>;
```
- `"SimpleRISC"`: Target name.
- `[i32]`: Supported types (32-bit integers).
- `32`: Register size in bits.
- `(add R0, R1, ...)`: List of registers.

### **Individual Register**
```tablegen
def R0 : Register<"R0">, DwarfRegNum<[0]>;  // DWARF debug info reg number
def SP : Register<"SP">;  // Stack pointer
```

---

## **5. Instruction Definitions**
### **Basic Instruction**
```tablegen
class Inst<dag outs, dag ins, string asmstr> {
  dag OutOperandList = outs;
  dag InOperandList = ins;
  string AsmString = asmstr;
}

def ADD : Inst<(outs GPR:$dst), (ins GPR:$src1, GPR:$src2), "add $dst, $src1, $src2">;
```

### **Instruction with Pattern Matching**
```tablegen
def SUB : Inst<(outs GPR:$dst), (ins GPR:$src1, GPR:$src2), "sub $dst, $src1, $src2",
  [(set GPR:$dst, (sub GPR:$src1, GPR:$src2))]>;
```

---

## **6. Multiclasses (Grouping Related Instructions)**
```tablegen
// Define a multiclass for arithmetic ops
multiclass ArithOps<string mnemonic, SDNode OpNode> {
  def rr : Inst<(outs GPR:$dst), (ins GPR:$src1, GPR:$src2),
              !strconcat(mnemonic, " $dst, $src1, $src2"),
              [(set GPR:$dst, (OpNode GPR:$src1, GPR:$src2))]>;
  
  def ri : Inst<(outs GPR:$dst), (ins GPR:$src1, i32imm:$imm),
              !strconcat(mnemonic, " $dst, $src1, $imm"),
              [(set GPR:$dst, (OpNode GPR:$src1, imm:$imm))]>;
}

// Instantiate ADD/SUB variants
defm ADD : ArithOps<"add", add>;
defm SUB : ArithOps<"sub", sub>;
```
- `defm` generates multiple instructions (`ADD_rr`, `ADD_ri`, etc.).

---

## **7. Constraints & Predicates**
### **Predicate (Guard Conditions)**
```tablegen
class RequiresPred<string pred> {
  bits<32> Predicate = pred;
}

def JUMP : Inst<..., RequiresPred<"SomeCondition">>;
```

### **Operand Constraints**
```tablegen
def MOV : Inst<(outs GPR:$dst), (ins (GPR, i32imm):$src), "mov $dst, $src",
  [(set GPR:$dst, (src))]>;
```
- `(GPR, i32imm)` means the operand can be either a register or immediate.

---

## **8. Advanced Features**
### **Template Strings (`!strconcat`, `!eq`)**
```tablegen
defm ADD : ArithOps<"add", add> {
  let AsmString = !strconcat(Opcode, " $dst, $src1, $src2");
}
```

### **Including Other Files**
```tablegen
include "llvm/Target/Target.td"
include "MyTargetRegisters.td"
```

### **Let Overrides**
```tablegen
def SUB : Inst<...> {
  let isCommutable = 0;  // Subtraction is not commutative
}
```

---

## **9. Example: Full Instruction Set**
```tablegen
// Define a LOAD instruction
def LOAD : Inst<(outs GPR:$dst), (ins GPR:$addr, i32imm:$offset),
  "ld $dst, [$addr + $offset]",
  [(set GPR:$dst, (load (add GPR:$addr, imm:$offset))]>;

// Define a STORE instruction
def STORE : Inst<(outs), (ins GPR:$addr, i32imm:$offset, GPR:$val),
  "st [$addr + $offset], $val",
  [(store GPR:$val, (add GPR:$addr, imm:$offset))]>;
```

---

## **10. Summary of Key Syntax**
| **Feature** | **Syntax** | **Purpose** |
|-------------|-----------|-------------|
| **Class** | `class Name<...> { ... }` | Template for definitions. |
| **Definition** | `def Name : Class<...>;` | Concrete instance. |
| **Multiclass** | `multiclass Name<...> { ... }` | Group related definitions. |
| **DAG** | `(operator op1, op2)` | Operand/pattern matching. |
| **RegisterClass** | `def RC : RegisterClass<...>` | Set of registers. |
| **`let` Override** | `let Field = Value;` | Modify inherited values. |

---

### **TableGen (`.td`) Example: Defining a Simple RISC-like ISA**  
TableGen (`.td`) files in LLVM define **target instructions, registers, and scheduling information** in a declarative way. Below is an example for a fictional **32-bit RISC architecture** called `SimpleRISC`.

---

## **1. Define the Target Architecture (`SimpleRISC.td`)**
```tablegen
//===------ SimpleRISC.td - Target Description for SimpleRISC ------===//
// Defines registers, instructions, and patterns for SimpleRISC.

// Include common LLVM TableGen definitions
include "llvm/Target/Target.td"

// Define the SimpleRISC target
def SimpleRISC : Target {
  let InstructionSet = SimpleRISCInstr;
}

//===------------------------ Registers -------------------------===//
// Define a 32-bit register class
def GPR : RegisterClass<"SimpleRISC", [i32], 32, (add
  (sequence "R%u", 0, 15)  // Registers R0-R15
)>;

// Assign a simple register for the stack pointer
def SP : Register<"SP">, DwarfRegNum<[13]>;

//===------------------------ Instructions ----------------------===//
// Define a base instruction class
class SimpleRISCInst<dag outs, dag ins, string asmstr, list<dag> pattern>
  : Instruction {
  let Namespace = "SimpleRISC";
  let OutOperandList = outs;
  let InOperandList = ins;
  let AsmString = asmstr;
  let Pattern = pattern;
}

// Example: ADD instruction (R3 = R1 + R2)
def ADD : SimpleRISCInst<(outs GPR:$dst), (ins GPR:$src1, GPR:$src2),
  "ADD $dst, $src1, $src2",
  [(set GPR:$dst, (add GPR:$src1, GPR:$src2))]
>;

// Example: LOAD instruction (R1 = [R2 + imm])
def LOAD : SimpleRISCInst<(outs GPR:$dst), (ins GPR:$addr, i32imm:$offset),
  "LOAD $dst, [$addr + $offset]",
  [(set GPR:$dst, (load (add GPR:$addr, imm:$offset)))]
>;

// Example: STORE instruction ([R1 + imm] = R2)
def STORE : SimpleRISCInst<(outs), (ins GPR:$addr, i32imm:$offset, GPR:$val),
  "STORE [$addr + $offset], $val",
  [(store GPR:$val, (add GPR:$addr, imm:$offset))]
>;

// Example: BRANCH instruction (if R1 == 0, jump to label)
def BEQ : SimpleRISCInst<(outs), (ins GPR:$cond, bb:$target),
  "BEQ $cond, $target",
  [(brcond (seteq GPR:$cond, 0), bb:$target)]
>;
```

---

## **2. How LLVM Uses This `.td` File**
When you run `llc` on an LLVM IR file, it:
1. **Matches IR patterns** (e.g., `add`, `load`, `store`) to the TableGen-defined instructions.
2. **Generates machine instructions** (e.g., `ADD`, `LOAD`, `STORE`).
3. **Emits assembly or object code**.

---

## **3. Example LLVM IR → SimpleRISC Assembly**
### **Input LLVM IR (`input.ll`)**
```llvm
define i32 @example(i32 %a, i32 %b) {
  %sum = add i32 %a, %b
  ret i32 %sum
}
```

### **Generated Assembly (`llc -march=simplerisc input.ll -o output.s`)**
```asm
; SimpleRISC Assembly Output
ADD R0, R1, R2  ; R1 = %a, R2 = %b, R0 = %sum
RET R0           ; Return R0
```

---

## **4. Key Concepts in TableGen**
| **Feature** | **Example** | **Purpose** |
|-------------|------------|------------|
| **RegisterClass** | `def GPR : RegisterClass<...>` | Defines a set of registers (e.g., R0-R15). |
| **Instruction** | `def ADD : SimpleRISCInst<...>` | Defines an instruction (opcode + operands). |
| **Pattern Matching** | `[(set GPR:$dst, (add GPR:$src1, GPR:$src2))]` | Maps LLVM IR `add` to `ADD` instruction. |
| **Constraints** | `(ins GPR:$src1, GPR:$src2)` | Specifies input operands must be in `GPR`. |

---

## **5. Advanced: Adding Constraints & Variants**
### **Immediate Values (Small Constants)**
```tablegen
// Constrain immediate to 16 bits
def ADDi : SimpleRISCInst<(outs GPR:$dst), (ins GPR:$src1, i16imm:$imm),
  "ADDi $dst, $src1, $imm",
  [(set GPR:$dst, (add GPR:$src1, imm:$imm))]
>;
```

### **Conditional Execution**
```tablegen
// Compare and branch
def CMP : SimpleRISCInst<(outs), (ins GPR:$a, GPR:$b),
  "CMP $a, $b",
  [(set (i32 0), (seteq GPR:$a, GPR:$b))]  ; Sets flags
>;

def BEQ : SimpleRISCInst<(outs), (ins bb:$target),
  "BEQ $target",
  [(brcond (seteq (i32 0), (i32 0)), bb:$target)]  ; Uses flags
>;
```

---

- **Example patterns**:
  - `(add a, b)` → `ADD`
  - `(load (add ptr, offset))` → `LOAD`
  - `(store val, addr)` → `STORE`
