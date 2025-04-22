from tsc_cyk_algo import TwoSidedContextCYK

def test_scope():
  grammar = {
      "S": [["DECL", "STMT"]],
      "DECL": [["var", "x"]],
      "STMT": [["x", "=", "1"]],
  }
  left_context = {"DECL": {"begin"}}
  right_context = {"STMT": {"end"}}
  parser = TwoSidedContextCYK(grammar, left_context, right_context, "S")
  
  # Tests
  assert parser.parse("begin var x x = 1 end") == True
  assert parser.parse("var x x = 1") == False  # Missing scoping

def test_number_check():
  grammar = {
    "S": [["NUM", "NOUN"]],
    "NUM": [["1"], ["2"], ["3"]],
    "NOUN": [["cat"], ["cats"]],
  }
  left_context = {
    "cat": {"1"},      # "cat" requires "1" to the left
    "cats": {"2", "3"} # "cats" requires "2" or "3"
  }
  parser = TwoSidedContextCYK(grammar, left_context, {}, "S")

  # Tests
  assert parser.parse("1 cat") == True
  assert parser.parse("3 cats") == True
  assert parser.parse("2 cat") == False  # Number mismatch

def test_indent_python():
  grammar = {
      "PROGRAM": [["STMTS"]],
      "STMTS": [["STMT", "STMTS"], ["STMT"]],
      "STMT": [["BLOCK"], ["SIMPLE_STMT"]],
      "BLOCK": [["if", "EXPR", ":", "NEWLINE", "INDENT", "STMTS", "DEDENT"]],
      "SIMPLE_STMT": [["pass", "NEWLINE"]],
      "EXPR": [["True"], ["False"]],
  }
  
  # Context constraints:
  # - INDENT only allowed after ":"
  # - DEDENT must match indentation level
  left_context = {
      "INDENT": {":"},  # INDENT requires ":" to the left
      "DEDENT": {"INDENT"}  # DEDENT must close an INDENT
  }
  
  # Track indentation depth (simplified)
  indent_stack = []
  
  def parse_with_indentation(tokens):
      parser = TwoSidedContextCYK(grammar, left_context, {}, "PROGRAM")
      adjusted_tokens = []
      for token in tokens:
          if token == "INDENT":
              indent_stack.append(1)
          elif token == "DEDENT":
              if not indent_stack:
                  return False  # Unmatched DEDENT
              indent_stack.pop()
          adjusted_tokens.append(token)
      return parser.parse(adjusted_tokens)
  
  # Test Case
  tokens = [
      "if", "True", ":", "NEWLINE",
      "INDENT", "pass", "NEWLINE", "DEDENT"
  ]
  assert parse_with_indentation(tokens) == True  # Valid block
  
  tokens = [
      "if", "True", ":", "NEWLINE",
      "DEDENT"  # Error: DEDENT without INDENT
  ]
  assert parse_with_indentation(tokens) == False

def test_xml_check():
  grammar = {
    "DOC": [["OPEN_TAG", "CONTENT", "CLOSE_TAG"]],
    "OPEN_TAG": [["<", "ID", ">"]],
    "CLOSE_TAG": [["</", "ID", ">"]],
    "CONTENT": [["TEXT"], ["DOC"]],
    "TEXT": [["word"]],
  }

  tag_stack = []

  def parse_xml(tokens):
    parser = TwoSidedContextCYK(grammar, {}, {}, "DOC")
    adjusted_tokens = []
    for token in tokens:
        if token.startswith("<") and not token.startswith("</"):
            tag_stack.append(token.strip("<>"))  # Push opening tag
        elif token.startswith("</"):
            if not tag_stack or tag_stack[-1] != token.strip("</>"):
                return False  # Mismatched tag
            tag_stack.pop()
        adjusted_tokens.append(token)
    return parser.parse(adjusted_tokens) and not tag_stack

  # Test Case
  tokens = ["<div>", "word", "</div>"]
  assert parse_xml(tokens) == True  # Valid XML

  tokens = ["<div>", "<p>", "word", "</div>", "</p>"]
  assert parse_xml(tokens) == False  # Invalid nesting

# NB: 
# Stateful Contexts (e.g., indentation stacks, tag matching) often require augmenting the parser with external state.
# Non-Context-Free Patterns (e.g., tag matching) can be handled by combining CYK with runtime checks.
