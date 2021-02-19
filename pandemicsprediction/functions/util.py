import pickle


def table_to_matrix(db, row_dim, col_dim, settings):
    index: int = 0
    matrix = [[0 for x in range(col_dim)] for y in range(row_dim)]
    for line in db:
        matrix[index] = line.as_Array(settings)
        index += 1
        if index >= row_dim:
            break
    return matrix


def encode_city(city):
    if city == "iq":
        return 1
    if city == "sj":
        return 2
    return 0


def decode_city(code):
    if code == 1:
        return "iq"
    if code == 2:
        return "sj"
    # default value
    return "??"


def serialize(blackbox):
    return pickle.dumps(blackbox)


def deserialize(bytes):
    return pickle.loads(bytes)
