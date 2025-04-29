The paper **"Grammars with Two-Sided Contexts"** introduces and builds upon several formal grammar models, extending classical context-free grammars with new operators for context sensitivity. Below is a breakdown of the grammar forms discussed:

---

### **1. Context-Free Grammars (CFGs)**
- The **base model**, where rules are of the form:  
  \( A \rightarrow \alpha \) (where \( \alpha \) is a string of terminals and nonterminals).  
- **Limitation**: Rules are context-independent; they cannot specify conditions on surrounding substrings.

---

### **2. Conjunctive Grammars**
- **Extension of CFGs** with **conjunction** (`&`), allowing rules like:  
  \( A \rightarrow \alpha_1 \ \& \ \alpha_2 \ \& \ \ldots \ \& \ \alpha_k \)  
- A string must satisfy **all** conjuncts to derive \( A \).  
- **Example**:  
  \( S \rightarrow AB \ \& \ CD \) means a string must be both derivable as \( AB \) **and** \( CD \).  


---

### **3. Boolean Grammars**
- Further extends conjunctive grammars with **negation** (`¬`), enabling rules like:  
  \( A \rightarrow \alpha \ \& \ \neg \beta \)  
- **Example**:  
  \( S \rightarrow AB \ \& \ \neg a^* \) means "derive \( AB \) but exclude strings in \( a^* \)."  
- **Complexity**: More expressive but harder to parse efficiently.

---

### **4. Grammars with One-Sided Contexts**
- Introduced in the authors' prior work (**Barash & Okhotin, LATA 2012**).  
- Adds **left-context operators** (`<`, `≤`):  
  \( A \rightarrow BC \ \& \ < D \)  
  - Here, \( BC \) must appear **after** a substring derivable as \( D \).  
- **Example**:  
  \( B \rightarrow b \ \& \ < A \) means "\( b \) has property \( B \) only if it is preceded by \( A \)."  
- **Limitation**: Cannot specify right-context conditions.

---

### **5. Grammars with Two-Sided Contexts (New Contribution)**
- The **main focus** of the paper, generalizing one-sided contexts to **both left and right**.  
- **Operators**:  
  - **Left context**: `< D` (strict left), `≤ E` (extended left, includes current substring).  
  - **Right context**: `> F` (strict right), `≥ H` (extended right).  
- **Rule example**:  
  \( A \rightarrow BC \ \& \ < D \ \& \ > E \)  
  - \( BC \) must be **preceded** by \( D \) **and followed** by \( E \).  
- **Semantics**:  
  - Defined via **deduction rules** for propositions like \( A(u⟨w⟩v) \), where \( w \) is the substring and \( u, v \) are left/right contexts.  
- **Expressive power**:  
  - Can model **cross-references** (e.g., declarations before/after use).  
  - Encodes **graph reachability** (Example 5 in the paper).  

---

### **6. Binary Normal Form**
- A **normal form** for two-sided context grammars, analogous to Chomsky Normal Form for CFGs.  
- **Rules restricted to**:  
  1. \( A \rightarrow BC \ \& \ \text{(context conditions)} \)  
  2. \( A \rightarrow a \ \& \ \text{(context conditions)} \)  
- **Purpose**: Simplifies parsing and theoretical analysis.

---

### **Key Comparisons**
| Grammar Form               | Operators          | Context Sensitivity | Example Use Case               |
|----------------------------|--------------------|---------------------|--------------------------------|
| **Context-Free (CFG)**     | None               | No                  | Basic syntax rules             |
| **Conjunctive**            | `&`                | "Mildly"            | Intersection of languages      |
| **Boolean**                | `&`, `¬`           | "Greater than Conj. | Exclusion patterns             |
| **One-Sided Context**      | `<`, `≤`           | Left app. only      | Declarations before use        |
| **Two-Sided Context**      | `<`, `≤`, `>`, `≥` | Left and right app  | Prototypes, graph reachability |

---

### **Conclusion**
**grammars with two-sided contexts** are a generalization of:
1. Classical **context-free grammars**,  
2. **Conjunctive grammars** (with `&`),  
3. Their earlier **one-sided context grammars**.  

This model **unifies** context sensitivity in a logical framework, enabling natural specifications for languages requiring **bidirectional context checks** (e.g., programming language syntax with forward/backward dependencies). The **normal form** and **parsing algorithm** (O(n⁴)) demonstrate its practicality, though later work (Rabkin, 2014) improved parsing to O(n³).  

The work opens directions for **Boolean extensions**, **stochastic variants**, and applications in **biosequence modeling** (e.g., RNA pseudoknots).
