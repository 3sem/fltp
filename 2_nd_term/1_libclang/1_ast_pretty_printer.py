import sys
from clang.cindex import Index, CursorKind

def analyze_c_file(file_path):
    index = Index.create()
    translation_unit = index.parse(file_path)
    cursor = translation_unit.cursor
    print_ast(cursor)

def print_ast(cursor, level=0):
    # Define ANSI color codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"

    # Get the cursor kind and spelling
    kind = cursor.kind
    spelling = cursor.spelling or "<no spelling>"
    
    # Create the tree structure
    prefix = "│   " * (level - 1) + "├── " if level > 0 else ""
    
    # Color-code different types of nodes
    if kind == CursorKind.FUNCTION_DECL:
        node_info = f"{BOLD}{CYAN}{kind.name}{RESET} : {GREEN}{spelling}{RESET}"
    elif kind == CursorKind.VAR_DECL:
        node_info = f"{BOLD}{YELLOW}{kind.name}{RESET} : {spelling}"
    else:
        node_info = f"{kind.name} : {spelling}"
    
    # Print the node
    print(f"{prefix}{node_info}")
    
    # Recursively print children
    for child in cursor.get_children():
        print_ast(child, level + 1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <c_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    analyze_c_file(file_path)
