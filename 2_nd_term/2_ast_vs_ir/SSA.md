To visualize the concept of **Static Single Assignment (SSA)** in LLVM IR, we can create a diagram that shows how variables are assigned exactly once and how **phi nodes** are used to handle control flow merges. Below is a textual representation of the figure, which you can recreate using tools like **Graphviz**, **Lucidchart**, or **draw.io**.

---

### **Figure: LLVM SSA Form**

```
+-------------------+       +-------------------+     
|                   |       |                   |     
|                   |       |   SSA Form        |       |   Phi Nodes :     |
|                   |       |                   |       |                   |
|  int x = 10;      |       |  %x1 = 10         |       |  %x3 = phi i32    |
|  if (cond) {      |       |  br i1 %cond,     |       |    [%x1, %entry], |
|    x = 20;        |  -->  |    label %true,   |       |    [%x2, %true]   |
|  }                |       |    label %false   |       
|  return x;        |       |  true:            |    
|                   |       |    %x2 = 20       |   
+-------------------+       |    br label %merge|    
                            |  false:           |      
                            |    br label %merge|     
                            |  merge:           |     
                            |    %x3 = phi i32  |      
                            |      [%x1, %entry]|      
                            |      [%x2, %true] |      
                            |    ret i32 %x3    |       
                            +-------------------+       
```

---

### **Explanation of the Figure**

1. **Non-SSA Code**:
   - variable `x` that is assigned in multiple places (violating SSA).

2. **SSA Form**:
   - Each variable is assigned exactly once.
   - New versions of the variable are created for each assignment (e.g., `%x1`, `%x2`).
   - Control flow merges (e.g., after an `if` statement) are handled using **phi nodes**.

3. **Phi Nodes**:
   - A phi node (`phi`) selects a value based on the predecessor block.
   - In the example, `%x3` gets its value from either `%x1` (from the `entry` block) or `%x2` (from the `true` block).

---

### **Steps in the Transformation**

1. **Convert to SSA**:
   - Each assignment to a variable creates a new version of the variable.
   - Example:
     - `int x = 10;` becomes `%x1 = 10`.
     - `x = 20;` becomes `%x2 = 20`.

2. **Insert Phi Nodes**:
   - At control flow merge points, phi nodes are inserted to select the correct value of a variable based on the incoming edge.
   - Example:
     - `%x3 = phi i32 [%x1, %entry], [%x2, %true]`.

3. **Replace Uses**:
   - All uses of the original variable are replaced with the appropriate SSA version.

---

### **How to Recreate the Figure**

1. **Using Graphviz**:
   - Write a `.dot` file to describe the graph:
     ```dot
     digraph SSA {
       rankdir=LR;
       node [shape=box];

       NonSSA [label="Non-SSA Code\nint x = 10;\nif (cond) {\n  x = 20;\n}\nreturn x;"];
       SSA [label="SSA Form\n%x1 = 10\nbr i1 %cond, label %true, label %false\n\ntrue:\n  %x2 = 20\n  br label %merge\n\nfalse:\n  br label %merge\n\nmerge:\n  %x3 = phi i32 [%x1, %entry], [%x2, %true]\n  ret i32 %x3"];
       PhiNodes [label="Phi Nodes\n%x3 = phi i32 [%x1, %entry], [%x2, %true]"];

       NonSSA -> SSA [label="Convert to SSA"];
       SSA -> PhiNodes [label="Insert Phi Nodes"];
     }
     ```
   - Render the graph using the `dot` command:
     ```bash
     dot -Tpng ssa.dot -o ssa.png
     ```

2. **Using draw.io**:
   - Open [draw.io](https://app.diagrams.net/).
   - Create three boxes for **Non-SSA Code**, **SSA Form**, and **Phi Nodes**.
   - Connect the boxes with arrows labeled **Convert to SSA** and **Insert Phi Nodes**.
   - Add the respective code snippets inside the boxes.

---

### **Example LLVM IR Code**

Here’s the LLVM IR code corresponding to the SSA form in the figure:

```llvm
define i32 @main(i1 %cond) {
entry:
  %x1 = 10
  br i1 %cond, label %true, label %false

true:
  %x2 = 20
  br label %merge

false:
  br label %merge

merge:
  %x3 = phi i32 [%x1, %entry], [%x2, %true]
  ret i32 %x3
}
```

---

### **Summary**
- SSA form ensures each variable is assigned exactly once.
- Phi nodes are used to handle control flow merges.
- The figure illustrates the transformation from non-SSA code to SSA form with phi nodes.
- You can recreate the figure using tools like Graphviz or draw.io for better visualization.
