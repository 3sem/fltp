import pprint

class Tree:
    def __init__(self):
        self.children = {}

    # for now, just prints what should be added to it
    def add(self, node):
        print(f"Adding node |{node}|")
        return


def make_parsing_table(
    terminals: set[str],
    non_terminals: set[str],
    rule_set: dict[str, set[str]],
    first: dict[str, set[str]],
    follow: dict[str, set[str]],
    epsilon_symbol: str,
) -> dict[tuple[str, str], dict[str, str]]:
    parsing_table = {}
    for non_term in non_terminals:
        for term in terminals:
            parsing_table[(non_term, term)] = None

    for non_term in non_terminals:
        for expand_str in rule_set[non_term]:
            rule_to_add = {non_term: expand_str}
            term_pool = first[expand_str[0]]

            if epsilon_symbol in term_pool:
                term_pool.remove(epsilon_symbol)
                term_pool = term_pool | follow[non_term]

            for term in term_pool:
                if parsing_table[(non_term, term)] is None:
                    parsing_table[(non_term, term)] = rule_to_add
                else:
                    raise ValueError(
                        f"Conflicting rules for {non_term} and {term}: {parsing_table[(term, non_term)]} and {rule_to_add}"
                    )

    return parsing_table


def ll1_algorithm(
    input_string: str,
    parsing_table: dict[tuple[str, str], dict[str, str]],
    starting_symbol: str,
    end_symbol: str,
    epsilon_symbol: str,
):
    taken_len = 0
    stack = []
    stack.append(end_symbol)
    stack.append(starting_symbol)

    non_term_term_pairs = parsing_table.keys()
    non_terminals = {pair[0] for pair in non_term_term_pairs}
    terminals = {pair[1] for pair in non_term_term_pairs}

    current = input_string[taken_len]
    taken_len += 1

    while stack[-1] != end_symbol:
        stack_top = stack[-1]
        print("Stack:", stack[::-1])
        print(input_string[taken_len-1:])
        if stack_top == epsilon_symbol:
            print("Pop terminal:", epsilon_symbol)
            stack.pop()
            continue
        if stack_top == current:
            stack.pop()
            print("Pop terminal:", current)
            current = input_string[taken_len]
            taken_len += 1
        elif stack_top in non_terminals:
            corresponding_rule = parsing_table[stack_top, current]
            print("Non terminal: corresponding parsing table content", corresponding_rule)
            if corresponding_rule is None:
                raise LookupError(
                    f"parsing table empty with non_term {stack_top} and term {current}, which is {taken_len} symbol from {input_string}"
                )
            stack.pop()
            stack.extend(corresponding_rule[stack_top][::-1])
            print("Apply corresponding rule:", corresponding_rule)
        else:
            raise LookupError(
                f"terminal {current} #{taken_len} from input {input_string} is not equal to terminal{stack_top} from stack while parsing"
            )

    if current != end_symbol:
        raise LookupError(
            f"parsing of input {input_string} with len{len(input_string)} ended on {taken_len} symbol"
        )


def main():
    EPSILON = 'e'
    terminals = {"(", ")", "$"}
    non_terminals = {"S"}
    rules = {"S": {"(S)S", EPSILON}}

    first = {}
    for term in terminals:
        first[term] = {term}
    first = first | {"S":
                         {"(", EPSILON},
                     EPSILON:
                         {EPSILON}
                     }
    follow = {"S": {")", "$"}}

    table = make_parsing_table(terminals, non_terminals, rules, first, follow, EPSILON)
    input_str = "())()$"
    for k,v in table.items():
        print(k, ":", v)
    print(f"Starting to parse: {input_str}")
    ll1_algorithm(input_str, table, "S", "$", EPSILON)
    return 0


if __name__ == "__main__":
    main()
