Для чего можно использовать libclang:

---

### 1. **Syntax Tree Traversal**
   - **Example**: Traverse the Abstract Syntax Tree (AST) of a C/C++ file to extract information about functions, variables, and statements.
   - **Use Case**: Analyze the structure of the code to identify patterns or anomalies.

### 2. **Type Checking**
   - **Example**: Verify the types of variables, function arguments, and return values to ensure they match expected types.
   - **Use Case**: Detect type mismatches or unsafe type conversions.

### 3. **Code Metrics Calculation**
   - **Example**: Calculate metrics such as cyclomatic complexity, number of function parameters, or depth of nested loops.
   - **Use Case**: Assess code quality and maintainability.

### 4. **Unused Code Detection**
   - **Example**: Identify unused variables, functions, or macros in the codebase.
   - **Use Case**: Clean up dead code to improve readability and reduce technical debt.

### 5. **Error and Warning Detection**
   - **Example**: Detect syntax errors, semantic errors, and potential runtime issues (e.g., null pointer dereferences).
   - **Use Case**: Improve code reliability by catching issues early.

### 6. **Dependency Analysis**
   - **Example**: Analyze include directives and dependencies between files to identify unnecessary or circular dependencies.
   - **Use Case**: Optimize build times and reduce coupling.

### 7. **Code Refactoring Support**
   - **Example**: Identify opportunities for refactoring, such as renaming variables, extracting functions, or simplifying expressions.
   - **Use Case**: Improve code readability and maintainability.

### 8. **Macro Expansion Analysis**
   - **Example**: Analyze how macros are expanded in the code and detect potential issues with macro usage.
   - **Use Case**: Prevent bugs caused by unintended macro expansions.

### 9. **Cross-Reference Analysis**
   - **Example**: Find all references to a specific function, variable, or type across the codebase.
   - **Use Case**: Understand the impact of changes or identify unused code.

### 10. **Code Style Enforcement**
   - **Example**: Check for adherence to coding standards, such as naming conventions, indentation, or brace placement.
   - **Use Case**: Ensure consistency across the codebase.

### 11. **Security Vulnerability Detection**
   - **Example**: Identify potential security issues, such as buffer overflows, use-after-free, or insecure API usage.
   - **Use Case**: Improve code security by detecting vulnerabilities early.

### 12. **Memory Management Analysis**
   - **Example**: Detect memory leaks, double frees, or improper use of dynamic memory allocation.
   - **Use Case**: Improve memory safety and prevent runtime crashes.

### 13. **API Usage Analysis**
   - **Example**: Verify that APIs are used correctly, including proper initialization and cleanup.
   - **Use Case**: Prevent misuse of libraries or frameworks.

### 14. **Template Instantiation Analysis**
   - **Example**: Analyze how C++ templates are instantiated and detect potential issues with template specialization.
   - **Use Case**: Ensure correct usage of templates and avoid code bloat.

### 15. **Code Documentation Extraction**
   - **Example**: Extract comments and documentation from the code to generate documentation automatically.
   - **Use Case**: Maintain up-to-date documentation with minimal effort.

### 16. **Control Flow Analysis**
   - **Example**: Analyze the control flow of functions to detect unreachable code or infinite loops.
   - **Use Case**: Improve code reliability and performance.

### 17. **Data Flow Analysis**
   - **Example**: Track how data flows through the program to detect uninitialized variables or redundant computations.
   - **Use Case**: Optimize code and prevent bugs.

### 18. **Cross-Platform Compatibility Analysis**
   - **Example**: Identify platform-specific code or non-portable constructs.
   - **Use Case**: Ensure code works correctly across different platforms.

### 19. **Header File Analysis**
   - **Example**: Analyze header files to detect issues such as missing include guards or redundant declarations.
   - **Use Case**: Improve compilation times and reduce errors.

### 20. **Custom Rule Enforcement**
   - **Example**: Define custom rules (e.g., banning certain functions or enforcing specific coding patterns) and check for violations.
   - **Use Case**: Enforce project-specific coding standards.

---

These examples demonstrate the versatility of LibClang for static analysis, making it a valuable tool for improving code quality, security, and maintainability. By leveraging LibClang, developers can build custom tools tailored to their specific needs.

---

import clang.cindex

def traverse_ast(node):
    """Recursively traverse the AST and print node information."""
    print(f"Kind: {node.kind}, Spelling: {node.spelling}, Location: {node.location}")
    for child in node.get_children():
        traverse_ast(child)

