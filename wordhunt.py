import time
import networkx as nx
from matplotlib import pyplot as plt
import json
class Cell(object):
    """docstring for Cell"""
    def __init__(self, xposition, yposition, letter, board):
        super(Cell, self).__init__()
        self.xposition = xposition
        self.yposition = yposition
        self.letter = letter
        self.board = board
        self.next_letters = []
        self.neighbors = []

    def pos(self):
        return (self.yposition / 4,(self.board.height - self.xposition) / 4)

    def __str__(self):
        return self.letter 

    def __repr__(self):
        return self.letter

    def get_neighbors(self):
        if self.neighbors:
            return self.neighbors
        xposition = self.xposition
        yposition = self.yposition
        neighbors = []
        if xposition > 0:
            neighbors.append(self.board.cells[xposition - 1][yposition])
        if xposition < self.board.width - 1:
            neighbors.append(self.board.cells[xposition + 1][yposition])
        if yposition > 0:
            neighbors.append(self.board.cells[xposition][yposition - 1])
        if yposition < self.board.height - 1:
            neighbors.append(self.board.cells[xposition][yposition + 1])
        if xposition > 0 and yposition > 0:
            neighbors.append(self.board.cells[xposition - 1][yposition - 1])
        if xposition < self.board.width - 1 and yposition < self.board.height - 1:
            neighbors.append(self.board.cells[xposition + 1][yposition + 1])
        if yposition > 0 and xposition < self.board.width - 1:
            neighbors.append(self.board.cells[xposition + 1][yposition - 1])
        if yposition < self.board.height - 1 and xposition > 0:
            neighbors.append(self.board.cells[xposition - 1][yposition + 1])
        self.neighbors = neighbors
        return neighbors

    def next_letters(self):
        if not self.next_letters:
            self.next_letters = [neighbor.letter for neighbor in self.get_neighbors()]
        return self.next_letters

class Board(object):
    """docstring for Board"""
    def __init__(self, letters):
        super(Board, self).__init__()
        self.cells = []
        self.width = len(letters)
        self.height = len(letters[0])
        self.flat_cells = []
        for x in range(self.width):
            self.cells.append([])
            for y in range(self.height):
                self.cells[-1].append(Cell(x, y, letters[x][y], self))

    def get_cells(self):
        if not self.flat_cells:
            self.flat_cells = [cell for col in self.cells for cell in col]
        return self.flat_cells


def get_words(size=3):
    initwords = [word for word in json.loads(open("words_list.json","r").read()) if len(word) > 2]
    words = sorted(initwords, key=lambda k: k, reverse=True)
    return words

def check_words(words, cell, path="", cellpath=[]):
    found_words = []
    raw_found_words = []
    path += cell.letter
    cellpath = cellpath.copy()
    cellpath.append(cell)
    for word in words:
        if word == path:
            raw_found_words.append(word)
            found_words.append({'word':word,'cellpath':cellpath,})
            break
    new_words = []
    for word in words:
        if word.startswith(path):
            new_words.append(word)
    if not len(new_words):
        return found_words
    for cell in cell.get_neighbors():
        if cell in cellpath:
            continue
        for found_word in check_words(new_words, cell, path, cellpath):
            if found_word['word'] not in raw_found_words:
                found_words.append(found_word)
                raw_found_words.append(found_word['word'])
    return found_words

def check_all_words(board, words):
    my_words = []
    raw_found_words = []
    for cell in board.get_cells():
        for found_word in check_words(words, cell):
            if found_word['word'] not in raw_found_words:
                my_words.append(found_word)
                raw_found_words.append(found_word['word'])
    all_words = sorted(my_words, key=lambda k: len(k['word']), reverse=True)
    return all_words

def plot(cells):
    G = nx.DiGraph()
    G.add_nodes_from([c.pos() for c in cells])

    plt.figure(figsize=(6,6))
    pos = {c.pos():c.pos() for c in cells}
    labels = {c.pos():c.letter for c in cells}
    if len(cells) > 1:
        for i, cell in enumerate(cells[1:]):
            G.add_edge(cells[i].pos(),cell.pos())
    nx.draw_networkx_labels(G,
                            pos=pos,
                            labels=labels)
    nx.draw(G,
            pos=pos,
            node_color='lightgreen', 
            node_size=600)
    return plt

def go_next(current_index=0):
    all_cells = board.get_cells()
    cells = all_words[current_index]['cellpath']
    G = nx.DiGraph()
    G.add_nodes_from([c.pos() for c in all_cells])
    plt.figure(figsize=(6,6))
    pos = {c.pos():c.pos() for c in all_cells}
    labels = {c.pos():c.letter for c in all_cells}
    if len(cells) > 1:
        for i, cell in enumerate(cells[1:]):
            G.add_edge(cells[i].pos(),cell.pos())
    print('word: ', all_words[current_index]['word'])
    nx.draw_networkx_labels(G,
        pos=pos,
        labels=labels)
    colors = []
    for cell in all_cells:
        try:
            colors.append(cells.index(cell) + 1)
        except ValueError:
            colors.append(0)
    nx.draw(G,
        pos=pos,
        node_color=colors, 
        node_size=600,
        cmap=plt.cm.Blues,
        )
    plt.title(all_words[current_index]['word'])
    plt.draw()
    plt.waitforbuttonpress(0)
    plt.close()
    if current_index < len(all_words) - 1:
        go_next(current_index+1)

def convert(mystring):
    return [[letter for letter in mystring[x*4:x*4+4]] for x in range(4)]

a = convert(input('enter a game board:\n'))
board = Board(a)
words = get_words()
all_words = check_all_words(board, words)
go_next()
