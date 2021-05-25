def print_grammar(grammar):
    print("P = {")
    for key in grammar:
        for value in grammar[key]:
            print(key, "→", value)
    print("}")


def get_grammar(filename):
    stream = open(filename, "r")
    grammar = dict()

    vn = ((stream.readline().strip()).split(' '))
    vt = ((stream.readline().strip()).split(' '))
    for line in stream:
        rule = line.strip().split(' ')
        if rule[0] in grammar:
            grammar[rule[0]].append(rule[1])
        else:
            grammar[rule[0]] = [rule[1]]

    stream.close()

    # Print grammar
    # print("VN = ", vn)
    # print("VT = ", vt)
    # print_grammar(grammar)
    return [grammar, vn, vt]


def first(character, grammar, vn, vt):
    if character in vt:
        return [character]
    if character in vn:
        ret = []
        for production in grammar[character]:
            frst = first(production[0], grammar, vn, vt)
            for result in frst:
                if result not in ret:
                    ret.append(result)
        return ret
    return ['ε']


def follow(character, grammar, vn, vt):
    if character == 'S':
        return ['$']

    ret = []
    if character in vn:
        for key, value in grammar.items():
            for production in value:
                if character in production:
                    index = production.index(character)
                    result_list = []
                    if index >= len(production) - 1:
                        if key != character:
                            result_list = follow(key, grammar, vn, vt)
                    else:
                        result_list = first(production[index + 1], grammar, vn, vt)

                    for result in result_list:
                        result = result.replace('ε', '')
                        if result not in ret and result != '':
                            ret.append(result)
    return ret


def get_table(grammar, vn, vt):
    ret = {}
    vt.append('$')
    vt.append('ε')
    for val, keys in grammar.items():
        for key in keys:
            alpha_list = first(key[0], grammar, vn, vt)
            for alpha in alpha_list:
                if alpha == 'ε':
                    follow_list = follow(key, grammar, vn, vt)
                    for follow_chars in follow_list:
                        ret[val, follow_chars] = key
                ret[(val, alpha)] = key
    return ret


def input_string(string, parse_table):
    string += '$'
    stack = ['S', '$']
    input_counter = 0
    print("Parsing:")
    while len(stack):
        stack_counter = 0
        stack_symbol = stack[stack_counter]
        input_symbol = string[input_counter]
        if stack_symbol == input_symbol and stack_symbol == '$':
            return True

        if stack_symbol == input_symbol:
            stack.pop(0)
            input_counter += 1
            continue

        if (stack_symbol, input_symbol) in parse_table or (stack_symbol, 'ε') in parse_table:
            if (stack_symbol, input_symbol) not in parse_table:
                input_symbol = 'ε'
            replacement = parse_table[(stack_symbol, input_symbol)]
            print(stack[0], '→', replacement)
            stack.pop(0)
            if replacement == 'ε':
                continue
            for char in reversed(replacement):
                stack.insert(0, char)
        else:
            return False


def main():
    [grammar_v12, vn_v12, vt_v12] = get_grammar("grammar_v12.txt")
    table_v12 = get_table(grammar_v12, vn_v12, vt_v12)
    input_v12 = 'abgdcf'
    print("Parsing Result for V12: '" + input_v12 + "'", input_string(input_v12, table_v12))

    [grammar_example, vn_example, vt_example] = get_grammar("grammar_example.txt")
    table_example = get_table(grammar_example, vn_example, vt_example)
    input_example = 'ababacdabae'
    print("Parsing Result for example: '" + input_example + "'", input_string(input_example, table_example))

    print(
        "Results on V12 instead of V14 because V13 V14 and V15 have left-recursions, which makes the grammars ll(1) "
        "incompatible")


main()
