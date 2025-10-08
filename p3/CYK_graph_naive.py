import copy

G={
    'A':[['a']],
    'B':[['d']],
    'C':[['c']],
    'D':[['A','B']],
    'E':[['B','C']],
    'S':[['D','E']]
 }


def search_lhs_non_terminal_rule(first, second):
    res = []
    for k,v in G.items():
        for item in v:
            if [first,second] == item:
                res.append(k)
                print("==rule found:", first, second,"<-",k)
    return res


def search_lhs_terminal_rule(term=None):
    if not term:
        return []
    res = []
    for k,v in G.items():
        for rhs_item in v:
            if len(rhs_item) == 1:
                if term == rhs_item[0]:
                    res.append(k)
    return res


def logM(M, prefix_msg=None, postfix_msg=None):
    if prefix_msg:
        print(prefix_msg)
    
    # Find the maximum width needed for any element in the matrix
    max_width = 0
    for row in M:
        for item in row:
            item_str = str(item)
            if len(item_str) > max_width:
                max_width = len(item_str)
    
    # Print each row with aligned columns
    for row in M:
        # Convert all elements to strings and format with padding
        formatted_row = [f" {str(item):>{max_width}} " for item in row]
        print("[" + "".join(formatted_row) + "]")
    
    if postfix_msg:
        print(postfix_msg)
    return M


def matrCmp(M1, M2):
    for i,row in enumerate(M1):
        for j in range(len(row)):
            if not M1[i][j] == M2[i][j]:
                return False
    return True


def CYK_graph(M, G = None, log=True):
    M1 = copy.deepcopy(M)
    for i,row in enumerate(M):
        for j in range(len(row)):
            nonterm_list = search_lhs_terminal_rule(M[i][j])
            M[i][j] = nonterm_list

    if log == True:
        logM(M, "After 1st step:")

    n = len(M)
    # динамика для 2 шага и далее:
    while not matrCmp(M1, M):
        M1 = copy.deepcopy(M)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    first_non_term_set = M[i][k]
                    second_non_term_set = M[k][j]

                    for lhr in first_non_term_set:
                        for rhr in second_non_term_set:
                            ntr = search_lhs_non_terminal_rule(lhr, rhr)
                            if len(ntr) > 0:

                                try:
                                    M[i][j] += search_lhs_non_terminal_rule(lhr, rhr)
                                except TypeError:
                                    M[i][j] = search_lhs_non_terminal_rule(lhr, rhr)
                                M[i][j]=list(set(M[i][j]))

        if log:
            logM(M, prefix_msg="M after current pass:")


if __name__ == '__main__':
    print("==========Test 1===========")
    graph1 = [
        ['0', 'a', '0', '0', '0'],
        ['0', '0', 'd', '0', '0'],
        ['0', '0', '0', 'd', '0'],
        ['0', '0', '0', '0', 'c'],
        ['0', '0', '0', '0', '0'],
    ]

    CYK_graph(graph1, G)
    print("==========Test 2===========")
    graph2 = [
        ['0', 'a', '0', '0', '0'],
        ['0', '0', 'd', '0', '0'],
        ['0', '0', '0', 'd', '0'],
        ['0', '0', '0', 'c', 'c'],
        ['0', '0', '0', '0', '0']
    ]

    CYK_graph(graph2, G)
    