def analyze_code(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    traverse_ast(translation_unit.cursor)

# Example usage
analyze_code("example.c")

---

import clang.cindex

def find_unused_symbols(cursor):
    """Find unused variables or functions."""
    if cursor.kind == clang.cindex.CursorKind.VAR_DECL or cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        if not cursor.is_referenced():
            print(f"Unused symbol: {cursor.spelling} at {cursor.location}")
    for child in cursor.get_children():
        find_unused_symbols(child)

def analyze_unused_code(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    find_unused_symbols(translation_unit.cursor)

# Example usage
analyze_unused_code("example.c")

---

3. Errors

import clang.cindex

def detect_errors(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    for diag in translation_unit.diagnostics:
        print(f"{diag.severity}: {diag.spelling} at {diag.location}")

# Example usage
detect_errors("example.c")

---

4. Type checking

import clang.cindex

def check_types(cursor):
    """Check types of variables and function arguments."""
    if cursor.kind == clang.cindex.CursorKind.VAR_DECL:
        print(f"Variable: {cursor.spelling}, Type: {cursor.type.spelling}")
    elif cursor.kind == clang.cindex.CursorKind.PARM_DECL:
        print(f"Parameter: {cursor.spelling}, Type: {cursor.type.spelling}")
    for child in cursor.get_children():
        check_types(child)

def analyze_types(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    check_types(translation_unit.cursor)

# Example usage
analyze_types("example.c")

5. Code metrics

import clang.cindex

def calculate_complexity(cursor):
    """Calculate cyclomatic complexity of a function."""
    if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        complexity = 1
        for child in cursor.walk_preorder():
            if child.kind in (clang.cindex.CursorKind.IF_STMT, clang.cindex.CursorKind.FOR_STMT,
                              clang.cindex.CursorKind.WHILE_STMT, clang.cindex.CursorKind.CASE_STMT,
                              clang.cindex.CursorKind.CONDITIONAL_OPERATOR):
                complexity += 1
        print(f"Function: {cursor.spelling}, Cyclomatic Complexity: {complexity}")

def analyze_complexity(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    calculate_complexity(translation_unit.cursor)

# Example usage
analyze_complexity("example.c")

---

6. Cross-ref analysis

import clang.cindex

def find_references(cursor, target_name):
    """Find all references to a specific function or variable."""
    if cursor.kind == clang.cindex.CursorKind.DECL_REF_EXPR and cursor.spelling == target_name:
        print(f"Reference to {target_name} found at {cursor.location}")
    for child in cursor.get_children():
        find_references(child, target_name)

def analyze_references(file_path, target_name):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    find_references(translation_unit.cursor, target_name)

# Example usage
analyze_references("example.c", "my_function")

--- 

7.  Mem

import clang.cindex

def check_memory_management(cursor):
    """Detect memory leaks or improper use of dynamic memory."""
    if cursor.kind == clang.cindex.CursorKind.CALL_EXPR:
        if cursor.spelling == "malloc" or cursor.spelling == "free":
            print(f"Memory management function: {cursor.spelling} at {cursor.location}")
    for child in cursor.get_children():
        check_memory_management(child)

def analyze_memory(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    check_memory_management(translation_unit.cursor)

# Example usage
analyze_memory("example.c")

---

8. Vul detection

import clang.cindex

def detect_buffer_overflows(cursor):
    """Detect potential buffer overflows."""
    if cursor.kind == clang.cindex.CursorKind.ARRAY_SUBSCRIPT_EXPR:
        print(f"Potential buffer overflow at {cursor.location}")
    for child in cursor.get_children():
        detect_buffer_overflows(child)

def analyze_security(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    detect_buffer_overflows(translation_unit.cursor)

# Example usage
analyze_security("example.c")

---

9. Comments extraction

import clang.cindex

def extract_comments(cursor):
    """Extract comments associated with a node."""
    if cursor.raw_comment:
        print(f"Comment at {cursor.location}: {cursor.raw_comment}")
    for child in cursor.get_children():
        extract_comments(child)

def analyze_documentation(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    extract_comments(translation_unit.cursor)

# Example usage
analyze_documentation("example.c")

---

10. coding-style check

import clang.cindex

def check_naming_conventions(cursor):
    """Check if variable and function names follow camelCase or snake_case."""
    if cursor.kind == clang.cindex.CursorKind.VAR_DECL or cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        name = cursor.spelling
        if not (name.islower() or "_" in name):  # Simple check for snake_case
            print(f"Invalid naming convention: {name} at {cursor.location}")
    for child in cursor.get_children():
        check_naming_conventions(child)

def analyze_code_style(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    check_naming_conventions(translation_unit.cursor)

# Example usage
analyze_code_style("example.c")

---

11. sec v d

import clang.cindex

def detect_insecure_apis(cursor):
    """Detect usage of insecure APIs like strcpy."""
    if cursor.kind == clang.cindex.CursorKind.CALL_EXPR:
        if cursor.spelling in ["strcpy", "gets", "sprintf"]:
            print(f"Insecure API usage: {cursor.spelling} at {cursor.location}")
    for child in cursor.get_children():
        detect_insecure_apis(child)

def analyze_security(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    detect_insecure_apis(translation_unit.cursor)

# Example usage
analyze_security("example.c")

---

12 mem

import clang.cindex

def check_memory_management(cursor):
    """Detect memory leaks or improper use of dynamic memory."""
    if cursor.kind == clang.cindex.CursorKind.CALL_EXPR:
        if cursor.spelling == "malloc" or cursor.spelling == "free":
            print(f"Memory management function: {cursor.spelling} at {cursor.location}")
    for child in cursor.get_children():
        check_memory_management(child)

def analyze_memory(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    check_memory_management(translation_unit.cursor)

# Example usage
analyze_memory("example.c")

---

13 api usage analysis

import clang.cindex

def check_api_usage(cursor):
    """Check if APIs are used correctly."""
    if cursor.kind == clang.cindex.CursorKind.CALL_EXPR:
        if cursor.spelling == "open" and not has_matching_close(cursor):
            print(f"Potential resource leak: {cursor.spelling} at {cursor.location}")
    for child in cursor.get_children():
        check_api_usage(child)

def has_matching_close(cursor):
    """Check if a matching close/cleanup call exists."""
    # Implement logic to check for matching cleanup calls
    return False

def analyze_api_usage(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    check_api_usage(translation_unit.cursor)

# Example usage
analyze_api_usage("example.c")

---

14 templ inst

import clang.cindex

def analyze_template_instantiations(cursor):
    """Analyze template instantiations in C++ code."""
    if cursor.kind == clang.cindex.CursorKind.CLASS_TEMPLATE or cursor.kind == clang.cindex.CursorKind.FUNCTION_TEMPLATE:
        print(f"Template: {cursor.spelling} at {cursor.location}")
    for child in cursor.get_children():
        analyze_template_instantiations(child)

def analyze_templates(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    analyze_template_instantiations(translation_unit.cursor)

# Example usage
analyze_templates("example.cpp")

---

15 

extract code doc

import clang.cindex

def extract_comments(cursor):
    """Extract comments associated with a node."""
    if cursor.raw_comment:
        print(f"Comment at {cursor.location}: {cursor.raw_comment}")
    for child in cursor.get_children():
        extract_comments(child)

def analyze_documentation(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    extract_comments(translation_unit.cursor)

# Example usage
analyze_documentation("example.c")

---

16 cfa

import clang.cindex

def analyze_control_flow(cursor):
    """Analyze control flow to detect unreachable code."""
    if cursor.kind == clang.cindex.CursorKind.RETURN_STMT:
        print(f"Return statement at {cursor.location}")
    for child in cursor.get_children():
        analyze_control_flow(child)

def analyze_control_flow(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    analyze_control_flow(translation_unit.cursor)

# Example usage
analyze_control_flow("example.c")

17 dfa

import clang.cindex

def analyze_data_flow(cursor):
    """Analyze data flow to detect uninitialized variables."""
    if cursor.kind == clang.cindex.CursorKind.VAR_DECL:
        if not cursor.type.is_pod():  # Check if the variable is initialized
            print(f"Uninitialized variable: {cursor.spelling} at {cursor.location}")
    for child in cursor.get_children():
        analyze_data_flow(child)

def analyze_data_flow(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    analyze_data_flow(translation_unit.cursor)

# Example usage
analyze_data_flow("example.c")

18
portability analysis

import clang.cindex

def detect_platform_specific_code(cursor):
    """Detect platform-specific code or non-portable constructs."""
    if cursor.kind == clang.cindex.CursorKind.PREPROCESSING_DIRECTIVE:
        if "WIN32" in cursor.spelling or "linux" in cursor.spelling:
            print(f"Platform-specific code: {cursor.spelling} at {cursor.location}")
    for child in cursor.get_children():
        detect_platform_specific_code(child)

def analyze_platform_compatibility(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    detect_platform_specific_code(translation_unit.cursor)

# Example usage
analyze_platform_compatibility("example.c")

19

headers analysis

import clang.cindex

def check_include_guards(cursor):
    """Check if header files have include guards."""
    if cursor.kind == clang.cindex.CursorKind.INCLUSION_DIRECTIVE:
        print(f"Include directive: {cursor.spelling} at {cursor.location}")
    for child in cursor.get_children():
        check_include_guards(child)

def analyze_header_files(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    check_include_guards(translation_unit.cursor)

# Example usage
analyze_header_files("example.h")
