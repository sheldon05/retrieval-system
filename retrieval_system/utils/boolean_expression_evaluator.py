from django.db.models import Q


"""
Grammar to evaluate boolean expresions:
E -> TX
X -> or TX | epsilon
T -> FY
Y -> and FY | epsilon
F -> not Z | Z
Z -> (E) | b
"""


def evaluate(tokens, documents) -> Q:
    """
    Evaluates an expression recursively.
    """

    def E(i):
        i, term = T(i)
        return X(i, term)

    def X(i, value):
        if i < len(tokens):
            if tokens[i] == "or":
                i += 1
                i, term2 = T(i)
                result = value.union(term2)
                i, value = X(i, result)

        return i, value

    def T(i):
        i, fact = F(i)
        return Y(i, fact)

    def Y(i, value):
        if i < len(tokens):
            if tokens[i] == "and":
                operator = tokens[i]
                i += 1
                i, fact2 = F(i)
                result = value.intersection(fact2)
                i, value = Y(i, result)

        return i, value

    def F(i):
        if tokens[i] == "not":
            i += 1
            i, value = Z(i)
            return i, documents.difference(value)

        else:
            return Z(i)

    def Z(i):
        if tokens[i] not in ["(", ")", "and", "or", "not"]:
            return i + 1, documents.filter(term_documents__term__key=tokens[i])

        elif tokens[i] == "(":
            i, exp = E(i + 1)
            if i == len(tokens):
                raise Exception(
                    f"Expected token ')' at {i-1}. Instead got {tokens[i-1]}"
                )
            if tokens[i] != ")":
                raise Exception(f"Expected token ')' at {i}. Instead got {tokens[i]}")
            return i + 1, exp

        else:
            raise Exception("Malformed Expresion")

    try:
        i, value = E(0)
        assert i == len(tokens)
        return value
    except Exception as error:
        print(error)
        return None


# testing
# query = "chuchi and kuko or not ( nosy or jorge )"
# document = ['chuchi', 'jorge']

# query = query_tokenizer(query)
# print(evaluate(query, document))
