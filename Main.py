def remove_occurrences(key, grammar, duplicate):
    for rule in grammar:
        productions_list = grammar[rule]
        for production in productions_list:
            if key in production:
                new_production_list = []
                for old_production in productions_list:
                    new_production = old_production.replace(key, '')
                    if duplicate and new_production != old_production:
                        new_production_list.append(old_production)
                    new_production_list.append(new_production)
                grammar[rule] = new_production_list
                break


def remove_epsilon(grammar, removed=None):
    if removed is None:
        removed = []
    for key in grammar:
        if key in removed:
            continue
        productions = grammar[key]
        for value in productions:
            if value == 'ε' or value == '':
                removed.append(key)
                if len(productions) > 1:
                    remove_occurrences(key, grammar, True)
                else:
                    remove_occurrences(key, grammar, False)
                remove_epsilon(grammar, removed)
    return grammar


def remove_renaming(grammar, iteration=0):
    new_grammar = dict()
    for (key, production_list) in grammar.items():
        new_production_list = []
        for production in production_list:
            if production in grammar:
                for new_productions in grammar[production]:
                    new_production_list.append(new_productions)
            else:
                new_production_list.append(production)
        new_grammar[key] = new_production_list

    for production_list in new_grammar:
        for production in production_list:
            if production in new_grammar and iteration < 5:
                return remove_renaming(new_grammar, iteration + 1)

    return new_grammar


def remove_inaccessible(grammar):
    bool_grammar = dict()
    for key in grammar:
        bool_grammar[key] = False
    for key in grammar:
        for value in grammar[key]:
            for char in value:
                bool_grammar[char] = True

    new_grammar = dict()
    for key in grammar:
        if bool_grammar[key]:
            new_grammar[key] = grammar[key]

    return new_grammar


def remove_unproductive(grammar):
    bool_grammar = dict()
    for key in grammar:
        bool_grammar[key] = False
    change = True
    while change:
        change = False
        for key in grammar:
            for value in grammar[key]:
                for char in value:
                    if (char not in grammar or bool_grammar[char]) and not bool_grammar[key]:
                        bool_grammar[key] = True
                        change = True

    new_grammar = dict()
    for key in grammar:
        if bool_grammar[key]:
            new_grammar[key] = grammar[key]

    return new_grammar


x_counter = 0


def check_if_valid(production, vn, vt):
    return (len(production) == 1 and production[0] in vt) or (
            len(production) == 2 and production[0] in vn and production[1] in vn)


def add_new_productions(production, grammar, vn, vt):
    global x_counter

    if check_if_valid(production, vn, vt):
        return production

    for index in range(len(production)):
        if check_if_valid([production[index]], vn, vt):
            new_production = [c for c in production]

            full_production = None
            for i in range(1, x_counter + 1):
                if [new_production[index]] in grammar['X' + str(i)]:
                    full_production = 'X' + str(i)

            if full_production is not None:
                new_production[index] = full_production

                return add_new_productions(new_production, grammar, vn, vt)

            x_counter += 1
            new_symbol_name = 'X' + str(x_counter)
            vn.append(new_symbol_name)
            grammar[new_symbol_name] = [[new_production[index]]]
            new_production[index] = new_symbol_name

            return add_new_productions(new_production, grammar, vn, vt)

        elif index + 1 < len(production) and check_if_valid([production[index], production[index + 1]], vn,
                                                            vt):
            new_production = production.copy()

            # if such production is already added, just use that one
            full_production = None
            for i in range(1, x_counter + 1):
                if [new_production[index], new_production[index + 1]] in grammar['X' + str(i)]:
                    full_production = 'X' + str(i)

            if full_production is not None:
                new_production[index] = full_production
                del new_production[index + 1]

                return add_new_productions([new_production[index], new_production[index + 1]], grammar, vn, vt)

            x_counter += 1
            new_symbol_name = 'X' + str(x_counter)
            vn.append(new_symbol_name)
            grammar[new_symbol_name] = [[new_production[index], new_production[index + 1]]]
            new_production[index] = new_symbol_name
            del new_production[index + 1]

            return add_new_productions(new_production, grammar, vn, vt)


def convert_chomsky(grammar, vn, vt):
    temp_grammar = dict(grammar)
    for rule in temp_grammar:
        for production_list in grammar[rule]:
            if not check_if_valid(production_list, vn, vt):
                index = grammar[rule].index(production_list)
                grammar[rule][index] = add_new_productions(production_list, grammar, vn, vt)

    new_grammar = dict()

    for symbol, production_list in grammar.items():
        new_production_list = []
        for production in production_list:
            if isinstance(production, list):
                new_production = ''
                for string in production:
                    new_production += string
                new_production_list.append(new_production)
            else:
                new_production_list.append(production)

        new_grammar[symbol] = new_production_list

    return new_grammar


def print_grammar(grammar):
    print("P = {")
    for key in grammar:
        for value in grammar[key]:
            print(key, "->", value)
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
    print("VN = ", vn)
    print("VT = ", vt)
    print_grammar(grammar)
    return [grammar, vn, vt]


def main():
    [grammar, vn, vt] = get_grammar("grammar.txt")
    grammar = remove_epsilon(grammar)
    print("removed epsilon")
    print_grammar(grammar)
    grammar = remove_renaming(grammar)
    print("removed renaming")
    print_grammar(grammar)
    grammar = remove_inaccessible(grammar)
    print("removed inaccessible")
    print_grammar(grammar)
    grammar = remove_unproductive(grammar)
    print("removed unproductive")
    print_grammar(grammar)
    grammar = convert_chomsky(grammar, vn, vt)
    print("converted to chomsky normal form")
    print_grammar(grammar)


main()
