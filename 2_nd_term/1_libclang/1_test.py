import sys
from clang.cindex import Index, CursorKind

def analyze_c_file(file_path):
    # Create an index
    index = Index.create()

    # Parse the C file
    translation_unit = index.parse(file_path)

    # Get the root cursor
    cursor = translation_unit.cursor

    # Traverse the AST
    traverse_ast(cursor)

def traverse_ast(cursor, indent=0):
    # Print the current node
    print('  ' * indent + f'{cursor.kind}: {cursor.spelling}')

    # Recursively traverse child nodes
    for child in cursor.get_children():
        traverse_ast(child, indent + 1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <c_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    analyze_c_file(file_path)
