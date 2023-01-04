def loadBoard(filename):
    with open(filename, 'r') as f:
        board = [list(line.strip()) for line in f.readlines()]
    return board