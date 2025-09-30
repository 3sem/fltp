**Flex transforms regex rules into a DFA**:

## Flex Compilation Pipeline

### 1. **Regex → NFA (Nondeterministic Finite Automaton)**
Flex converts each regex pattern into an NFA using **Thompson's construction**:
- Basic regex elements become NFA states and transitions
- Operators (`|`, `*`, `+`, `?`) combine smaller NFAs
- Your rules become:
  - `{nonws}+` = `[^ \t\n]+`
  - `{ws}+` = `[ \t]+`
  - `\n` = literal newline

### 2. **NFA → DFA (Deterministic Finite Automaton)**
Using **subset construction**:
- Creates a DFA where each state represents a set of possible NFA states
- Ensures deterministic behavior (one transition per input character)
- Much faster execution than NFA

### 3. **DFA Minimization & Optimization**
- **State minimization**: Merges equivalent states
- **Table compression**: Optimizes transition table storage
- Your specific DFA would have states for:
  - Matching non-whitespace sequences
  - Matching whitespace sequences  
  - Handling newlines
  - EOF detection

## Generated Code Structure

The generated `lex.yy.c` contains:

### **Transition Tables**
```c
static const yy_state_type yy_transition[] = {
    /* States and their transitions for each input character */
    0, 1, 2, 1, 3, 4, ... 
};
```

### **Scanner Engine**
```c
YY_DECL {
    yy_state_type current_state;
    char *yy_cp;
    
    current_state = YY_START;
    
    for (;;) {
        yy_cp = yy_c_buf_p;
        current_state = yy_current_state;
        
        /* DFA simulation loop */
        while (yy_chk[yy_base[current_state] + *yy_cp] != current_state) {
            current_state = yy_def[current_state];
            if (current_state >= YY_FINAL) 
                break;
        }
        
        /* Pattern matched - execute action */
        if (current_state == STATE_MATCH_NONWS) {
            cc += yyleng; ++wc;
        }
        // ... other actions
    }
}
```

## Why DFA? Performance!

- **O(n) time complexity** regardless of pattern complexity
- **Single pass** over input
- **Constant time per character** (just table lookups)
- **No backtracking** unlike regex engines like PCRE
