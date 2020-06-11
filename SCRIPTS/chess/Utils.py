def get_index_by_position(position):
    f = ord(position[0]) - 97
    r = int(position[1]) - 1
    return f + r * 8

def get_position_by_index(index):
    # b2 = 9
    # e3 = 20
    reminder = index % 8
    f = chr(97 + reminder)
    r = int(index / 8) + 1
    return f'{f}{r}'