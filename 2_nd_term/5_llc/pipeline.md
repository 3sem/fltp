### Code Generation Pipeline
```text
LLC follows a structured lowering process:
a) Instruction Selection (DAG Lowering)

    Converts LLVM IR into a SelectionDAG (Directed Acyclic Graph) representing operations.

    Matches IR patterns to target-specific instructions using a TableGen-defined instruction set.

b) Legalization

    Ensures the DAG only contains operations natively supported by the target.

        Expands unsupported operations (e.g., 64-bit ops on 32-bit machines).

        Converts illegal types to legal ones.

c) Optimization (Machine-IR Level)

    Applies machine-specific optimizations:

        DAG Combiner – Simplifies operations.

        Machine Instruction Scheduling – Reorders instructions for efficiency.

d) Register Allocation

    Maps virtual registers to physical registers (or spills to memory if needed).

    Algorithms: Linear Scan, Graph Coloring (default in LLVM).

e) Instruction Scheduling

    Reorders instructions to minimize pipeline stalls (important for superscalar CPUs).

f) Code Emission

    Generates either:

        Assembly (text) (-filetype=asm).

        Object code (-filetype=obj via MC Layer).

5. Machine Code (MC) Layer

    The MC Layer handles final binary encoding.

    Output formats:

        ELF (Linux), COFF (Windows), Mach-O (macOS).

        Direct object emission (.o files) instead of textual assembly.

6. Output

The final output can be:

    Assembly file (.s) – Human-readable.

    Object file (.o) – Directly linkable.

    Executable – If linked (via ld or lld).
```

---


